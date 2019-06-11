BOT_NAME = 'ManHua'

SPIDER_MODULES = ['ManHua.spiders']
NEWSPIDER_MODULE = 'ManHua.spiders'
ITEM_PIPELINES = {'ManHua.pipelines.ManhuaPipeline': 800, }
ROBOTSTXT_OBEY = False