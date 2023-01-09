# cow_transfer

## 安装
```
pip install cow_transfer
```
## 使用

### 文件下载
一个完整的奶牛快传的文章下载链接就像这样：https://xiyoucloud.cowtransfer.com/s/9f9b7c098b9049  
你可以根据文件的 id 来下载文件 9f9b7c098b9049。
```
cow download -u 9f9b7c098b9049
```
```
Usage: cow download [OPTIONS]

Options:
  -u, --urlcode TEXT     urlcode for download file  [required]       
  -t, --threads INTEGER  set threads for download file  [default: 20]
  -p, --path PATH        set save path for download file
  --help                 Show this message and exit.
```

### 文件上传
```
Usage: cow upload [OPTIONS]

  CowTransfer - 奶牛快传

Options:
  --authorization TEXT  用户 authorization  [required]
  --remember_mev2 TEXT  用户 remember-mev2  [required]
  --upload_path TEXT    待上传文件或目录路径  [required]
  --folder_name TEXT    文件夹名称
  --title TEXT          传输标题
  --message TEXT        传输描述
  --valid_days INTEGER  传输有效期（天）  [default: 7]
  --chunk_size INTEGER  分块大小（字节）  [default: 2097152]
  --threads INTEGER     上传并发数  [default: 5]
  --help                Show this message and exit.
```

默认情况下会开启 20 个线程对文件进行下载，这会大大加快下载速度，不过下载速度还受到网络带宽的限制，即下载速度最快不会超过网络带宽。

## 打包源码
```
# 安装依赖
pip install wheel
# 打包
python setup.py bdist_wheel sdist

# 上传打包后的 python 包到 https://pypi.org
twine upload dist/*
```