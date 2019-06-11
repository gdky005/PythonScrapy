url = "https://mh3.xitangwenhua.com/upload/zhegedashutailengao/5312480/0000.jpg"
print(url)

url = url[0:url.rindex("/")]
id2 = url[url.rindex("/") + 1:len(url)]
print(id2)

url = url[0:url.rindex("/")]
id1 = url[url.rindex("/") + 1:len(url)]
print(id1)