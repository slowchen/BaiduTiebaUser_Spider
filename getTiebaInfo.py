#!/usr/bin/env python
#coding=utf-8
__author__ = 'chengj'

# 贴吧ID : 流雨清扬
# Q   Q :  644209001
# 爬取百度贴吧用户数据


import requests
import time
import re
import xlrd
import xlutils.copy
from bs4 import BeautifulSoup

def get_soup(url):
    wb_data = requests.get(url)
    soup = str(BeautifulSoup(wb_data.text,'lxml'))
    return soup

def get_info(n,soup):

    print(time.strftime("\n%Y-%m-%d %H:%M:%S"))
    print('第 %s 页' % i)
    print('rank|' 'name|' 'sex|' 'level|' 'age|' 'exp|' 'notes|' 'gift|' 'fans|' 'favorite|''status|''home')

    # 获取贴吧排名
    tieba_ranks_top = re.compile(r'<p class="drl_item_index_(\d)">', re.S)
    tieba_ranks_nor = re.compile(r'<p class="drl_item_index_nor">(.*?)</p>', re.S)
    ranks_top = re.findall(tieba_ranks_top, soup)
    rank_nor = re.findall(tieba_ranks_nor, soup)
    ranks = ranks_top + rank_nor
    # print(ranks)

    # 获取贴吧ID
    tieba_usernames = re.compile(r'username="(.*?)</a></div></td><td class="drl_item_title">', re.S)
    tieba_names = re.findall(tieba_usernames, soup)
    # print(tieba_names)

    # 获取贴吧等级
    tieba_levels = re.compile(r'<div class="bg_lv(.*?)">', re.S)
    levels = re.findall(tieba_levels, soup)
    # print(levels)

    # 获取经验值
    tieba_exps = re.compile(r'"drl_item_exp"><span>(.*?)</span>', re.S)
    exps = re.findall(tieba_exps, soup)
    # print(exps)

    # 获取排名变化状态
    rank_status = re.compile(r'<td class="drl_item_status"><img src="(.*?)" title=""/>', re.S)
    status = re.findall(rank_status, soup)
    # print(status)

    # 获取用户个人中间编码
    home_pages = re.compile(r'target="_blank" username="(.*?)">', re.S)
    home_page = re.findall(home_pages, soup)
    # print(home_page)

    for rank,names,level,exp,statu,page in zip (ranks,tieba_names,levels,exps,status,home_page):
        # print(page)

        #获取个人主页
        herfs = 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank'
        # print(herfs)
        new_soup = get_soup(herfs)

        #获取性别
        user_sexs = re.compile(r'<span class="userinfo_sex userinfo_sex_(.*?)">',re.S)
        sexs = re.findall(user_sexs,new_soup)
        # print(sexs)

        #获取吧龄
        tieba_ages = re.compile(r'<span>吧龄:(.*?)</span>',re.S)
        ages = re.findall(tieba_ages,new_soup)
        # print(ages)

        #获取发帖数
        tieba_notes = re.compile(r'<span>发贴:(.*?)</span>', re.S)
        notes = re.findall(tieba_notes, new_soup)
        # print(notes)

        #获取礼物数
        tieba_gifts = re.compile(r'<i>(.*?)</i>',re.S)
        gifts = re.findall(tieba_gifts,new_soup)
        # print(gifts)

        #获取关注数
        user_favorites = re.compile(r'<a href="/home/concern(.*?)</a>', re.S)
        favorites = re.findall(user_favorites, new_soup)
        if len(favorites) == 1:
            favorite = favorites[0].split(r'>')[-1]
            # print(favorite)
        elif len(favorites) == 0:
            favorite = '0'
            # print(favorite)

        #获取粉丝数
        user_fans = re.compile(r'<a href="/home/fans(.*?)</a>', re.S)
        fans_num = re.findall(user_fans, new_soup)
        if len(fans_num) == 1:
            fans = fans_num[0].split(r'>')[-1]
            # print(fans)
        elif len(fans_num) == 0:
            fans = '0'
            # print(fans)

        for sex,age,note,gift in zip (sexs,ages,notes,gifts):
            name = names.split(r'>')[1]

            path1 = 'F:\\TIEBA\\User'
            path2 = '\\%s' % rank
            path3 = '_%s' % level
            path4 = '_%s.txt' % name
            info = open(str(path1 + path2 + path3 + path4), 'w')

            if statu == 'http://static.tieba.baidu.com/tb/static-member/img/furank_num_0.png':
                print(rank, name, sex , level, age , exp , note , gift, fans,favorite,'不变', 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.write(
                    '贴吧昵称 : ' + name + '\n''贴吧排名 : ' + rank + '\n''贴吧性别 : ' + sex + '\n''贴吧年龄 : ' + age + '\n''发帖总数 : ' + note + '\n''关 注 数 : '+favorite+'\n''粉 丝 数 : '+fans+'\n''TA的礼物 : ' + gift + '\n''贴吧等级 : ' + level + '\n''经 验 值 : ' + exp + '\n''排名变化 : ' + '不变' + '\n' + '个人主页 : ' + 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.close()

            elif statu == 'http://static.tieba.baidu.com/tb/static-member/img/furank_num_1.png':
                print(rank, name, sex , level, age , exp , note , gift, fans,favorite,'升高', 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.write(
                    '贴吧昵称 : ' + name + '\n''贴吧排名 : ' + rank + '\n''贴吧性别 : ' + sex + '\n''贴吧年龄 : ' + age + '\n''发帖总数 : ' + note + '\n''关 注 数 : '+favorite+'\n''粉 丝 数 : '+fans+'\n''TA的礼物 : ' + gift + '\n''贴吧等级 : ' + level + '\n''经 验 值 : ' + exp + '\n''排名变化 : ' + '升高' + '\n' + '个人主页 : ' + 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.close()
            elif statu == 'http://static.tieba.baidu.com/tb/static-member/img/furank_num_2.png':
                print(rank, name, sex , level, age , exp , note , gift, fans,favorite,'降低', 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.write(
                    '贴吧昵称 : ' + name + '\n''贴吧排名 : ' + rank + '\n''贴吧性别 : ' + sex + '\n''贴吧年龄 : ' + age + '\n''发帖总数 : ' + note + '\n''关 注 数 : '+favorite+'\n''粉 丝 数 : '+fans+'\n''TA的礼物 : ' + gift + '\n''贴吧等级 : ' + level + '\n''经 验 值 : ' + exp + '\n''排名变化 : ' + '降低' + '\n' + '个人主页 : ' + 'http://tieba.baidu.com/home/main/?un=' + page + '&fr=furank')
                info.close()

            # #打开excel，将数据保存在excel中
            oldexcel = xlrd.open_workbook('F:/tiebainfo2.xls')
            newexcel = xlutils.copy.copy(oldexcel)
            sheet = newexcel.get_sheet(0)
            # 设置变量n，n为行数
            sheet.write(n, 0, rank)
            sheet.write(n, 1, name)
            sheet.write(n, 2, sex)
            sheet.write(n, 3, age)
            sheet.write(n, 4, note)
            sheet.write(n, 5, level)
            sheet.write(n, 6, exp)
            sheet.write(n, 7, gift)
            sheet.write(n, 8, fans)
            sheet.write(n, 9, favorite)
            sheet.write(n, 10, herfs)
            newexcel.save('F:/tiebainfo2.xls')
            n = n + 1
n=1
for i in range(1,2269) :
    url = 'http://tieba.baidu.com/f/like/furank?kw=%CE%E4%BA%BA%C8%ED%BC%FE%B9%A4%B3%CC%D6%B0%D2%B5%D1%A7%D4%BA&pn={}'.format(i)
    soup = get_soup(url)
    get_info(n,soup)
    n = n+20
