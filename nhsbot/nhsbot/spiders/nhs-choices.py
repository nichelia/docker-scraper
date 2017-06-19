import scrapy

class NHSChoices(scrapy.Spider):
  name = "nhs-choices"
  start_urls = [
    'http://www.nhs.uk/Conditions/Pages/hub.aspx'
  ]

  def parse(self, response):
    page = response.url.split('/')[-2]
    filename = 'nhschoices-%s.html' % page

    with open(filename, 'wb') as f:
      f.write(response.body)

    self.log('Saved file %s' % filename)