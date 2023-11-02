# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#B11[=z!:xNVdp+NIQ1P33Q9=20a[ba6,
# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成

### 这里自己创建了一个子账号
secret_id="AKIDreNxPiqvqX0Phl2561rY9ZkgLpIdkfSD"

secret_key="jEVaS6VihRwMhzPl610lHh08DAyjRB0i"
#secret_id = os.environ['SecretId']     # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
#secret_key = os.environ['SecretKey']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region = 'ap-nanjing'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

#### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
# 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
with open('Lena.tiff', 'rb') as fp:
    response = client.put_object(
        Bucket='baimo-1322064620',
        Body=fp,
        Key='Lena.tiff',
        StorageClass='STANDARD',
        EnableMD5=False
    )
print(response['ETag'])

#### 字节流简单上传
response = client.put_object(
    Bucket='baimo-1322064620',
    Body=b'bytes',
    Key='Lena.tiff',
    EnableMD5=False
)
print(response['ETag'])


#### chunk 简单上传
import requests
stream = requests.get('https://cloud.tencent.com/document/product/436/7778')

# 网络流将以 Transfer-Encoding:chunked 的方式传输到 COS
response = client.put_object(
    Bucket='baimo-1322064620',
    Body=stream,
    Key='Lena.tiff'
)
print(response['ETag'])

#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
response = client.upload_file(
    Bucket='baimo-1322064620',
    LocalFilePath='local.txt',
    Key='Lena.tiff',
    PartSize=1,
    MAXThread=10,
    EnableMD5=False
)
print(response['ETag'])