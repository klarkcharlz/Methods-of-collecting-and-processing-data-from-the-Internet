import scrapy
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:
    def process_item(self, item, spider):
        return item


class LeroymerlinItemPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
