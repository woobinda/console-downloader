import os
import threading
import urllib.request
import time

from multiprocessing import Queue
from config import *


queue_lock = threading.Lock()
queue = Queue()


class DowloadWorker(threading.Thread):
    """
    Worker for downloading data from URL:

        queue           - array of URLs for downloading
        queue_lock      - threading Lock object

    """
    def __init__(self, queue, queue_lock):
        super(DowloadWorker, self).__init__()
        self.queue = queue
        self.queue_lock = queue_lock

    def run(self):
        while True:
            nexturl = self.grab_next_url()
            if nexturl is None:
                break
            self.download_file(nexturl[0], nexturl[1])

    def grab_next_url(self):
        """
        Get next url from queue.
        """
        self.queue_lock.acquire(1)
        if queue.empty() is True:
            nexturl = None
        else:
            nexturl = queue.get_nowait()
        self.queue_lock.release()
        return nexturl

    def download_file(self, file_url, local_filename):
        """
        Downloading data from url to local folder.

            file_url            - link to download file
            local_filename      - filename for local recording
            total_size          - total size of all downloadings

        """
        global total_size
        file = os.path.join(UPLOAD_DIR + '/' + local_filename)
        with urllib.request.urlopen(file_url) as data, \
                open(file, 'wb') as filename:
            bits = filename.write(data.read())
        total_size += bits


def main(urls_list, threads_count):
    """
    Main process for downloading data from URL-addresses.
    Reads a file and adds links in queue, init threads.

        urls_list         - file with array of URLs for downloading
        threads_count     - count of threads/workers
        start             - starting process time
        end               - ending process time

    """
    print("\nSTARTED\n")
    start = time.localtime()
    with open(urls_list) as links:
        for url in links:
            queue.put(url.rstrip().split(' '))

    for i in range(threads_count):
        thread = DowloadWorker(queue, queue_lock)
        thread.start()
    while threading.active_count() > 2:
        time.sleep(1)

    print("FINISHED")
    end = time.localtime()
    print('Summary downloading size : ' +
          '%.1f mb (%s bytes)' % ((total_size / 100000), total_size))
    print('Total downloading time: ' + '%s min %s sec \n' % (
        (end.tm_min - start.tm_min), (end.tm_sec - start.tm_sec))
    )


if __name__ == '__main__':
    main(urls_list, threads_count)
