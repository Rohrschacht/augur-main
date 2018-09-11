import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import { createBigNumber } from "utils/create-big-number";

import { selectMarket } from "modules/markets/selectors/market";
import MarketTrading from "modules/trading/components/trading/trading";
import { clearTradeInProgress } from "modules/trades/actions/update-trades-in-progress";

const mapStateToProps = state => ({
  availableFunds: createBigNumber(state.loginAccount.eth || 0),
  isLogged: state.isLogged,
  isMobile: state.appStatus.isMobile
});

const mapDispatchToProps = dispatch => ({
  clearTradeInProgress: marketId => dispatch(clearTradeInProgress(marketId))
});

const mergeProps = (sP, dP, oP) => {
  const market = selectMarket(oP.marketId);

  return {
    ...sP,
    ...dP,
    ...oP,
    market
  };
};

const MarketTradingContainer = withRouter(
  connect(
    mapStateToProps,
    mapDispatchToProps,
    mergeProps
  )(MarketTrading)
);

export default MarketTradingContainer;
