#coding=utf-8
#Author:Leonsec
#Mail:leonsec@163.com
#Date:2021年1月14日 3:01:50

import requests
import sys
import json
import time

def upload_file():
    if len(sys.argv) > 1 | len(sys.argv) == 0:
        print("Params error!")
        print("Usage: python3 webdir.py /filepath or C:\filepath")
        exit()
    else:
        path = sys.argv[1]
    url = "https://scanner.baidu.com/enqueue"
    try:
        archive = open(path, 'rb')
    except IOError:
        print(path,"is not found or you don't have permission to access this file!")
        exit()
    files = {'archive': archive}
    try:
        r = requests.post(url, files=files)
    except:
        print("Upload file error!")
        exit()
    return r.text

def parse(json_str):
    data = json.loads(json_str)
    return data

def apijson(json_str):
    data = parse(json_str)
    if data['status'] == 0:
        url = data['url']
    else:
        print(data['descr'])
        exit()
    return url

def result(url):
    while 1:
        try:
            r = requests.get(url)
            time.sleep(0.5)
            data = parse(r.text)
            if data[0]['total'] == 0 & data[0]['scanned'] == 0:
                continue
            if data[0]['scanned'] < data[0]['total']:
                total = data[0]['total']
                scanned = data[0]['scanned']
                msg = str(scanned)+'/'+str(total)
                print(msg)
            if data[0]['scanned'] == data[0]['total'] & data[0]['total'] != 0:
                print("--------------------")
                print("Scan result url:",url)
                print("Total file:",data[0]['total'])
                print("Webshell detected:",data[0]['detected'])
                print("--------------------")
                for i in range(0,data[0]['total']):
                    if data[0]['data'][i]['descr'] == None:
                        continue
                    print(data[0]['data'][i]['path'],"--",data[0]['data'][i]['descr'])
                break
        except:
            print("Try get result error!")
            exit()


if __name__ == '__main__':
    api_response = upload_file()
    url = apijson(api_response)
    result(url)