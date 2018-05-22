import requests
import os

# url = 'https://www.cnblogs.com/jiu0821/p/6275685.html'
url = 'http://dl74.80s.im:920/1610/80s测试短片/80s测试短片.mp4'

print("开始下载")
print(os.path.basename(url))

r = requests.get(url)

with open(os.path.basename(url), "wb") as code:
    code.write(r.content)

print("完成")