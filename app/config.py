import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, help='Threads count'),
parser.add_argument("--l", type=int, help='Download speed limit'),
parser.add_argument("--f", type=str, help='Path to links for upload'),
parser.add_argument("--o", type=str, help='Folder for download')
args = parser.parse_args()

threads_count = args.n
speed_limit = args.l
links_list = args.f
upload_folder = args.o
total_size = 0


BASE_DIR = os.path.abspath('.')
if not os.path.exists(os.path.join(BASE_DIR,
                                   upload_folder)):
    os.mkdir(upload_folder)
UPLOAD_DIR = os.path.join(BASE_DIR, upload_folder)
