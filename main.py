import base64
from icrawler import ImageDownloader
from six.moves.urllib.parse import urlparse
from icrawler.builtin import BaiduImageCrawler
from icrawler.builtin import BingImageCrawler
from icrawler.builtin import GoogleImageCrawler
import argparse, os

parser = argparse.ArgumentParser(description='img_collection')
parser.add_argument('--output_dir', default="", type=str, help='')
parser.add_argument('--N', default=10, type=int, help='')
parser.add_argument('--engine',
                    choices=['baidu', "bing", "google"],
                    default="bing",
                    type=str,
                    help='')
args = parser.parse_args()


class Base64NameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # works for python 3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)


def get_crawler(args, dir_name):
    if args.engine == "baidu":
        crawler = BaiduImageCrawler(downloader_cls=Base64NameDownloader,
                                    storage={'root_dir': dir_name})
    elif args.engine == "bing":
        crawler = BingImageCrawler(downloader_cls=Base64NameDownloader,
                                   storage={'root_dir': dir_name})
    elif args.engine == "google":  # dont work
        crawler = GoogleImageCrawler(storage={'root_dir': dir_name})
    return crawler


if __name__ == "__main__":
    # read ini file.
    with open('./setting.txt', mode='r', encoding="utf_8") as f:
        read_data = list(f)

    print("SELECTED ENGINE : " + args.engine)

    for i in range(len(read_data)):
        print("SEARCH WORD : " + read_data[i].replace('\n', ''))
        print("NUM IMAGES  : " + str(args.N))
        dir_name = os.path.join(
            args.output_dir, read_data[i].replace('\n', '').replace(' ', '_'))

        #init crawler
        crawler = get_crawler(args, dir_name)
        crawler.crawl(keyword=read_data[i], max_num=args.N)
