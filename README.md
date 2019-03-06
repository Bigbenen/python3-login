# python3-login
#### 目标
>深入理解网站登陆请求过程，采用构造（post）请求参数的方式实现登陆github主页。

>采用selenium模仿登陆微博主页。

#### 总结
* 采用构造请求参数的方式可行，除了requests.session，scrapy的cookiejar同样可以实现对cookie的管理。
* 当请求参数比较难构造（如淘宝、京东、微博），或需要其他验证（如验证码识别）时，可以采用selenium结合ocr技术或云打码平台来模仿登陆。
