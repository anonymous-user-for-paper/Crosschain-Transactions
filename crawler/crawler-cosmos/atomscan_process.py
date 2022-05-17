from bs4 import BeautifulSoup
import requests as re
import json
import os
import warnings
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
import multiprocessing
import time
warnings.filterwarnings("ignore")
def cosmos(thread,start,end):
    now = 8885879
    lowest = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
    print("线程"+thread,"开始时间",start,"结束快",end)
    height = start
    block_path_root = r"https://cosmos.node.cracklord.com/txs?tx.height="
    cosmoshub = ""
    tx_path_root = "https://cosmos.node.cracklord.com/txs?page=1&limit=100&tx.hash="
    #https://cosmos.node.cracklord.com/txs?page=1&limit=100&tx.hash=8063770D244DDB3897ED581A0EEF4E79F70CD2C72542D4F3E2DD268C5B640400
    save_path = "data/all"
    while(True):
        if height > now or height > end:
            break


        try:
            block_path = block_path_root+str(height)
            r = re.get(block_path,verify=False,headers=headers,timeout=10)
            j = json.loads(r.text)
            tx_list = j["txs"]
            id_list = 0
            for tx in tx_list:
                tx_path = tx_path_root+str(tx["txhash"])
                r = re.get(tx_path,verify=False,headers=headers,timeout=10)
                tx_json = json.loads(r.text)
                path = save_path+"/"+str(tx_json["txs"][0]["height"])+"_"+str(id_list)+".json"
                id_list = id_list+1
                if os.path.isfile(path):
                    os.remove(path)
                    print("重复删除")
                with open(path, 'w', encoding='utf-8') as fObj:
                    json.dump(tx_json, fObj, ensure_ascii=False)
                print("save:   "+path)
        except Exception as e:
            print("错误",e)
            if(str(type(e))=="<class 'requests.exceptions.ReadTimeout'>"):
                height = height-1
                print("重置高度")
        print("线程"+thread,"高度",height)
        # time.sleep(2)
        height = height+1

        # t.append(threading.Thread(target=cosmos, args=("Thread"+str(i), int((now-lowest)/thread_num*i+lowest,),int((now-lowest)/thread_num*(i+1)+lowest,))))
        # _thread.start_new_thread(polk_threat, ("Thread"+str(i), now/20*i,))
        # t[i].start()
if __name__ == '__main__':
    now = 8885879
    lowest = 0
    count = now-lowest
    task = []
    thread_num = 7
    print("输入合适的进程,默认为7")
    thread_num=int(input())
    print("请输入你的编号：(1-8)")
    number = int(input())
    end = now/8*number+lowest
    start = now/8*(number-1)+lowest
    # executor = ProcessPoolExecutor(max_workers=10)
    # executor.map(cosmos)
    for i in range(0, thread_num):


        # executor.submit(cosmos, ("Thread" + str(i), int((now - lowest) / thread_num * i + lowest, ),
        #                          int((now - lowest) / thread_num * (i + 1) + lowest)))
        process = multiprocessing.Process(target=cosmos, args=("Thread"+str(i), int((end-start)/thread_num*i+start,),int((end-start)/thread_num*(i+1)+start,)))
        process.start()