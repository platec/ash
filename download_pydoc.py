
import re
from threading import Thread, Lock
import os
from urllib.parse import urlparse, urljoin
from queue import Queue
import requests

"""
多线程下载python文档页面
"""

BASE_URL = 'http://localhost:5000/'
url_pattern = re.compile(r'href="(.*?)"')

lock = Lock()
url_visited = set()
current_path = os.getcwd()
print(current_path)

class Fetcher(Thread):
    def __init__(self, urls):
        self.urls = urls
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            url = self.urls.get()
            resp = requests.get(url)
            page_content = resp.text
            path = url.replace(BASE_URL, current_path + '/')
            dirname = os.path.dirname(path)
            print(path)
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            if path.endswith('/'):
                path += 'index.html'
            with open(path, 'wt', encoding='utf-8') as f:
                f.write(page_content)
            links = self.parse_links(page_content, url)

            lock.acquire()
            for link in links.difference(url_visited):
                self.urls.put(link)
            url_visited.update(links)
            lock.release()
            self.urls.task_done()

    def parse_links(self, page_content, page_url):
        urls = url_pattern.findall(page_content)
        links = set()
        for url in urls:
            parsed = urlparse(url)
            path = parsed.path
            if parsed.scheme not in ('http', 'https') and path.endswith('.html'):
                links.add(urljoin(page_url, path))
        return links


class ThreadPool:
    def __init__(self, thread_num=1):
        self.tasks = Queue()
        for _ in range(thread_num):
            Fetcher(self.tasks)
    
    def add_task(self, url):
        self.tasks.put(url)

    def wait_completion(self):
        self.tasks.join()


if __name__ == '__main__':
    pool = ThreadPool(8)
    pool.add_task(BASE_URL)
    pool.wait_completion()