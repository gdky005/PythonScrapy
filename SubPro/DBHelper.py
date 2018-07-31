# 插入数据到数据库中

from SubPro.items import SubInfoItem, SubMovieDownloadInfoItem, SubMovieLastestInfoItem


def insertSubInfoItem2DB(pid, movie_name, movie_pic, url, movie_update_time, movie_intro, movie_intro_pic):
    item = SubInfoItem()
    item['pid'] = pid
    item['name'] = movie_name
    item['pic'] = movie_pic
    item['url'] = url
    item['update_time'] = movie_update_time
    item['intro'] = movie_intro
    item['capture_pic'] = movie_intro_pic
    return item


def insertSubMovieDownloadItem2DB(pid, fj_name, fj_number, fj_download_url):
    item = SubMovieDownloadInfoItem()
    item['pid'] = pid
    item['fj_name'] = fj_name
    item['fj_number'] = fj_number
    item['fj_download_url'] = fj_download_url
    return item


def insertSubMovieLastestItem2DB(pid, fj_number):
    item = SubMovieLastestInfoItem()
    item['pid'] = pid
    item['fj_number'] = fj_number
    return item
