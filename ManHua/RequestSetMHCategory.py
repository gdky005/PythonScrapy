import json
import os
import time
from datetime import datetime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

page = 6
pageCount = 2000

manhuaDetailPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhuaPic/"
myUrl = "http://zkteam.cc/ManHua/setJsonCategoryForIdData"

# save_dir_name = str((page - 1) * pageCount) + "-" + str(page * pageCount)
save_dir_name = str((page - 1) * pageCount) + "-" + str(page * pageCount)
save_dir = manhuaDetailPath + save_dir_name

isExists = os.path.exists(save_dir)
if not isExists:
    os.makedirs(save_dir)


def getFile1(url1, header):
    return getFile(url1, header, None, 0)


def getFile(url1, header, proxies1, id):
    try:
        if proxies1 is None:
            res = requests.get(url1, headers=header, timeout=5, verify=False)
        else:
            res = requests.get(url1, headers=header, timeout=5, proxies=proxies1, verify=False)

        if 200 == res.status_code:
            content = res.content.decode("utf-8")

            # print(content)

            url2 = url1[0: len(url1) - 1]

            idStr = str(id)
            id = idStr.zfill(5)
            fileName = id + "_" + url1[url2.rindex("/") + 1: len(url1) - 1]

            print("获取文件内容成功，准备写入到文件中：" + fileName)

            fileObject = open(save_dir + "/" + fileName, 'w+')
            # fileObject = open("/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhuaDetail/" + fileName, 'w+')
            fileObject.write(content + "\n")
            fileObject.close()
            return 1
        else:
            return 0
    except:
        print("超时")
        return 0


def getJson(ipListPath):
    try:
        global text
        f = open(ipListPath)
        data = f.read()
        text = json.loads(data)
        return text
    except:
        pass

    return None


ipListPath1 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_nima.txt"
ipListPath2 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_xici.txt"
ipListPath3 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/new_detail_avilable_ip.txt"
json1 = getJson(ipListPath1)
json2 = getJson(ipListPath2)
json3 = getJson(ipListPath3)

jsonList = []

if json3 is not None:
    for obj in json1:
        jsonList.append(obj)
else:
    for obj in json1:
        jsonList.append(obj)

    for obj in json2:
        jsonList.append(obj)

print(jsonList.__len__())


def getStr(data):
    return str(len(data))


def getFormatTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    formatTime1 = "%02d:%02d:%02d" % (h, m, s)
    # print()
    return formatTime1


# 字符类型的时间
# timeStr = '2013-10-10 23:40:00'
def getTimeStamp(timeStr):
    # 转为时间数组
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))  # # 1381419600
    # print(timeStr + " ---> ")
    # print(timeStamp)
    return timeStamp


jsonListNew = jsonList


def showCurrentTime(msg):
    now_time = datetime.now()
    time_str = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    print(msg + ": " + time_str)
    return time_str


def getCurrentTime():
    now_time = datetime.now()
    time_str = datetime.strftime(now_time, '%Y_%m_%d_%H_%M_%S')
    return time_str


start_time = showCurrentTime("当前任务开始时间")


# 网络层
urlSource = "http://zkteam.cc/ManHua/jsonMHAllDetailView?page=" + str(page) + "&pageCount=" + str(pageCount)

res = requests.get(urlSource)
resultList = res.json()['result']

showCurrentTime("从服务器获取数据成功，开始处理")

postData = []

index = 0
for data in resultList:
    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    showCurrentTime("处理任务中")
    print("当前 index ---> " + str(index) + "/" + str(pageCount) + ", "
          + str((page - 1) * pageCount + index) + "/" + str(page * pageCount))

    postData.append({
        "mid": data['mid'],
        "cid": data['categoryIdList']})

data_json = json.dumps(postData)

code = requests.post(myUrl, data=data_json)
showCurrentTime("处理任务:" + str(code))

showCurrentTime("处理任务全部完成")


end_time = showCurrentTime("整个流程全部处理完成")


print("\n\n\n 任务 开始 时间：" + start_time)
print("\n 任务 结束 时间：" + end_time + "\n\n\n")

diffTime = getTimeStamp(end_time) - getTimeStamp(start_time)
print("\n总共耗时: " + str(diffTime) + "秒")
print("\n总共耗时: " + getFormatTime(diffTime))







