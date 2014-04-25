django-aliyun-oss-storage
=========================

a storage backend for aliyun oss

How to use
----------

Add following settings in your django app setting.py

DEFAULT_FILE_STORAGE = 'aliyun_oss_storage.oss_storage.AliyunOssStorage'

ALIYUN_OSS_HOST = 'oss.aliyuncs.com'
ALIYUN_OSS_BUCKET = 'YOUR_BUCKET'
ALIYUN_OSS_ACCESSID = 'YOUR_ACCESS_ID'
ALIYUN_OSS_ACCESSSECRET = 'YOUR_ACCESS_KEY'
