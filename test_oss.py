from django.conf import settings
__author__ = 'lfyzjck'


host = 'oss.aliyuncs.com'
access_key = ''
secret_key = ''
bucket = 'lfyzjck-test'
# configure django settings
settings.configure()
from aliyun_oss_storage.oss_storage import AliyunOssStorage

def test_init():
    s = AliyunOssStorage(host='xx', bucket='x', access_key=access_key, secret_key=secret_key)
    assert s.host == 'xx'
    assert s.bucket == 'x'
    assert s.connection is not None

def test_put_file():
    s = AliyunOssStorage(host, bucket, access_key, secret_key)
    assert s._put_file('folder/test.txt', "test content")
    assert s.delete('folder/test.txt')


def test_delete_file():
    f = 'xx.txt'
    s = AliyunOssStorage(host, bucket, access_key, secret_key)
    assert s._save(f, "test content")
    assert s.delete(f)

def test_exists():
    f = 'xxx.txt'
    s = AliyunOssStorage(host, bucket, access_key, secret_key)
    assert s.exists(f)==False
    assert s._save(f, "ss")
    assert s.exists(f)
    assert s.delete(f)

def test_get_size():
    f = 'xxx.txt'
    s = AliyunOssStorage(host, bucket, access_key, secret_key)
    assert s._save(f, "ss")
    assert s.exists(f)
    assert s.size(f) == 2
    assert s.delete(f)

