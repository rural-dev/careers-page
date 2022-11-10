import json
import scrapy
import csv
from ..utils import clean


class BelmontBehavioralSpider(scrapy.Spider):
    name = 'belmontbehavioral'

    def start_requests(self):
        yield scrapy.Request(
            url='https://recruiting.ultipro.com/ACA1001/JobBoard/f24b6286-a80b-4d02-e4e1-ad04762a00de/?q=belmont&o=relevance&f4=cLOvmm4UsFmPq-IAdLrnig+XPzvHHQfCFq9_m5pihZibg+-WklicUeSUSLsnN8dpRTvw',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        token = response.xpath("//script[contains(., '__RequestVerificationToken')]/text()").get()
        splitter = token.split('"')
        print(splitter[5])
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7",
            "content-type": "application/json; charset=UTF-8",
            "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "x-requestverificationtoken": splitter[5]
        }
        data = {"opportunitySearch": {"Top": 50, "Skip": 0, "QueryString": "belmont", "OrderBy": [
            {"Value": "relevance", "PropertyName": "MatchScore", "Ascending": False}], "Filters": [
            {"t": "TermsSearchFilterDto", "fieldName": 4, "extra": None,
             "values": ["9aafb370-146e-59b0-8fab-e20074bae78a", "1ceffc5c-1f74-5a08-bdfe-6e698a16626e",
                        "892569f9-1ec5-4449-8bb2-737c769453bf"]},
            {"t": "TermsSearchFilterDto", "fieldName": 5, "extra": None, "values": []},
            {"t": "TermsSearchFilterDto", "fieldName": 6, "extra": None, "values": []}]},
                "matchCriteria": {"PreferredJobs": [], "Educations": [], "LicenseAndCertifications": [], "Skills": [],
                                  "hasNoLicenses": False, "SkippedSkills": []}}
        yield scrapy.Request(
            url=f'https://recruiting.ultipro.com/ACA1001/JobBoard/f24b6286-a80b-4d02-e4e1-ad04762a00de/JobBoardView/LoadSearchResults',
            callback=self.parse_list,
            headers=headers,
            method='POST',
            body=json.dumps(data),
            dont_filter=True,
        )

    def parse_list(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        opportunities = jsonresponse["opportunities"]
        for job in opportunities:
            yield scrapy.Request(
                url=f'https://recruiting.ultipro.com/ACA1001/JobBoard/f24b6286-a80b-4d02-e4e1-ad04762a00de/OpportunityDetail?opportunityId={job["Id"]}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={'job': job}
            )

    def parse_detail(self, response, **kwargs):
        script = response.xpath("//script[contains(., 'US.Opportunity.CandidateOpportunityDetail')]/text()").get()
        data = json.loads("{" + script.split("({")[1].split("})")[0] + "}")
        print(data)
        locations = []
        for location in data['Locations']:
            if location['LocalizedName'] is None:
                address = location['Address']
                locations.append(
                    address['City'] + ", " + address['State']['Code'] + " " + address['PostalCode'] + ", " +
                    address['Country']['Code'])
            else:
                locations.append(location['LocalizedName'])
        yield {
            'Name of the role': data['Title'],
            'Department': data['JobCategoryName'],
            'Location': locations,
            'Job type': 'Full Time' if data['FullTime'] else 'Part Time',
            'Job description': clean(data['Description']),
            'URL': response.request.url,
        }
