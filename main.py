import os
import threading
import urllib.request
import time

from multiprocessing import Queue
from config import *


url_queue_lock = threading.Lock()
queue = Queue()


class WorkerThread(threading.Thread):
    
    def __init__(self, queue, url_queue_lock):
        super(WorkerThread, self).__init__()
        self.queue = queue
        self.url_queue_lock = url_queue_lock

    def run(self):
        while True:
            nexturl = self.grab_next_url()
            if nexturl is None:
                return
            self.download_file(nexturl[0], nexturl[1])

    def grab_next_url(self):
        self.url_queue_lock.acquire(1)
        if queue.empty() is True:
            nexturl = None
        else:
            nexturl = queue.get_nowait()
        self.url_queue_lock.release()
        return nexturl

    def download_file(self, file_url, upload_filename):
        global total_size
        file = os.path.join(UPLOAD_DIR + '/' + upload_filename)
        with urllib.request.urlopen(file_url) as data, \
                open(file, 'wb') as filename:
            bits = filename.write(data.read())
        total_size += bits


def main(links_list, threads_count):
    print("STARTED")
    start = time.clock()
    with open(links_list) as links:
        for url in links:
            queue.put(url.rstrip().split(' '))

    for i in range(threads_count):
        thread = WorkerThread(queue, url_queue_lock)
        thread.start()

    while threading.active_count() > 2:
        time.sleep(1)
    print("FINISHED")
    print('Summary downloading size : ' + \
        '%-6.2f'%(total_size) + '  mbs')
    print('Total downloading time: ' + \
        '%-6.2f'%(time.clock() - start) + 'minutes')


if __name__ == '__main__':
    main(links_list, threads_count)
