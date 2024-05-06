import sys
from cow_transfer.cow_download import (
    download_file
)
from cow_transfer.cow_upload import (
    CowUploader
)
import argparse
import click


@click.group()
def cli():
    """upload and download - v0.1.5"""


@cli.command()
@click.option("-h", "--header_file_path", type=click.Path(exists=True), help="header file path",
              default="./header.txt")
@click.option("--upload_path", type=str, prompt="待上传文件或目录路径", help="待上传文件或目录路径", required=True)
@click.option("--folder_name", type=str, help="文件夹名称", default="")
@click.option("--title", type=str, help="传输标题", default="")
@click.option("--message", type=str, help="传输描述", default="")
@click.option("--valid_days", type=int, help="传输有效期（天）", default=7, show_default=True)
@click.option("--chunk_size", type=int, help="分块大小（字节）", default=2097152, show_default=True)
@click.option("--threads", type=int, help="上传并发数", default=5, show_default=True)
def upload(header_file_path, upload_path, folder_name, title, message, valid_days,
           chunk_size, threads):
    """CowTransfer - 奶牛快传"""
    upload_file(header_file_path, upload_path, folder_name, title, message, valid_days,
                chunk_size, threads)


def upload_file(header_file_path, upload_path, folder_name, title, message, valid_days,
                chunk_size, threads):
    # TODO 如果传入特殊字符，就获取 xiyou 的 author 和 remember
    thread = CowUploader(header_file_path, upload_path, folder_name,
                         title, message, valid_days, chunk_size, threads)
    if thread.start_upload():
        click.echo(f"链接：{thread.upload_info.get('transfer_url')}\n"
                   f"口令：{thread.upload_info.get('transfer_code')}")
    else:
        click.echo(f"上传失败，{thread.err}")
    return thread


@cli.command()
# 列表，必须
@click.option('-u', '--urlcode', help="urlcode for download file", required=True)
# int，可选，默认值
@click.option("-t", "--threads", default=20, help="set threads for download file", show_default=True)
# 可选，默认值
@click.option("-p", "--path", type=click.Path(exists=True), help="set save path for download file", default=".")
# 可选，默认值
@click.option("-h", "--header_file_path", type=click.Path(exists=True), help="header file path",
              default="./header.txt")
def download(urlcode, threads, path, header_file_path):
    download_file(urlcode, target=path, threads=threads, header_file_path=header_file_path)


if __name__ == "__main__":
    # download_file('bdae5a8fc3444b', ".", 20, "./header.txt")
    # upload_file("./header.txt", "./DSCF0001123.jpg", "", "", "", 1, 2097152, 5)
    cli()
