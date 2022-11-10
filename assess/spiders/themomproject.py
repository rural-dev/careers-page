import json
import scrapy
import csv
from ..utils import clean


class TheMomProjectSpider(scrapy.Spider):
    name = 'themomproject'

    def start_requests(self):
        yield scrapy.Request(
            url='https://themomproject.com/api/v1/careers',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        jobs = jsonresponse['projects']
        for job in jobs:
            yield scrapy.Request(
                url=f'https://themomproject.com/projects/{job["slug"]}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'role': job['project_title'],
                    'location': ', '.join(job['location_remote_or_city_state_list']),
                    'team': job['industry_name'],
                    'type': job['employment_status_human_readable']
                }
            )

    def parse_detail(self, response, **kwargs):
        desc = "/n".join(response.xpath('//div[@class="project-job-description-content"]').extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'],
            'Location': kwargs['location'],
            'Job type': kwargs['type'],
            'Job description': clean(desc),
            'URL': response.request.url,
        }
