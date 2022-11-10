import json
import scrapy
import csv
from ..utils import clean, cleannewline


class DasmenResidentialSpider(scrapy.Spider):
    name = 'dasmenresidential'

    def start_requests(self):
        yield scrapy.Request(
            url='https://recruitingbypaycor.com/career/CareerHome.action?clientId=8a7883d0688e28aa0168beaee28b24d6&parentUrl=https://dasmenresidential.com/careers/&gns=',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jobs = response.xpath('//div[@class="gnewtonCareerGroupRowClass"]')
        for job in jobs:
            dep = job.xpath(".//preceding-sibling::*[@class='gnewtonCareerGroupHeaderClass'][1]/text()").get()
            link = job.xpath(".//div[@class='gnewtonCareerGroupJobTitleClass']/a/@href").get()
            role = job.xpath(".//div[@class='gnewtonCareerGroupJobTitleClass']/a/text()").get(),
            print(link)
            yield scrapy.Request(
                url=f'{link}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'link': cleannewline(link),
                    'role': cleannewline(role),
                    'dep': cleannewline(dep)
                }
            )

    def parse_detail(self, response, **kwargs):
        desc = "".join(response.xpath('//*[@id="vjs-jobtitle"]').extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['dep'],
            'Location': response.xpath('//*[@id="gnewtonJobLocationInfo"]/text()').get(),
            'Job type': '',
            'Job description': clean(desc),
            'URL': response.request.url,
        }
