import requests
import json
import os
import time
import sys
from concurrent.futures import ProcessPoolExecutor


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

CSV_HEADER = "crossTxName,timeStr,isSuccess,crossTxHash,fromChainName,fromChainAddress,toChainName,toChainAddress,tokenName,amount,from_txHash,from_tokenHash,from_fromAddress,from_toAddress,to_txHash,to_tokenHash,to_fromAddress,to_toAddress"

executor = None


def getCrossTxList(page_no, page_size):
    url = "https://explorer.poly.network/api/v1/getcrosstxlist"
    data = json.dumps({"pageNo": page_no, "pageSize": page_size})
    resp = requests.post(url, headers=HEADERS, data=data)
    cross_txs = json.loads(resp.text)["crosstxs"]

    print("Current Page {}, got {}".format(i, len(cross_txs)))

    for tx in cross_txs:
        executor.submit(getDetailInfoByTxHash,
                        tx["txhash"], tx["state"], page_no)


def getDetailInfoByTxHash(tx_hash, state, page_no):
    try:
        url = "https://explorer.poly.network/api/v1/getcrosstx?txhash="+tx_hash
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp_dict = json.loads(resp.text)

        # 跨链类型名称
        crossTxName = resp_dict["crosstransfer"]["crosstxname"]
        # 跨链交易hash
        crossTxHash = tx_hash
        # 时间戳
        timestamp = resp_dict["mchaintx"]["timestamp"]
        # 时间
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        # 文件名
        fileName = timeStr[:7]
        # 是否成功
        isSuccess = "unknow"
        if state == 1:
            isSuccess = "Confirmed"
        elif state == 0:
            isSuccess = "In Progress"
        else:
            isSuccess = "Failed"

        # fromchain名称
        fromChainName = resp_dict["crosstransfer"]["fromchainname"]
        # fromchain账户地址
        fromChainAddress = resp_dict["crosstransfer"]["fromaddress"]
        # tochain名称
        toChainName = resp_dict["crosstransfer"]["tochainname"]
        # tochain账户地址
        toChainAddress = resp_dict["crosstransfer"]["toaddress"]
        # 代币名称
        tokenName = resp_dict["crosstransfer"]["tokenname"]
        # 转账金额
        amount = resp_dict["crosstransfer"]["amount"]

        # fromchain交易hash
        from_txHash = resp_dict["fchaintx"]["txhash"]
        # fromchain代币hash
        from_tokenHash = resp_dict["fchaintx"]["transfer"]["tokenhash"]
        # fromchain的发送地址
        from_fromAddress = resp_dict["fchaintx"]["transfer"]["from"]
        # fromchain的接收地址
        from_toAddress = resp_dict["fchaintx"]["transfer"]["to"]

        # tochain的交易hash
        to_txHash = resp_dict["tchaintx"]["txhash"]
        # tochain的代币hash
        to_tokenHash = resp_dict["tchaintx"]["transfer"]["tokenhash"]
        # tochain的发送地址
        to_fromAddress = resp_dict["tchaintx"]["transfer"]["from"]
        # tochain的接收地址
        to_toAddress = resp_dict["tchaintx"]["transfer"]["to"]

        writeToFile(fileName, crossTxName, timeStr, isSuccess, crossTxHash, fromChainName, fromChainAddress, toChainName, toChainAddress, tokenName, amount,
                    from_txHash, from_tokenHash, from_fromAddress, from_toAddress, to_txHash, to_tokenHash, to_fromAddress, to_toAddress)
        print("pageNo {}, writeToFile {} {} {} -> {}".format(page_no, timeStr,
              str(timestamp), fromChainName, toChainName))

    except Exception as e:
        print(e)
        return


def writeToFile(fileName, *args):
    if not os.path.exists(fileName + ".csv"):
        with open(fileName + ".csv", "w+", encoding="utf-8") as f:
            f.write(CSV_HEADER + "\n")

    with open(fileName + ".csv", "a+", encoding="utf-8") as f:
        f.write(args[0])
        for i in range(1, len(args)):
            f.write("," + args[i])
        f.write("\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("sys args error.")
        pass

    executor = ProcessPoolExecutor(max_workers=300)
    for i in range(int(sys.argv[1]), int(sys.argv[2])):
        getCrossTxList(i, 5000)

    executor.shutdown(wait=True)
    print("DONE")
