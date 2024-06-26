import os
import sys

import requests
from DownloadKit import DownloadKit

from cow_transfer.util import get_headers_from_curl_file

dirname = os.path.dirname(__file__)
# 创建下载器对象
d = DownloadKit(roads=20)
# 线程数
# 大文件分块大小，默认 20MB
d.block_size = '50M'
# 设置文件保存路径
d.global_path = dirname
# 设置重试次数
d.set.retry(8)
# 设置失败重试间隔
d.set.retry(8)
# 设置存在文件名冲突时的处理方式 skip overwrite rename
d.file_exists = 'rename'
HOST = 'https://cowtransfer.com'
SUCCESS_CODE = '0000'


def get_unique_url(download_code):
    url = f"{HOST}/core/api/transfer/share/precheck?downloadCode={download_code}"
    response = requests.get(url, headers=common_header).json()
    if response['code'] != SUCCESS_CODE:
        raise BaseException("获取uniqueUrl失败")
    return response['data']['uniqueUrl']


def get_permission_info(unique_url):
    url = f"{HOST}/core/api/transfer/share/precheck?uniqueUrl={unique_url}"
    response = requests.get(url, headers=common_header).json()
    if response['code'] != SUCCESS_CODE:
        raise BaseException("获取权限信息失败")
    if response['data']['needPassword']:
        raise BaseException("不支持加密文件下载")
    return response


def get_file_details(unique_url):
    url = f"{HOST}/core/api/transfer/share?uniqueUrl={unique_url}"
    response = requests.get(url, headers=common_header).json()
    if response['code'] != SUCCESS_CODE:
        raise BaseException("获取文件详情失败")
    file_details = response['data']['firstFile']
    return {
        'title': file_details['file_info']['title'],
        'format': file_details['file_info']['format'],
        'size': file_details['file_info']['size'],
        'file_id': file_details['id'],
        'guid': response['data']['guid']
    }


def get_download_url(file_details):
    url = f"{HOST}/core/api/transfer/share/download?transferGuid={file_details['guid']}&title={file_details['title']}&fileId={file_details['file_id']}"
    response = requests.get(url, headers=common_header).json()
    if response['code'] != SUCCESS_CODE:
        raise BaseException("获取下载URL失败")
    return response['data']['downloadUrl']


def get_file_name(file_details):
    return file_details['title'] + "." + file_details['format']


def process_bar(num, total):
    rate = float(num) / total
    rate_num = int(100 * rate)
    r = '\r[{}{}]{}%'.format('*' * rate_num, ' ' * (100 - rate_num), rate_num)
    sys.stdout.write(r)
    sys.stdout.flush()


def download_file(unique_url, target=None, threads=20, header_file_path=None):
    if header_file_path is None:
        header_file_path = './header.txt'
    if not os.path.exists(header_file_path):
        raise SyntaxError("请添加header.txt文件")
    global common_header
    common_header = get_headers_from_curl_file(header_file_path)
    get_permission_info(unique_url)
    file_details = get_file_details(unique_url)
    download_url = get_download_url(file_details)
    if target is None:
        target = dirname
    else:
        if os.path.exists(target) and os.path.isdir(target):
            target = target
        else:
            raise BaseException("保存目录需要是一个已存在的目录, 如果不设置，默认为当前目录")
    d.global_path = target
    d.set.roads(threads)
    d.add(download_url, goal_path=target, stream=True)
    d.show()


def show_help():
    sys.stdout.write(
        'download file : cow download ${downloadUniqueUrl}')
    sys.stdout.flush()


def get_str_from_file(file_path):
    with open(file_path, "r") as file:
        return str(file.read()).removesuffix("\n")


if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len <= 1:
        raise SyntaxError("不合法的参数，help显示帮助，download下载文件")
    command = sys.argv[1]
    if command == 'download':
        unique_url = None
        save_target = None
        header_file_path = None
        if arg_len == 4:
            unique_url = sys.argv[2]
            header_file_path = sys.argv[3]
        elif arg_len == 5:
            unique_url = sys.argv[2]
            save_target = sys.argv[3]
            header_file_path = sys.argv[4]
        else:
            raise SyntaxError("不合法的参数个数")
        download_file(unique_url, save_target, header_file_path=header_file_path)
    elif command == 'help':
        show_help()
    else:
        raise SyntaxError("不合法的命令")
