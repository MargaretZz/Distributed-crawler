from requests.api import request
from requests.exceptions import ProxyError
import redis
from config import headers, settings, r_server

def make_redis_handler():
    pool = redis.ConnectionPool(host=r_server['ip'], port=r_server['port'], password=r_server['password'])
    return redis.Redis(connection_pool=pool)

def get_url(url):
    headers['Referer'] = url
    while True:
        try:
            resp = request('get', url, headers=headers)
            return resp
        except ProxyError:
            continue

if __name__ == '__main__':
    print(get_url('http://bbs.kaoyan.com'))