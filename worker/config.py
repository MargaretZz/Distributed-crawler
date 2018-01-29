headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Referer': ''
}

r_server = {
    'ip': '39.108.77.137',
    'port': '6379',
    'password': 'xun',
    's_url': 'url'
}

# settings for connecting database
d_server = {
    'user': 'root',
    'password': 'root',
    'addr': 'localhost'
}

settings = {
    'p_pages': 4,
    # 使用代理时最大尝试次数
    'maxtries': 3,
    # 每个版块遍历的页数
    'b_pages': 5,
    # 合格的回复下限
    'reply': 45,
    # 合格的阅读下限
    'read': 10000
}

filters = {
    # 文本最少字符数
    'txt-len': 100,
    # 允许楼主在第一页最大回复数 re-max/10
    're-max': 5
}
