from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ProcessPoolExecutor

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

CSV_HEADER = "isSuccess,timeago,lockHash,fromChainName,fromChainAddress,toChainName,toChainAddress,amountType,amount"

session = HTMLSession()

executor = ProcessPoolExecutor(max_workers=1)


def getTxList(i, url):
    content = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(content.content, 'lxml')

    chainnames = soup.find_all("span", class_="crosschain_chainName")
    if len(chainnames) != 2:
        raise Exception("len(chainnames) != 2")
    filename = chainnames[0].text + "-" + chainnames[1].text

    page = soup.find('a', class_='lastBtn')
    page = page.attrs["href"]
    if "p=" in page:
        page = int(page[page.find("p=")+2:])
    else:
        page = 1

    if not os.path.exists("output/" + filename + ".csv"):
        with open("output/" + filename + ".csv", "w+", encoding="utf-8") as f:
            f.write(CSV_HEADER + "\n")

    for p in range(1, page+1):
        _url = url + "?p=" + str(p)
        executor.submit(_getTxList, i, "{}/{}".format(p, page), filename, _url)


def _getTxList(i, j, filename, url):
    content = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(content.content, 'lxml')

    tbody = soup.find_all("tbody")[0]
    trs = tbody.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 0:
            continue

        lockHash = tds[1].text

        timeago = tds[2].text

        fromChainRaw = tds[3].text
        fromChainName = fromChainRaw[
            fromChainRaw.find("(")+1:fromChainRaw.find(")")
        ]
        fromChainAddress = fromChainRaw[
            fromChainRaw.find(")")+2:
        ]

        toChainRaw = tds[4].text
        toChainName = toChainRaw[
            toChainRaw.find("(")+1:toChainRaw.find(")")
        ]
        toChainAddress = toChainRaw[
            toChainRaw.find(")")+2:
        ]

        isSuccess = tds[5].text

        amountRaw = tds[6].text
        amountType = amountRaw[
            amountRaw.find(" ")+1:
        ]
        amount = amountRaw[
            :amountRaw.find(" ")
        ].replace(",", "")

        writeToFile(filename, isSuccess, timeago, lockHash, fromChainName, fromChainAddress,
                    toChainName, toChainAddress, amountType, amount)
    print("writeToFile url {} page {} {}".format(i, j, filename))


def writeToFile(fileName, *args):
    with open("output/" + fileName + ".csv", "a+", encoding="utf-8") as f:
        f.write(args[0])
        for i in range(1, len(args)):
            f.write("," + args[i])
        f.write("\n")


if __name__ == '__main__':
    url = "https://www.wanscan.org/crosschain"

    content = session.get(url, headers=HEADERS)
    urls = [url for url in content.html.absolute_links
            if "www.wanscan.org/crosschain/" in url]

    for url in urls:
        getTxList("{}/{}".format(urls.index(url)+1, len(urls)), url)
