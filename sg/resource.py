import boto


class AwsResource(object):
    def __init__(self, access_key, secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key

        self.__l1 = None

    @property
    def access_key(self):
        return self.__access_key

    @property
    def secret_key(self):
        return self.__secret_key

    def get_l1(self):
        if self.__l1 is None:
            self.__l1 = boto.glacier.layer1.Layer1(
                aws_access_key_id=self.__access_key, 
                aws_secret_access_key=self.__secret_key)

        return self.__l1
