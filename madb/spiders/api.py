# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider


class ApiSpider(CrawlSpider):
    name = 'api'
    allowed_domains = ['mediaarts-db.bunka.go.jp']
    base_url = 'https://mediaarts-db.bunka.go.jp/api/search'
    parameters = {
        'limit': 500
    }

    def start_requests(self):
        start_url = self.base_url
        if hasattr(self, 'fieldId'):
            self.parameters['fieldId'] = getattr(self, 'fieldId')
            start_url += '?' + urllib.parse.urlencode(self.parameters)
        yield Request(start_url)

    def parse_start_url(self, response: scrapy.http.Response):
        data = json.loads(response.body)
        total = int(data['hitnum'])

        for offset in range(0, total, self.parameters['limit']):
            params = dict(self.parameters, offset=offset)
            url = self.base_url + '?' + urllib.parse.urlencode(params)
            yield Request(url, callback=self.parse_resource)

    def parse_resource(self, response: scrapy.http.Response):
        self.logger.info('response: %s', response.url)
        data = json.loads(response.body)
        for record in data['record']:
            yield record
