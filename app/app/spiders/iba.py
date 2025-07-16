import scrapy


class IBASpider(scrapy.Spider):
    name = "iba"

    start_urls = [
        "https://iba-world.com/cocktails/all-cocktails/"
    ]

    def parse(self, response):
        page_name = response.css('h1.elementor-heading-title')[0].xpath('text()').get().strip()
        sections = [x for x in response.css('div.elementor-shortcode') if x.css('p')]

        if page_name != 'All Cocktails' and len(sections) > 1:
            method, garnish = sections[0], sections[1]

            yield {
                'name': page_name,
                # TODO : Decide how to parse the ingredients list. save as string or list?
                'ingredients': "\n".join(response.css('div.elementor-shortcode ul').css('li::text').getall()),
                'method': [''.join(x.css('::text').getall()) for x in method.css('p')],
                'garnish': [''.join(x.css('::text').getall()) for x in garnish.css('p')],
                'url': response.url,
            }


        for cocktail in response.css('div.cocktail a'):
            yield response.follow(cocktail.attrib['href'], callback=self.parse)

        next_page = response.css('.next')
        if next_page:
            yield response.follow(next_page.attrib['href'], callback=self.parse) 
