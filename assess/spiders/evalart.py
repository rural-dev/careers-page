import json
import scrapy
import csv
from ..utils import clean


class EvalartSpider(scrapy.Spider):
    name = 'evalart'

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://evalart.com/en/questionnaires/',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        links = response.xpath('//div[@id="questionnaire_catalog_tree"]/ul/li/ul/li/ul/li/a/@href').getall()
        for idx, link in enumerate(links):
            yield scrapy.Request(
                url=f'https://evalart.com{link}/',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs=({"idx": idx})
            )

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//h1/strong/text()').get()
        desc = response.xpath('//div[contains(text(),"Description")]/following-sibling::div[1]/text()').get()
        family = response.xpath('//div[contains(text(),"family")]/following-sibling::div[1]/text()').get()
        subfamily = response.xpath('//div[contains(text(),"Sub Family")]/following-sibling::div[1]/text()').get()
        level = response.xpath('//div[contains(text(),"Level")]/following-sibling::div[1]/text()').get()
        time = response.xpath('//div[contains(text(),"Time Limit")]/following-sibling::div[1]/text()').get()
        type = response.xpath('//div[contains(text(),"Type")]/following-sibling::div[1]/text()').get()
        status = response.xpath('//div[contains(text(),"Status")]/following-sibling::div[1]/text()').get()
        areas = response.xpath('//div[contains(text(),"Evaluated Areas")]/following-sibling::div[1]/table/tbody/tr')
        area_test = []
        for area in areas:
            result = ": ".join(area.xpath('.//td/text()').getall())
            area_test.append(result)

        yield {
            'idx': kwargs['idx'],
            'url': response.request.url,
            'title': title,
            'desc': desc,
            'family': family,
            'subfamily': subfamily,
            'level': level,
            'time': time,
            'type': type,
            'status': status,
            'area_test': area_test,
        }