from abc import abstractmethod


class RedisInterface():
    @abstractmethod
    def set_info(self, authentication_token, time, user_reference, user_type_name, user_name): pass
