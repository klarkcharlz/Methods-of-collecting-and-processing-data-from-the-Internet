BOT_NAME = 'jobparser'

SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0

COOKIES_ENABLED = True

ITEM_PIPELINES = {
   'jobparser.pipelines.JobparserPipeline': 300,
}
