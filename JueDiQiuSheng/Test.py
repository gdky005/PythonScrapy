import unittest

import requests

from JueDiQiuSheng.JueDiQiuSheng import Utils


class TestCase(unittest.TestCase):
    def test_getNowTime(self):
        print("test_getNowTime: " + Utils.getCollectionTime())

    def test_getCategoryId(self):
        categoryUrl = "http://www.gamersky.com/z/playbattlegrounds/862094_64754/"
        print("test_getCategoryId: " + Utils.getCategoryId(categoryUrl))

    def test_getJid(self):
        url = "http://www.gamersky.com/handbook/201706/919363-67.shtml"
        print("test_getJid: " + Utils.getJid(url))

    def test_addList(self):
        l1 = [1, 2, 3]
        l2 = [4, 5, 6]

        l1 += l2

        for a in l1:
            print(a)

    def test_request(self):
        content = requests.get('http://zkteam.cc/JueDiQiuSheng/json')

        json = content.json()

        print(json["result"][0]["artifactSourceUrl"])

        print(json)



