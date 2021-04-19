from utils.constant import TIME_ERROR, NO_RESPONSE_ON_INSERT
from utils.interface import RedisInterface
from utils.settings import REDIS_INSTANCE


class TokenManagement(RedisInterface):

    def add_entry(self, name, time, value):
        if not isinstance(time, int):
            raise ValueError(TIME_ERROR)

        response = REDIS_INSTANCE.setex(name=name, time=time, value=value)
        if not response:
            raise MemoryError(NO_RESPONSE_ON_INSERT)

    def set_info(self, authentication_token, time, user_reference, user_type_name, user_name):
        REDIS_INSTANCE.setex(name=authentication_token, time=time, value=user_reference)
        REDIS_INSTANCE.setex(name=authentication_token + user_reference, time=time, value=user_type_name)
        REDIS_INSTANCE.setex(name=user_reference, time=time, value=user_name)

    def get_info(self, authentication_token):
        user_info = REDIS_INSTANCE.get(name=authentication_token)
        if user_info:
            user_type_name = REDIS_INSTANCE.get(name=authentication_token + user_info.decode("utf-8"))
            user_name = REDIS_INSTANCE.get(name=user_info.decode("utf-8"))
            return user_info.decode("utf-8"), user_type_name.decode("utf-8"), user_name.decode(
                "utf-8")
        return False
