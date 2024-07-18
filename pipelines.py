
import json
import os.path
import time
import sys


class JsonWriterPipeline(object):
    """
    写入json文件的pipline
    """

    def __init__(self):
        self.file = None
        self.argv = eval(sys.argv[2])
        self.dirs = sys.argv[3]

        if not os.path.exists(self.dirs):
            os.mkdir(self.dirs)

    def process_item(self, item, spider):
        """
        处理item
        """
        i = self.argv
        if not self.file:
            # print('spider', spider)
            # print('spider.name', spider.name)
            # print('type(spider.name)', type(spider.name))
            file_name = i['keywords'] + "_" + i['end_time'] + "_" + i['start_time'] + "_" + i['now'] + "_" + spider.name + '.jsonl'
            file_name = '{}_{}_{}_{}_{}.jsonl'.format(i['keywords'], i['end_time'], i['start_time'], i['now'], spider.name)
            self.file = open(self.dirs + file_name, 'wt', encoding='utf-8')
        item['crawl_time'] = int(time.time())
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item
