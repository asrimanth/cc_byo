class RedisServerException(Exception):
    pass


class UnknownCommandException(RedisServerException):
    pass


class RedisSyntaxError(RedisServerException):
    pass


class RespProtocolError(RedisServerException):
    pass


class RespParsingError(RedisServerException):
    pass


class CommandProcessingException(RedisServerException):
    pass
