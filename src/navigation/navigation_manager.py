#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站导航模块
"""

import webbrowser


class NavItem:
    """导航项类"""
    
    def __init__(self, name, url, description=""):
        self.name = name
        self.url = url
        self.description = description


class NavigationManager:
    """导航管理器"""
    
    def __init__(self):
        self.nav_items = []
        self.init_nav_items()
    
    def init_nav_items(self):
        """初始化导航项"""
        self.nav_items = [
            # 社交媒体
            NavItem("微信网页版", "https://wx.qq.com/", "微信网页版，无需安装客户端即可使用微信"),
            NavItem("QQ网页版", "https://im.qq.com/", "QQ网页版，无需安装客户端即可使用QQ"),
            NavItem("哔哩哔哩", "https://www.bilibili.com/", "哔哩哔哩，国内知名的视频弹幕网站"),
            NavItem("小红书", "https://www.xiaohongshu.com/", "小红书，生活方式分享平台"),
            NavItem("快手", "https://www.kuaishou.com/", "快手，短视频分享平台"),
            NavItem("抖音", "https://www.douyin.com/", "抖音，短视频分享平台"),
            
            # 官方下载
            NavItem("微信官方下载", "https://pc.weixin.qq.com/", "微信官方下载网站，获取最新版微信"),
            NavItem("QQ官方下载", "https://im.qq.com/pcqq/", "QQ官方下载网站，获取最新版QQ"),
            NavItem("火绒安全", "https://www.huorong.cn/", "火绒安全官方网站，提供安全软件下载"),
            NavItem("FirPE", "https://www.firpe.cn/", "FirPE官方网站，Windows PE工具"),
            
            # 搜索引擎
            NavItem("百度", "https://www.baidu.com/", "百度搜索引擎，国内最大的搜索引擎"),
            NavItem("谷歌", "https://www.google.com/", "谷歌搜索引擎，全球最大的搜索引擎"),
            
            # 知识社区
            NavItem("GitHub", "https://github.com/", "GitHub，全球最大的代码托管平台"),
            NavItem("知乎", "https://www.zhihu.com/", "知乎，知识问答社区"),
            
            # 美化资源
            NavItem("致美化", "https://zhutix.com/", "致美化官方网站，提供桌面美化资源"),
            NavItem("枫の主题社", "https://winmoes.com/", "枫の主题社，二次元技术研究社区，提供电脑美化资源"),
            
            # 科技资讯
            NavItem("IT之家", "https://www.ithome.com/", "IT之家，科技资讯网站"),
            NavItem("电手", "https://www.4hou.com/", "电手，科技资讯和教程网站"),
            
            # 其他常用网站
            NavItem("淘宝", "https://www.taobao.com/", "淘宝，国内最大的电子商务平台"),
            NavItem("京东", "https://www.jd.com/", "京东，国内知名的电子商务平台"),
            NavItem("网易", "https://www.163.com/", "网易，国内知名的互联网公司"),
            NavItem("新浪", "https://www.sina.com.cn/", "新浪，国内知名的互联网公司"),
            NavItem("网易云音乐", "https://music.163.com/", "网易云音乐，在线音乐平台"),
            NavItem("豆瓣", "https://www.douban.com/", "豆瓣，文化社区和评论网站"),
            NavItem("吾爱破解", "https://www.52pojie.cn/", "吾爱破解，软件破解和技术交流论坛")
        ]
    
    def get_nav_items(self):
        """获取导航项"""
        return self.nav_items
    
    def open_url(self, url):
        """打开URL"""
        webbrowser.open(url)
    
    def add_nav_item(self, name, url):
        """添加导航项"""
        self.nav_items.append(NavItem(name, url))
    
    def remove_nav_item(self, name):
        """移除导航项"""
        self.nav_items = [item for item in self.nav_items if item.name != name]
