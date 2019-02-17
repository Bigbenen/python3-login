import requests
from lxml import etree

class Login:
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/'
        self.session = requests.Session()


    def token(self):
        '''请求登陆页，并获取必要的参数'''
        res = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(res.text)
        token = selector.xpath('//div//input[@name="authenticity_token"]/@value')[0]
        #print(token)
        #print(res)
        return token

    def login(self, user, password):
        '''构造参数并发起登陆请求'''
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': user,
            'password': password
        }

        res = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if res.status_code == 200:
            self.check(res.text)
        else:
            print(res.status_code)


    def check(self, html):
        '''检测是否登陆成功'''
        selector = etree.HTML(html)
        title = selector.xpath('//h2/text()')
        print(title)


if __name__ == '__main__':
    login = Login()
    login.login(user='***', password='***')
