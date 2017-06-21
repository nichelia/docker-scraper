import scrapy, time

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
    # 'http://www.nhs.uk/Conditions/Pages/hub.aspx',
    'http://www.nhs.uk/Conditions/Pages/BodyMap.aspx?Index=A'
  ]
  custom_settings = { # override wide project configuration settings.
    'CONCURRENT_REQUESTS_PER_DOMAIN' : 2,
    'AUTOTHROTTLE_ENABLED' : True,
    'AUTOTHROTTLE_START_DELAY' : 1,
    'AUTOTHROTTLE_MAX_DELAY' : 3
  }


  def parse_(self, response):
    """
      Default callback to process downloaded responses.

      Crawls urls given in the 'Browse by index' section (alphabetical order).
      For each response a custom parser is used.
    """

    index_urls_xpath_selector = '//div[@id="haz-mod1"]//li/a/@href'

    index_urls_to_crawl = response.xpath(index_urls_xpath_selector).extract()

    if index_urls_to_crawl is None:
      return

    for index_url in index_urls_to_crawl:
      yield response.follow(index_url, callback=self.parse_index)


  def parse(self, response):
    # page = response.url.split("?")[1]
    # print page
    # filename = 'nhsbot-%s.html' % page
    # with open(filename, 'wb') as f:
    #     f.write(response.body)

    condition_urls_xpath_selector = '//div[@id="ctl00_PlaceHolderMain_BodyMap_ConditionsByAlphabet"]\
                                     //li/a/@href'

    condition_urls_to_crawl = response.xpath(condition_urls_xpath_selector).extract()

    if condition_urls_to_crawl is None:
      return

    for condition_url in condition_urls_to_crawl:
      yield response.follow(condition_url, callback=self.parse_condition)

  def parse_condition(self, response):
    # page = response.url.split("/")[-1]
    # filename = 'nhsbot-%s.html' % page
    # with open(filename, 'wb') as f:
    #     f.write(response.body)

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

    # Extract metadata elements on the page.
    meta = dict()
    meta_elems = response.xpath('//meta')

    for meta_elem in meta_elems:
      key = meta_elem.xpath('@name').extract_first()
      value = meta_elem.xpath('@content').extract_first()

      if not key or not value:
        continue

      meta[key] = value

    if meta:
      item['meta'] = meta


    # Extract page content.
    content_xpath_selector = '//div[contains(@class,"main-content healthaz-content")] \
                               /div[@id="webZoneLeft"]/ \
                               preceding-sibling::node()'
    content_text_xpath_selector = 'descendant-or-self::*/text()'


    content = (response.xpath(content_xpath_selector)
                       .xpath(content_text_xpath_selector)
                       .extract())

    if content:
      item['content'] = ' '.join(content)

    # Extract last reviewed date.
    last_reviewed_pattern = '%d/%m/%Y'
    last_reviewed_xpath_selector = '//div[contains(@class,"review-date")] \
                                    //span[contains(@class,"review-pad")]/text()'

    last_reviewed_date = response.xpath(last_reviewed_xpath_selector).extract_first()

    try:
      last_reviewed_epoch_date = int( time.mktime( time.strptime(last_reviewed_date, last_reviewed_pattern) ) )
      if last_reviewed_epoch_date:
        item['last_reviewed_epoch_date'] = last_reviewed_epoch_date
    except:
      pass

    return item