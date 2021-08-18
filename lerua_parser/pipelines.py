import os

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class LmParserPipeline:
    def process_item(self, item, spider):
        return item


class LmPhotosPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(LmPhotosPipeline, self).__init__(store_uri, download_func, settings)
        self.current_name = ''

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        self.current_name = str(item['name']).replace('\\', ' ').replace('/', ' ').replace(':', '')
        file_name = super().file_path(request, response, info, item=item)
        file_name = os.path.join(self.current_name, file_name)
        return file_name

    def thumb_path(self, request, thumb_id, response=None, info=None):
        file_name = super(LmPhotosPipeline, self).thumb_path(request, thumb_id, response, info)
        file_name = os.path.join(self.current_name, file_name)
        return file_name

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
