import scrapy


class IBASpider(scrapy.Spider):
    name = "iba"

    start_urls = [
        "https://iba-world.com/cocktails/all-cocktails/"
    ]

    def parse(self, response):
        page_name = response.css('h1.elementor-heading-title')[0].xpath('text()').get().strip()
        if page_name != 'All Cocktails':
            yield {
                'name': page_name,
                'url': response.url,
                'ingredients': "\n".join(response.css('div.elementor-shortcode ul').css('li::text').getall()),
                # TODO: Add method and garnish processing
            }


        for cocktail in response.css('div.cocktail a'):
            yield response.follow(cocktail.attrib['href'], callback=self.parse)

        next_page = response.css('.next')
        if next_page:
            yield response.follow(next_page.attrib['href'], callback=self.parse) 
