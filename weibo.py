
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
from . import local_ocr
#以下调试用
from selenium import webdriver


class WeiboCookies:
    def __init__(self, username, password, browser):
        self.login_url = 'https://weibo.com/login.php'
        self.username = username
        self.password = password
        #self.browser = browser
        #调试，自建browser
        self.init_browser()
        self.wait = WebDriverWait(self.browser, 20)
        #验证码识别次数初始化
        self.check_try_times = 0

    def open(self):
        '''
        打开网页，输入密码，点击提交
        :return:
        '''
        self.browser.delete_all_cookies()
        self.browser.get(self.login_url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginname')))
        username.send_keys(self.username)
        time.sleep(0.5)
        password = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        password.send_keys(self.password)
        time.sleep(0.5)
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[action-type="btn_submit"]')))
        submit.click()
        print('click submit')


    def init_browser(self):
        '''
        初始化浏览器，供模拟登陆使用
        :return:
        '''
        chrome_options = webdriver.ChromeOptions()

        self.browser = webdriver.Chrome()
        #设置全屏，方便截屏获取验证码,无法全屏？
        #self.browser.maximize_window()

    def password_error(self):
        '''
        判断账户密码是否错误
        :return: True or False
        '''
        try:
            WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span[node-type="text"]'), '用户名或密码错误。'))
            print('账户或密码错误')
            return True
        except TimeoutException:
            return False

    def login_successfully(self):
        '''
        判断是否登陆成功
        :return: True or False
        '''
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[nm="account"]')))
            return True
        except TimeoutException:
            return False

    def need_check(self):
        '''
        判断是否需要输入验证码
        :return:
        '''
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[value="验证码"]')))
            print('需要输入验证码')
            return True
        except TimeoutException:
            return False

    def check(self):
        '''
        验证码识别主程序
        :param image:
        :return:
        '''
        self.check_try_times += 1
        image = self.get_image()
        verifycode = self.image_to_verifycode(image)

        input_code = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[action-data="text=请输入验证码"]')))
        input_code.send_keys(verifycode)
        time.sleep(5)
        submit = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[action-type="btn_submit"]')))
        time.sleep(1)
        submit.click()
        #若验证码输入错误且尝试次数小于3，重试
        if self.verifycode_error() and self.check_try_times<1:
            self.check()
        else:
            print('验证码识别失败次数过多，已尝试{}次'.format(self.check_try_times))


    def verifycode_error(self):
        '''
        验证码是否错误
        :return:
        '''
        try:
            #10秒后若验证码图片还存在，则说明验证码错误，需要重新验证
            time.sleep(10)
            error = self.browser.find_element_by_css_selector('input[action-data="text=请输入验证码"]')
            if error:
                print('输入的验证码不正确')
                return True
        except Exception as e:
            print(e.args)


    def get_image(self):
        '''
        从网页截图中截取验证码图片
        :return:
        '''
        left, top, right, bottom = self.get_position()
        #截图像素坐标和chrome坐标之间存在倍数关系和边框宽度等，需要微调
        convert_x = 2400/1200
        convert_y = 1286/766
        screenshot = self.get_screenshot()
        capture = screenshot.crop((left*convert_x-10, top*convert_y+65, right*convert_x, bottom*convert_y+90))
        return capture

    def get_position(self):
        """
        获取验证码图片坐标
        :return: 验证码坐标
        """
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[action-type="btn_change_verifycode"]')))
        except TimeoutException:
            #print('超时，未出现验证码')
            #此处可以优化
            raise TimeoutException('未发现验证码图片')
        else:
            time.sleep(1)
            location = img.location
            size = img.size
            print('loacation', location, 'size', size, 'browser', self.browser.get_window_size())
            top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
            #print(left, top, right, bottom)
            return (left, top, right, bottom)

    def get_screenshot(self):
        '''
        获取网页截图
        :return: 网页截图
        '''
        screenshot = self.browser.get_screenshot_as_png()
        #self.browser.get_screenshot_as_file('./mytest.png')
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def image_to_verifycode(self, image):
        verifycode = local_ocr.verify(image)
        if verifycode:
            print('成功生成验证码:', verifycode)
            return verifycode[:6]
        else:
            print('！！！验证码生成失败,返回默认字符串')
            return 'default'


    def main(self):

        self.open()

        if self.password_error():
            return {'status':2, 'content':'账户或密码错误'}

        if self.need_check():
            self.check()

        if self.login_successfully():
            #此处cookies是字典列表
            cookies = self.browser.get_cookies()
            print({'status':1, 'content': cookies})
            # 调试用
            time.sleep(300)
            return {'status':1, 'content': cookies}

        else:
            return {'status':3, 'content':'登陆失败'}


if __name__ == '__main__':
    result = WeiboCookies('账号', '密码', None).main()
    print(result)
