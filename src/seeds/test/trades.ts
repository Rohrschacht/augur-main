import * as Knex from "knex";

exports.seed = async (knex: Knex): Promise<any> => {
  // Deletes ALL existing entries
  return knex("trades").del().then(async (): Promise<any> => {
    // Inserts seed entries
    const seedData = [{
      orderID: "0x1100000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000001",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C00",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1200000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000002",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C01",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1300000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000003",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C02",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1400000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000011",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C03",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1500000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000012",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400052,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C04",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1600000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000013",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "sell",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C05",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1700000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000014",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "buy",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C06",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }, {
      orderID: "0x1800000000000000000000000000000000000000000000000000000000000000",
      marketID: "0x0000000000000000000000000000000000000015",
      outcome: 0,
      shareToken: "0x1000000000000000000000000000000000000000",
      orderType: "buy",
      creator: "0x0000000000000000000000000000000000000b0b",
      filler: "0x000000000000000000000000000000000000d00d",
      blockNumber: 1400051,
      transactionHash: "0x0000000000000000000000000000000000000000000000000000000000000C07",
      logIndex: 0,
      numCreatorTokens: "0",
      numCreatorShares: "0.2",
      numFillerTokens: "1.1",
      numFillerShares: "0",
      price: "5.5",
      amount: "0.2",
      marketCreatorFees: "0",
      reporterFees: "0",
    }];
    return knex.batchInsert("trades", seedData, seedData.length);
  });
};
