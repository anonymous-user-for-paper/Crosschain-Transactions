import requests as re
import json
import threading
import os
import time
from requests import RequestException
def thor(thread,start,end):
    proxyHost = "ip"
    proxyPort = "port"
    proxyMeta = "http://%(host)s:%(port)s" % {

        "host": proxyHost,
        "port": proxyPort,
    }
    root_path = "https://api.viewblock.io/thorchain/txs?page="
    page =start
    now= 17000
    while (True):
        proxy = get_proxy().get("proxy")
        # print("目前代理",proxy)
        if page > now or page > end:
            break
        try:
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","Origin":"https://viewblock.io","Referer":"https://viewblock.io/"}
            if(thread == "Thread0"):
                print("目前线程",thread,"开始",start,"目标",end,"---目前page",page)
            url = root_path+str(page)+"&network=chaosnet&type=swap"
            a = re.get(root_path+str(page)+"&network=chaosnet&type=swap",headers=headers,proxies={"https": "http://{}".format(proxy),"http": "http://{}".format(proxy)},timeout = 5)
            a_json = json.loads(a.text)
            txs = a_json["docs"]
            for i in txs:
                save_path = "data/" + i["hash"]
                for j in i["extra"]["events"]:
                    save_path=save_path+"_"+j["name"]
                save_path = save_path+".json"
                if os.path.isfile(save_path):
                    print("重复删除")
                    # page=page+1
                    break
                with open(save_path, 'w', encoding='utf-8') as fObj:
                    json.dump(i, fObj, ensure_ascii=False)
                # print("save:   " + save_path)
            page = page+1
            print("page+1")

        except:
            # print("错误",r)
            print("删除代理",proxy)
            delete_proxy(proxy)


if __name__ == '__main__':
    t = []
    thread_num = 40
    for i in range(0, thread_num):
        now = 16978
        lowest = 7061
        t.append(threading.Thread(target=thor, args=(
        "Thread" + str(i), int((now - lowest) / thread_num * i, ) + lowest, int((now - lowest) / thread_num * (i + 1) + lowest, ))))
        # _thread.start_new_thread(polk_threat, ("Thread"+str(i), now/20*i,))
        t[i].start()