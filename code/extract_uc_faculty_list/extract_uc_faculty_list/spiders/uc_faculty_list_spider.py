import scrapy
from lxml import etree
import re


class UcFacultyListSpider(scrapy.Spider):
    name = 'uc_faculty_list'

    def start_requests(self):
        total_pages = 170
        template_url = "https://researcherprofiles.org/search/default.aspx?searchtype=people&searchfor=&exactphrase=false&perpage=100&offset=0&page={}&totalpages=170&searchrequest=A81BSfTwU3GNm4liSODkW6vB3EBYO6gz+a5TY1bFhuz1tc7ngL4Orww3064KoquG+9VriFtrDjpnsK5w9NhcO/kfsvk/2PSl/SKblT7HEZkWXAx5IRPusnUqOqtGWwiH3V4tBsJ3tamK9kWWF9DtXJMqQ/qxFe2BJZLaDlcUvO2V1N0ytegO2/HBDP8P8QURn+5vo0upMZuRk3TXkXIu+JWGYpISi1oJ0q0+gMvUJ79o75hdhxTooPsOXPSkQtoEArZqyHLjJPk22eg5Y8o8Q20lOjlkeinYiCwOSCR+ir0Fmz2P1wYF/h5NsP2iIhBIkjy9qp1+nIlA3H6H/sA5S29cvngX3xVqX7WEozALU0kuCDKKGCLsO6IIOC8sP+cuj34KQ/2Vk+jjO5+xZ1hK07Z/PsLHWsJS/Kl5x++rdczrSg3Qlz8y94IA1m2FM3tzWaDtFpEcNs71tc7ngL4Orww3064KoquG/9C1XRULWX+2dxkUjoawDsikkUBuiBa9RKeJqbXTHJnMy1S08WS8pKqc8Q7uB8+yXe1oBPOJ1SQeIDn/UP9gUu3J9C5TUQkryZmTRCU0RtqF8NGTpZZpyRfOimtfD03crppmjIFVFtiFGUhAfrKx0MbXCI4MPjCYO+6y+TkZ5mlHJXbfQTXqHn5g22pnI2Qrdksr9CS91NpY8+nZwbFiutmIYA7NevjBpIyLuPhaslOg9MVG0P9Ajw==&sortby=&sortdirection=&showcolumns=11"
        
        for page_num in range(1,total_pages+1):
            yield scrapy.Request(url=template_url.format(page_num), callback=self.parse)

    # start_urls = [template_url.format(i) for i in range(1,total_pages+1)]

    def parse(self, response):
        for profile in response.xpath("//table[@id='tblSearchResults']//tr[@*]"):
            input_box = profile.xpath("input")[0]

            profile_link = input_box.xpath("@id").get()

            profile_data = input_box.xpath("@value").get()
            profile_data = [x.strip() for x in profile_data.split('\n')]

            parsed_data = {re.search(r'<u>(.*?)</u>', x).group(1): re.search(r'</u> ?<br/>(.*?)$', x).group(1) for x in profile_data[1:]}
            parsed_data['name'] = etree.fromstring(profile_data[0]).text
            parsed_data['uc_profile_link'] = profile_link
            yield parsed_data