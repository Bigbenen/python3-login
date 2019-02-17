# python3-login
#### 目标
>深入理解网站登陆请求过程，采用构造（post）请求参数的方式实现登陆github主页。

#### 总结
* 采用构造请求参数的方式可行，除了requests.session，scrapy的cookiejar同样可以实现对cookie的管理
* 当请求参数比较难构造，或需要其他验证（如验证码识别）时，可以采用可视化工具进行登陆，如selenium/splash
