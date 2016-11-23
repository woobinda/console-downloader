import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=5,
                    help='Threads count'),
parser.add_argument("--f", type=str, default='links.txt',
                    help='Path to links for download'),
parser.add_argument("--o", type=str, default='uploads',
                    help='local folder for upload data')
args = parser.parse_args()

threads_count = args.n
urls_list = args.f
upload_folder = args.o
total_size = 0


BASE_DIR = os.path.abspath('.')
if not os.path.exists(os.path.join(BASE_DIR,
                                   upload_folder)):
    os.mkdir(upload_folder)
UPLOAD_DIR = os.path.join(BASE_DIR, upload_folder)
