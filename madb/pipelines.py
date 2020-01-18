# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter


class PerFieldJsonLinesExportPipeline(object):
    def open_spider(self, spider):
        self.field_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.field_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        field = item['fieldId']
        if field not in self.field_to_exporter:
            f = open('{}.jsonl'.format(field), 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.field_to_exporter[field] = exporter
        return self.field_to_exporter[field]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
