BOT_NAME = 'ManHua'

SPIDER_MODULES = ['ManHua.spiders']
NEWSPIDER_MODULE = 'ManHua.spiders'
ITEM_PIPELINES = {'ManHua.pipelines.ManhuaPipeline': 800, }
ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/74.0.3729.163 Safari/537.56'