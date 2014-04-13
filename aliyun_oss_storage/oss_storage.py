import mimetypes
from django.core.files.storage import Storage
from django.conf import settings
from oss.oss_api import OssAPI
from oss_exception import OssPutException

ALIYUN_OSS_DEFAULT_HOST = 'oss.aliyuncs.com'

class AliyunOssStorage(Storage):
    def __init__(self, host=settings.ALIYUN_OSS_DEFAULT_HOST, bucket=settings.ALIYUN_OSS_BUCKET):
        if settings.ALIYUN_OSS_HOST is not None:
            host = settings.ALIYUN_OSS_HOST
        self.host = host
        self.bucket = bucket
        ALIYUN_OSS_ACCESSID = getattr(settings, 'ALIYUN_OSS_ACCESSID')
        ALIYUN_OSS_ACCESSSECRET = getattr(settings, 'ALIYUN_OSS_ACCESSSECRET')
        self.connection = self.get_connection(self.host, ALIYUN_OSS_ACCESSID, ALIYUN_OSS_ACCESSSECRET)

    def get_connection(self, host, accessid, accesskey):
        return OssAPI(host,accessid, accesskey)

    def _put_file(self, filename, content):
        content_type = mimetypes.guess_type(filename)[0] or "application/x-octet-stream"
        result = self.connection.put_object_from_string(self.bucket, filename, content, content_type)
        if result.status / 100 == 2:
            return True
        else:
            raise OssPutException(result.status, result.read())

    def save(self, name, content):
        pass

    def open(self, name, mode='rb'):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        pass

    def url(self, name):
        pass
