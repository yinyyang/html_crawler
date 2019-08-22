#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
#     'tutorial.randomproxy.RandomProxy': 100,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#     'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#     'tutorial.spiders.rotate_useragent.RotateUserAgentMiddleware': 400,
# }
#
# # Proxy list containing entries like
# # http://host1:port
# # http://username:password@host2:port
# # http://host3:port
# # ...
# PROXY_LIST = 'list.txt'
#
# # Proxy mode
# # 0 = Every requests have different proxy
# # 1 = Take only one proxy from the list and assign it to every requests
# # 2 = Put a custom proxy to use in the settings
# PROXY_MODE = 0
#
# # If proxy mode is 2 uncomment this sentence :
# #CUSTOM_PROXY = "http://host1:port"