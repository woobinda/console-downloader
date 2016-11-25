import os
import threading
import urllib.request
import time

from time import sleep
from datetime import datetime, timedelta
from multiprocessing import Queue


queue_lock = threading.Lock()
queue = Queue()


class DownloadWorker(threading.Thread):
    """Worker for downloading data from URL:

        queue           - array of URLs for download
        queue_lock      - threading Lock object
        BANDWIDTH       - stream rate, byte/s
    """

    def __init__(self, queue, queue_lock, BANDWIDTH):
        super(DownloadWorker, self).__init__()
        self.queue = queue
        self.queue_lock = queue_lock
        self.BANDWIDTH = BANDWIDTH

    def run(self):
        while True:
            nexturl = self.grab_next_url()
            if nexturl is None:
                break
            self.download_file(nexturl[0], nexturl[1], self.BANDWIDTH)

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

    def download_file(self, file_url, local_filename, BANDWIDTH):
        """Downloading data from url to local folder.

            file_url            - link to download file
            local_filename      - filename for local recording
            BANDWIDTH           - stream rate, byte/s
        """
        global total_size   # total size of all downloads
        SECOND = timedelta(seconds=1)
        file = os.path.join(UPLOAD_DIR + '/' + local_filename)
        with urllib.request.urlopen(file_url) as data:
            with open(file, 'wb') as filename:
                for chunk in iter(lambda: data.read(BANDWIDTH), b""):
                    last_time = datetime.now()   # start time for writing chunk
                    filename.write(chunk)
                    time_passed = datetime.now() - last_time   # time delta
                    if time_passed < SECOND:   # if have extra time - waiting
                        time.sleep((SECOND - time_passed).microseconds /
                                   1000000.0)
        size = os.path.getsize(file)
        total_size += size


def main(urls_list, threads_count, total_BANDWIDTH):
    """Main process for downloading data from URL-addresses.
    Reads a file and adds links in queue, init threads:

        urls_list         - file with array of URLs for download
        threads_count     - count of threads/workers
        BANDWIDTH         - total stream rate for all threads, byte/s
    """
    print("\nSTARTED...\n")
    start = time.localtime()   # starting process time
    with open(urls_list) as links:
        for url in links:
            queue.put(url.rstrip().split(' '))

    BANDWIDTH = total_BANDWIDTH // threads_count   # rate for a single stream
    for i in range(threads_count):
        thread = DownloadWorker(queue, queue_lock, BANDWIDTH)
        thread.start()
    while threading.active_count() > 2:
        time.sleep(1)

    print("...FINISHED\n")
    end = time.localtime()   # ending process time
    end_mins = abs(end.tm_min - start.tm_min)
    end_secs = abs(end.tm_sec - start.tm_sec)
    print('Summary downloading size : ' +
          '%.1f mb (%s bytes)' % ((total_size / 1000000), total_size))
    print('Total downloading time: ' + '%d min %d sec \n' % (
        (end_mins), (end_secs))
    )


if __name__ == '__main__':

    from settings import threads_count, urls_list, upload_folder, \
        total_BANDWIDTH, total_size, UPLOAD_DIR

    main(urls_list, threads_count, total_BANDWIDTH)
