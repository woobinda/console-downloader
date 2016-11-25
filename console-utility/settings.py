import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, default=5,
                    help='Threads count'),
parser.add_argument("-f", type=str, default='links.txt',
                    help='Path to links for download'),
parser.add_argument("-l", type=str, default='20m',
                    help='Download rate limit')
parser.add_argument("-o", type=str, default='uploads',
                    help='local folder for upload data')
args = parser.parse_args()

threads_count = args.n
urls_list = args.f
upload_folder = args.o
total_BANDWIDTH = args.l
total_size = 0


def calculate_BANDWIDTH(total_BANDWIDTH):
    """Calculating stream rate units,
    depending on the transmitted from the console suffix.
    """
    if total_BANDWIDTH[-1] == 'k':
        total_BANDWIDTH = int(total_BANDWIDTH[:-1]) * 1024
    elif total_BANDWIDTH[-1] == 'm':
        total_BANDWIDTH = int(total_BANDWIDTH[:-1]) * 1024 * 1024
    return total_BANDWIDTH

total_BANDWIDTH = calculate_BANDWIDTH(total_BANDWIDTH)

BASE_DIR = os.path.abspath('.')

if not os.path.exists(os.path.join(BASE_DIR,
                                   upload_folder)):
    os.mkdir(upload_folder)
UPLOAD_DIR = os.path.join(BASE_DIR, upload_folder)
