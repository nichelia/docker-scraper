import scrapy
import time

from datetime import datetime
from nhsbot.items import NhsbotItem

class NHSChoices(scrapy.Spider):
  """
    Creates an NHSChoices Spider class to scrape the
    NHS Choices website.

    Inherits from basic spider which provides start_requests()
    implementation. This sends requests from the start_urls attribute
    and calls the parse method for each resulting responses.
  """

  name = "nhsuk" # defines the spider's name, must be unique (required).
  allowed_domains = [ # limit domains to crawl.
    'nhs.uk'
  ]
  start_urls = [ # define urls to start crawling from.
    'http://www.nhs.uk/Conditions/Pages/hub.aspx'
  ]
  custom_settings = { # override wide project configuration settings.
    'CONCURRENT_REQUESTS_PER_DOMAIN' : 2,
    'AUTOTHROTTLE_ENABLED' : True,
    'AUTOTHROTTLE_START_DELAY' : 1,
    'AUTOTHROTTLE_MAX_DELAY' : 3,
    'LOG_LEVEL': 'INFO'
  }


  def parse(self, response):
    """
      Default callback to process downloaded responses.

      Crawls the urls defined in start_urls, in our case the
      NHS choices conditions website. Aims to extract url links
      from the 'Browse by index' section.
    """

    index_urls_xpath_selector = '//div[@id="haz-mod1"]//li/a/@href'

    index_urls_to_crawl = (response.xpath(index_urls_xpath_selector)
                                   .extract())

    if not index_urls_to_crawl:
      self.logger.info('Failed to find URLs to follow at %s, xpath used: %s',
                        response.url, index_urls_xpath_selector)
      return

    for index_url in index_urls_to_crawl:
      yield response.follow(index_url, callback=self.parse_index)


  def parse_index(self, response):
    """
    Custom parser that aims to extract url links
    from the alphabetical index page.
    Limits the links to the ones interested in
    (url pattern ../conditions/..)
    """

    condition_urls_pattern = '/conditions/'
    condition_urls_xpath_selector = (
      '//div[@id="ctl00_PlaceHolderMain_BodyMap_ConditionsByAlphabet"]' \
      '//li/a/@href')

    condition_urls_to_crawl = (response.xpath(condition_urls_xpath_selector)
                                       .extract())

    if not condition_urls_to_crawl:
      self.logger.info('Failed to find URLs to follow at %s, xpath used: %s',
                        response.url, condition_urls_xpath_selector)
      return

    for condition_url in condition_urls_to_crawl:
      if condition_url.startswith(condition_urls_pattern):
        yield response.follow(condition_url, callback=self.parse_condition)
      else:
        self.logger.info('Ignoring url %s, to satisfy url pattern: %s',
                          condition_url, condition_urls_pattern)


  def parse_condition(self, response):
    """
    Custom parser that aims to scrape required
    information from the condition page.
    Information extracted (if found):
    title, metadata, content, last reviewed date.
    """

    item = NhsbotItem()

    # Add source of our spider.
    item['source'] = 'nhsuk-spider'

    # Add crawled date.
    item['crawled_epoch_date'] = int(time.time())

    # Extract url
    # Add url as id.
    url = response.url
    item['id'] = url
    item['url'] = url

    # Extract title
    title_xpath_selector = '//div[contains(@class,"healthaz-header")]/h1/text()'
    title = response.xpath(title_xpath_selector).extract_first()
    if title:
      item['title'] = title
    else:
      self.logger.info('Could not find a title for %s, xpath used: %s',
                        url, title_xpath_selector)

    # Extract metadata elements on the page.
    meta = dict()
    meta_elems = response.xpath('//meta')
    date_issued_pattern = '%Y-%m-%d'

    for meta_elem in meta_elems:
      key = meta_elem.xpath('@name').extract_first()
      value = meta_elem.xpath('@content').extract_first()

      if not key or not value:
        continue

      # Make sure that date metadata is extracted as UTC ISO8601 format
      if key == 'DC.date.issued':
        self.logger.info('Found date metadata %s, try to convert to UTC' \
                         'ISO8601 format with pattern %s',
                          key, date_issued_pattern)
        try:
          parsed_date = datetime.strptime(value,date_issued_pattern)
          if parsed_date:
            meta[key] = parsed_date.isoformat() + 'Z'
        except:
          pass
      else:
        meta[key] = value

    if meta:
      item['meta'] = meta
    else:
      self.logger.info('Could not find metadata for %s, xpath used: %s',
                        url, 'multiple: //meta, @name, @content')


    # Extract page content.
    content_xpath_selector = '//div[contains(@class,"main-content healthaz-content")]' \
                             '/div[@id="webZoneLeft"]' \
                             '/preceding-sibling::node()'
    content_text_xpath_selector = 'descendant-or-self::*/text()'


    content = (response.xpath(content_xpath_selector)
                       .xpath(content_text_xpath_selector)
                       .extract())

    if content:
      item['content'] = ' '.join(content)
    else:
      self.logger.info('Could not find content for %s, xpath used: %s',
                        url, 'multiple '+content_xpath_selector+' '+
                        content_text_xpath_selector)

    # Extract last reviewed date.
    last_reviewed_pattern = '%d/%m/%Y'
    last_reviewed_xpath_selector = '//div[contains(@class,"review-date")]' \
                                   '//span[contains(@class,"review-pad")]/text()'

    last_reviewed_date = response.xpath(last_reviewed_xpath_selector).extract_first()

    if last_reviewed_date:
      try:
        last_reviewed_epoch_date = int( time.mktime( 
                                         time.strptime(
                                          last_reviewed_date, last_reviewed_pattern)))
        if last_reviewed_epoch_date:
          item['last_reviewed_epoch_date'] = last_reviewed_epoch_date
        else:
          self.logger.info('Failed to convert extracted last reviewed date (%s)' \
                           'to an epoch representation. Date pattern used %s',
                            last_reviewed_date, last_reviewed_pattern)
      except:
        self.logger.info('Failed to convert extracted last reviewed date (%s)' \
                         'to an epoch representation. Date pattern used %s',
                          last_reviewed_date, last_reviewed_pattern)
        pass
    else:
      self.logger.info('Could not find last reviewed date for %s, xpath used: %s',
                        url, last_reviewed_xpath_selector)

    return item