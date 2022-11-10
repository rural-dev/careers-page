import json
import scrapy
import csv
from ..utils import clean


class InfostrideSpider(scrapy.Spider):
    name = 'infostride'

    def start_requests(self):
        yield scrapy.Request(
            url='https://api.ceipal.com/aFRIcUdhRkZpYkN4c2c2RkFSdVN0dz09/job-postings/?page=1',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        results = jsonresponse['results']
        for job in results:
            yield scrapy.Request(
                url=f'https://api.ceipal.com/aFRIcUdhRkZpYkN4c2c2RkFSdVN0dz09/job-postings/{job["id"]}/',
                callback=self.parse_detail,
                dont_filter=True,
            )
        next_page = jsonresponse['next']
        if next_page:
            yield scrapy.Request(
                url=f'{next_page}',
                callback=self.parse,
                dont_filter=True,
            )

    def parse_detail(self, response, **kwargs):
        data = json.loads(response.text)

        yield {
            'Name of the role': data['position_title'],
            'Department': '',
            'Location': 'Remote' if data['remote_opportunities'] == 1 else data['city'] + ', ' + data['state'] + ', ' + data['country'],
            'Job type': '',
            'Job description': clean(data['requistion_description']),
            'URL': f'https://infostride.com/job-openings/?job_id={data["id"]}',
        }
