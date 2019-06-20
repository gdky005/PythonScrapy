import requests

proxies = {'https': 'https://113.121.20.170:9999'}
# proxies = {'https': 'http://112.85.131.145:9999'}
# proxies = {'http': 'http://113.124.85.183:9999'}
# proxies = {'http': 'http://112.85.167.219:9999'}

res = requests.get("http://httpbin.org/get", proxies=proxies)

print(res.text)