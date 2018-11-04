# SFacg-Book
这是一个sf轻小说的爬虫。

这需要用Python2进行import

这个py里有几个函数：

sf(url,cookie)

用于获取sf轻小说的文本(vip章节使用讯飞OCR进行识图)

sfnv(url)

用于获取sf轻小说的免费章节

sfvip(url,cookie)

用于获取sf轻小说的收费章节(需要cookie）

sfnext(url)

用于获取本章的下一章链接

sflast(url)

用于获取本章的上一章链接

本脚本需要讯飞开放平台的识图API

appid和APIkey在讯飞开放平台获取"https://www.xfyun.cn/services/printed-word-recognition"

appid和APIkey在88和89行配置
