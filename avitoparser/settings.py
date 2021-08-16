BOT_NAME = 'avitoparser'

SPIDER_MODULES = ['avitoparser.spiders']
NEWSPIDER_MODULE = 'avitoparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

IMAGES_STORE = 'images'
IMAGES_THUMBS = {'small': (160, 120),
                 'medium': (320, 240)}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/92.0.4515.131 Safari/537.36 '

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8

DOWNLOAD_DELAY = 1.5

COOKIES_ENABLED = True

ITEM_PIPELINES = {
   'avitoparser.pipelines.AvitoparserPipeline': 300,
   'avitoparser.pipelines.AvitoPhotosPipeline': 200,
}
