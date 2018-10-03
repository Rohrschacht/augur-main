from ethereum.tools import tester
from ethereum.tools.tester import TransactionFailed, ABIContract
from pytest import fixture, raises
from utils import TokenDelta, EtherDelta, AssertLog

def test_bootstrap(localFixture, universe, reputationToken, auction, time):
    # Lets confirm the auction is in the dormant state initially and also in bootstrap mode
    assert auction.getAuctionType() == 0
    assert auction.bootstrapMode()
    assert not auction.isActive()

    # If we move time forward to the next auction start time we can see that the auction is now active.
    startTime = auction.getAuctionStartTime()
    assert time.setTimestamp(startTime)
    assert auction.getAuctionType() == 2
    assert auction.bootstrapMode()
    assert auction.isActive()

    # We can get the price of ETH in REP
    assert auction.getRepSalePriceInAttoEth() == auction.initialRepSalePrice()

    # However since we're in bootstrap mode we cannot yet sell REP for ETH.
    with raises(TransactionFailed):
        auction.getEthSalePriceInAttoRep()

    # If we move time forward but stay in the auction the sale price of the REP will drop accordingly. We'll move forward an hour and confirm the price is 1/24th less
    repSalePrice = auction.initialRepSalePrice() * 23 / 24
    assert time.incrementTimestamp(60 * 60)
    assert auction.getRepSalePriceInAttoEth() == repSalePrice

    # Before we do any trading lets confirm the contract balances are as expected
    assert auction.initialAttoRepBalance() == reputationToken.balanceOf(auction.address)
    assert auction.initialAttoRepBalance() == 11 * 10 ** 6 * 10 ** 18 / 400
    assert localFixture.chain.head_state.get_balance(auction.address) == 0

    # We can purchase some of the REP now. We'll send some extra ETH to confirm it just gets returned too
    repAmount = 10 ** 18
    cost = repAmount * repSalePrice / 10 ** 18
    with EtherDelta(cost, auction.address, localFixture.chain, "ETH was not transfered to auction correctly"):
        with TokenDelta(reputationToken, repAmount, tester.a0, "REP was not transferred to the user correctly"):
            assert auction.tradeEthForRep(repAmount, value=cost + 20)

    # Lets purchase the remaining REP in the auction
    repAmount = auction.currentAttoRepBalance()
    cost = repAmount * repSalePrice / 10 ** 18
    with EtherDelta(cost, auction.address, localFixture.chain, "ETH was not transfered to auction correctly"):
        with TokenDelta(reputationToken, repAmount, tester.a0, "REP was not transferred to the user correctly"):
            assert auction.tradeEthForRep(repAmount, value=cost)

    # If we try to purchase any more the transaction will fail
    with raises(TransactionFailed):
        auction.tradeEthForRep(repAmount, value=cost)

    # Lets end this auction then move time to the next auction
    endTime = auction.getAuctionEndTime()
    assert time.setTimestamp(endTime + 1)

    assert auction.getAuctionType() == 3
    assert auction.bootstrapMode()
    assert not auction.isActive()

    startTime = auction.getAuctionStartTime()
    assert time.setTimestamp(startTime)

    # We can see that the ETH and REP auctions are active
    assert auction.getAuctionType() == 6
    assert auction.isActive()

    assert auction.getRepSalePriceInAttoEth() == auction.initialRepSalePrice()
    assert auction.getEthSalePriceInAttoRep() == auction.initialEthSalePrice()

    assert not auction.bootstrapMode()

    ethSalePrice = auction.initialEthSalePrice()
    ethAmount = 10 ** 18
    cost = ethAmount * ethSalePrice / 10 ** 18
    with EtherDelta(ethAmount, tester.a0, localFixture.chain, "ETH was not transfered to user correctly"):
        with TokenDelta(reputationToken, cost, auction.address, "REP was not transferred to the auction correctly"):
            assert auction.tradeRepForEth(ethAmount)

    assert not auction.bootstrapMode()

def test_reporting_fee_from_auction(localFixture, universe, auction, reputationToken, time):
    # We'll quickly do the bootstrap auction and seed it with some ETH
    startTime = auction.getAuctionStartTime()
    assert time.setTimestamp(startTime)

    # Buy 5000 REP
    repSalePrice = auction.getRepSalePriceInAttoEth()
    repAmount = 5000 * 10 ** 18
    cost = repAmount * repSalePrice / 10 ** 18
    with EtherDelta(cost, auction.address, localFixture.chain, "ETH was not transfered to auction correctly"):
        with TokenDelta(reputationToken, repAmount, tester.a0, "REP was not transferred to the user correctly"):
            assert auction.tradeEthForRep(repAmount, value=cost)

    # Now we'll go to the first real auction, which will be a reported auction, meaning the result affects the reported REP price
    endTime = auction.getAuctionEndTime()
    assert time.setTimestamp(endTime + 1)

    startTime = auction.getAuctionStartTime()
    assert time.setTimestamp(startTime)

    # Initially the REP price of the auction will simply be what was provided as the constant initialized value and the bound values will be 0
    assert auction.getRepPriceInAttoEth() == auction.manualRepPriceInAttoEth()
    repSalePrice = auction.getRepSalePriceInAttoEth()
    assert auction.currentUpperBoundRepPriceInAttoEth() == 0
    assert auction.currentLowerBoundRepPriceInAttoEth() == 0

    # Purchasing REP or ETH will update the current auctions recorded bounds but will not yet update the official REP price
    repAmount = 10 ** 18
    cost = repAmount * repSalePrice / 10 ** 18
    assert auction.tradeEthForRep(repAmount, value=cost)

    # We purchased 1 REP for repSalePrice attoETH. Lets check the upper bound price of the auction now
    assert auction.currentUpperBoundRepPriceInAttoEth() == repSalePrice

    # If we purchase 1 ETH for ethSalePrice attoREP we'll simmilarly see the lower bound be set as such (10**36) / price of 1 ETH in attoREP.
    ethSalePrice = auction.getEthSalePriceInAttoRep()
    ethAmount = 10 ** 18
    cost = ethAmount * ethSalePrice / 10 ** 18
    assert auction.tradeRepForEth(ethAmount)

    expectedLowerBoundRepPrice = 10**36 / ethSalePrice
    assert auction.currentLowerBoundRepPriceInAttoEth() == expectedLowerBoundRepPrice

    # The reported value of REP is simply the mean of these two:
    assert auction.currentRepPrice() == (auction.currentLowerBoundRepPriceInAttoEth() + auction.currentUpperBoundRepPriceInAttoEth()) / 2

    # We'll let some time pass and buy more REP and ETH and the halfpoint prices
    assert time.incrementTimestamp(12 * 60 * 60)

    # First we purchase 2 REP at the new price
    newRepSalePrice = auction.getRepSalePriceInAttoEth()
    repAmount = 2 * 10 ** 18
    cost = repAmount * newRepSalePrice / 10 ** 18
    assert auction.tradeEthForRep(repAmount, value=cost)

    # We can observe that the recorded upper bound weighs this purchase more since more REP was purchased
    upperBoundRepPrice = (newRepSalePrice * 2 + repSalePrice) / 3
    assert auction.currentUpperBoundRepPriceInAttoEth() == upperBoundRepPrice

    # Now we'll purchase 2 ETH
    newEthSalePrice = auction.getEthSalePriceInAttoRep()
    ethAmount = 2 * 10 ** 18
    cost = ethAmount * newEthSalePrice / 10 ** 18
    assert auction.tradeRepForEth(ethAmount)

    # We can observe that the recorded lower bound weighs this purchase more since more ETH was purchased
    newExpectedLowerBoundRepPrice = 10**36 / newEthSalePrice
    lowerBoundRepPrice = (newExpectedLowerBoundRepPrice * 2 + expectedLowerBoundRepPrice) / 3
    assert auction.currentLowerBoundRepPriceInAttoEth() == lowerBoundRepPrice

    # And as before the recorded REP price is the mean of the two bounds
    derivedRepPrice = (auction.currentLowerBoundRepPriceInAttoEth() + auction.currentUpperBoundRepPriceInAttoEth()) / 2
    assert auction.currentRepPrice() == derivedRepPrice

    # Lets turn on auction price reporting and move time so that this auction is considered over
    assert localFixture.contracts["Controller"].toggleFeedSource(True)
    assert time.setTimestamp(auction.getAuctionEndTime() + 1)

    # We can see now that the auction will use the derived rep price when we request the price of rep for reporting fee purposes
    assert auction.getRepPriceInAttoEth() == derivedRepPrice

    # If we move time forward to the next auction we can confirm the price is still the derived price
    assert time.setTimestamp(auction.getAuctionStartTime())
    assert auction.getRepPriceInAttoEth() == derivedRepPrice

    # Lets purchase REP and ETH in this auction and confirm that it does not change the reported rep price, but is recorded for use internally to set auction pricing
    repSalePrice = auction.getRepSalePriceInAttoEth()

    # Note that the repSalePrice now starts at 4 x the previous auctions derived price
    assert auction.initialRepSalePrice() == 4 * derivedRepPrice

    repAmount = 10 ** 18
    cost = repAmount * repSalePrice / 10 ** 18
    assert auction.tradeEthForRep(repAmount, value=cost)

    # We can observe that the recorded upper bound weighs this purchase more since more REP was purchased
    assert auction.currentUpperBoundRepPriceInAttoEth() == repSalePrice

    # Now we'll purchase 1 ETH
    ethSalePrice = auction.getEthSalePriceInAttoRep()

    # Note that the ethSalePrice is now 4 x the previous auctions derived price in terms of ETH
    assert auction.initialEthSalePrice() == 4 * 10**36 / derivedRepPrice

    ethAmount = 10 ** 18
    cost = ethAmount * ethSalePrice / 10 ** 18
    assert auction.tradeRepForEth(ethAmount)

    # We can observe that the recorded lower bound weighs this purchase more since more ETH was purchased
    lowerBoundRepPrice = 10**36 / ethSalePrice
    assert auction.currentLowerBoundRepPriceInAttoEth() == lowerBoundRepPrice

    # And as before the recorded REP price is the mean of the two bounds
    newDerivedRepPrice = (auction.currentLowerBoundRepPriceInAttoEth() + auction.currentUpperBoundRepPriceInAttoEth()) / 2
    assert auction.currentRepPrice() == newDerivedRepPrice

    # Now lets go to the dormant state and confirm that the reported rep price is still the previous recorded auctions derived REP price
    assert time.setTimestamp(auction.getAuctionEndTime() + 1)
    assert auction.getRepPriceInAttoEth() == derivedRepPrice

    # In the next auction we will see the newly derived REP price used as the basis for auction pricing but NOT used as the reported rep price for fees
    assert time.setTimestamp(auction.getAuctionStartTime())
    assert auction.initializeNewAuction()
    assert auction.getRepPriceInAttoEth() == derivedRepPrice
    assert auction.lastRepPrice() == newDerivedRepPrice
    assert auction.initialRepSalePrice() == 4 * newDerivedRepPrice
    assert auction.initialEthSalePrice() == 4 * 10**36 / newDerivedRepPrice

@fixture(scope="session")
def localSnapshot(fixture, kitchenSinkSnapshot):
    fixture.resetToSnapshot(kitchenSinkSnapshot)
    universe = ABIContract(fixture.chain, kitchenSinkSnapshot['universe'].translator, kitchenSinkSnapshot['universe'].address)

    # Distribute REP
    reputationToken = fixture.applySignature('ReputationToken', universe.getReputationToken())
    for testAccount in [tester.a1, tester.a2, tester.a3]:
        reputationToken.transfer(testAccount, 1 * 10**6 * 10**18)

    return fixture.createSnapshot()

@fixture
def localFixture(fixture, localSnapshot):
    fixture.resetToSnapshot(localSnapshot)
    return fixture

@fixture
def reputationToken(localFixture, kitchenSinkSnapshot, universe):
    return localFixture.applySignature('ReputationToken', universe.getReputationToken())

@fixture
def universe(localFixture, kitchenSinkSnapshot):
    return ABIContract(localFixture.chain, kitchenSinkSnapshot['universe'].translator, kitchenSinkSnapshot['universe'].address)

@fixture
def auction(localFixture, kitchenSinkSnapshot, universe):
    return localFixture.applySignature('Auction', universe.getAuction())

@fixture
def time(localFixture, kitchenSinkSnapshot):
    return localFixture.contracts["Time"]
