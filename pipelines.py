
import json
import os.path
import time
from temp import set


class JsonWriterPipeline(object):
    """
    写入json文件的pipline
    """

    def __init__(self):
        self.file = None
        if not os.path.exists('../output'):
            os.mkdir('../output')

    def process_item(self, item, spider):
        """
        处理item
        """
        now = set.set()['now']
        if not self.file:
            file_name = now + "_" + spider.name + '.jsonl'
            self.file = open(f'../output/{file_name}', 'wt', encoding='utf-8')
        item['crawl_time'] = int(time.time())
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item
