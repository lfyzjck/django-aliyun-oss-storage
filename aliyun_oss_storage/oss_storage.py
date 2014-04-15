import mimetypes
import os.path
from django.core.files.storage import Storage
from django.conf import settings
from oss.oss_api import OssAPI
from oss.oss_util import *
from oss.oss_xml_handler import *
from oss_exception import OssPutException

ALIYUN_OSS_DEFAULT_HOST = 'oss.aliyuncs.com'

ALIYUN_OSS_HOST = getattr(settings, 'ALIYUN_OSS_HOST', ALIYUN_OSS_DEFAULT_HOST)
ALIYUN_OSS_BUCKET = getattr(settings, 'ALIYUN_OSS_BUCKET', None)
ALIYUN_OSS_ACCESSID = getattr(settings, 'ALIYUN_OSS_ACCESSID', None)
ALIYUN_OSS_ACCESSSECRET = getattr(settings, 'ALIYUN_OSS_ACCESSSECRET', None)

class AliyunOssStorage(Storage):
    def __init__(self, host=ALIYUN_OSS_HOST, bucket=ALIYUN_OSS_BUCKET, access_key=None, secret_key = None):
        if host is None:
            host = ALIYUN_OSS_DEFAULT_HOST
        self.host = host
        self.bucket = bucket

        if not access_key and not secret_key:
            access_key = ALIYUN_OSS_ACCESSID
            secret_key = ALIYUN_OSS_ACCESSSECRET
        self.connection = self.get_connection(self.host, access_key, secret_key)

    def get_connection(self, host, accessid, accesskey):
        return OssAPI(host,accessid, accesskey)

    def _put_file(self, filename, content):
        content_type = mimetypes.guess_type(filename)[0] or "application/x-octet-stream"
        result = self.connection.put_object_from_string(self.bucket, filename, content, content_type)
        if result.status / 100 == 2:
            return True
        else:
            raise IOError("OSSStorageError: %s" % result.read())
    def _clean_name(self, name):
        return os.path.normpath(name).replace("\\", '/')

    def _save(self, name, content):
        name = self._clean_name(name)
        self._put_file(name, content)
        return name

    def open(self, name, mode='rb'):
        pass

    def delete(self, name):
        name = self._clean_name(name)
        res = self.connection.delete_object(self.bucket, name)
        if res.status != 204:
           raise IOError("OSSStorageError: %s" % res.read())
        else:
            return True

    def exists(self, name):
        name = self._clean_name(name)
        res = self.connection.head_object(self.bucket, name)
        return (res.status / 100) == 2

    def listdir(self, path):
        path = self._clean_name(path)
        res = self.connection.get_object_group_index(self.bucket, path)
        if (res.status / 100) == 2:
            print "get_object_group_index OK"
            body = res.read()
            h = GetObjectGroupIndexXml(body)
            for i in h.list():
                print "object group part msg:", i
            else:
                print "get_object_group_index ERROR"
        return

    def size(self, name):
        name = self._clean_name(name)
        res = self.connection.head_object(self.bucket, name)
        header_map = convert_header2map(res.getheaders())
        content_length = safe_get_element("content-length", header_map)
        return content_length and int(content_length) or 0


    def url(self, name):
        pass
