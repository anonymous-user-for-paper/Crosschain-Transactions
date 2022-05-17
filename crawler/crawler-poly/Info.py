import numpy as np
import pandas as pd
import os
import json
from tqdm import tqdm
import time


def loadDataset():
    dfs = []
    for f in os.listdir("clean"):
        df = pd.read_csv("clean/" + f, error_bad_lines=False)
        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)
    print("Data size: {}".format(data.shape[0]))
    return data


def getPlatformInfo():
    df = loadDataset()
    # chainPlatforms = np.unique(np.concatenate((df["fromChainName"].values, df["toChainName"].values)))
    outChainInfo = {}
    inChainInfo = {}
    netChainInfo = {}

    for fcn, tcn, tn, am in list(zip(df["fromChainName"], df["toChainName"], df["tokenName"], df["amount"])):
        # print("fromchain:{}, tochain:{}, token:{}, amount:{}".format(fcn, tcn, tn, am))

        if fcn not in outChainInfo:
            outChainInfo[fcn] = {}
        if tcn not in outChainInfo[fcn]:
            outChainInfo[fcn][tcn] = {}
        if tn not in outChainInfo[fcn][tcn]:
            outChainInfo[fcn][tcn][tn] = 0
        outChainInfo[fcn][tcn][tn] += float(am)

        if "0total" not in outChainInfo[fcn]:
            outChainInfo[fcn]["0total"] = {}
        if tn not in outChainInfo[fcn]["0total"]:
            outChainInfo[fcn]["0total"][tn] = 0
        outChainInfo[fcn]["0total"][tn] += float(am)

        if tcn not in inChainInfo:
            inChainInfo[tcn] = {}
        if fcn not in inChainInfo[tcn]:
            inChainInfo[tcn][fcn] = {}
        if tn not in inChainInfo[tcn][fcn]:
            inChainInfo[tcn][fcn][tn] = 0
        inChainInfo[tcn][fcn][tn] += float(am)

        if "0total" not in inChainInfo[tcn]:
            inChainInfo[tcn]["0total"] = {}
        if tn not in inChainInfo[tcn]["0total"]:
            inChainInfo[tcn]["0total"][tn] = 0
        inChainInfo[tcn]["0total"][tn] += float(am)

        if fcn not in netChainInfo:
            netChainInfo[fcn] = {}
        if tcn not in netChainInfo[fcn]:
            netChainInfo[fcn][tcn] = {}
        if tn not in netChainInfo[fcn][tcn]:
            netChainInfo[fcn][tcn][tn] = 0
        netChainInfo[fcn][tcn][tn] -= float(am)

        if "0total" not in netChainInfo[fcn]:
            netChainInfo[fcn]["0total"] = {}
        if tn not in netChainInfo[fcn]["0total"]:
            netChainInfo[fcn]["0total"][tn] = 0
        netChainInfo[fcn]["0total"][tn] -= float(am)

        if tcn not in netChainInfo:
            netChainInfo[tcn] = {}
        if fcn not in netChainInfo[tcn]:
            netChainInfo[tcn][fcn] = {}
        if tn not in netChainInfo[tcn][fcn]:
            netChainInfo[tcn][fcn][tn] = 0
        netChainInfo[tcn][fcn][tn] += float(am)

        if "0total" not in netChainInfo[tcn]:
            netChainInfo[tcn]["0total"] = {}
        if tn not in netChainInfo[tcn]["0total"]:
            netChainInfo[tcn]["0total"][tn] = 0
        netChainInfo[tcn]["0total"][tn] += float(am)

    json.dump(outChainInfo, open("info/outChainInfo.json", "w", encoding="utf-8"),
              sort_keys=True, indent=2)
    json.dump(inChainInfo, open("info/inChainInfo.json", "w", encoding="utf-8"),
              sort_keys=True, indent=2)
    json.dump(netChainInfo, open("info/netChainInfo.json", "w", encoding="utf-8"),
              sort_keys=True, indent=2)


if __name__ == '__main__':
    getPlatformInfo()
