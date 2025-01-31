from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from src.scrapers.spiders.forumdesas import ForumDesasSpider

from src.scrapers.spiders.actualite import ActualiteSpider
from src.scrapers.spiders.mediacongo import MediacongoSpider
from src.scrapers.spiders.politico_cd import PoliticoSpider
from src.scrapers.spiders.spider_7sur7 import SevenPer7Spider

runner = CrawlerRunner(get_project_settings())
runner.crawl(PoliticoSpider)
runner.crawl(SevenPer7Spider)
runner.crawl(ForumDesasSpider)
runner.crawl(ActualiteSpider)
runner.crawl(MediacongoSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
