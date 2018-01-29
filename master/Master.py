from func import get_url, make_redis_handler
from lxml import etree
from config import settings, r_server
from multiprocessing import Pool


class Master(object):

    def __init__(self):
        self.index_url = 'http://bbs.kaoyan.com/'
        # 论坛版块字典, key为版块名字, value为url
        self.raw_block_url = dict()

    def get_block_url(self):
        '''
        获取论坛版块url
        '''
        print('获取版块url')
        resp = get_url(self.index_url)
        html = etree.HTML(resp.content.decode())
        a_tags = html.xpath('//*[@id="category_173"]/table/tr[1]/td[position()<5]//a')
        for a in a_tags:
            print(a.text)
            self.raw_block_url[a.text] = a.attrib['href'][:-1]

    def save_url(self, values):
        print('保存{}到redis'.format(*values))
        make_redis_handler().sadd(r_server['s_url'], *values)

    def delivery_post_url_by_block(self, raw_url):
        print('往redis中推送帖子url')
        for i in range(0, settings['b_pages']):
            made_url = raw_url + str(i+1)
            resp = get_url(made_url)
            html = etree.HTML(resp.content.decode())
            # 只记录符合阅读大于read，回复大于reply的
            raw_path = "//td[@class='num']/em[text()>{read_num}]/../a[text()>{reply_num}]/@href"
            made_path = raw_path.format(read_num=settings['read'], reply_num=settings['reply'])
            filtered_url_list = html.xpath(made_path)
            if len(filtered_url_list) < 1:
                print('Error: No data.@<delivery_post_url_by_block>:' + made_url)
                return
            self.save_url(filtered_url_list)

    def delivery_post_url(self):
        print('开始按版块多进程爬取帖子')
        # 使用多进程启动
        p = Pool(5)
        for url in self.raw_block_url.values():
            p.apply_async(self.delivery_post_url_by_block, args=(url,))
        p.close()
        p.join()

    def start(self):
        make_redis_handler().delete(r_server['s_url'])

        # 获取论坛版块url
        self.get_block_url()

        # 往redis推送帖子
        self.delivery_post_url()

if __name__ == "__main__":
    Master().start()
    # MasterDemo().get_block_url()