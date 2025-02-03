"""
Python implementation of the RESP Protocol.
"""

from enum import Enum
import io
import logging

from typing import List, Any

logger = logging.getLogger(__name__)


class Symbol(Enum):
    """Symbols used in the RESP protocol."""
    STRING = b"+"  # Simple string
    ERROR = b"-"   # Error message
    INTEGER = b":" # Integer
    BULK_STR = b"$" # Bulk string
    ARRAY = b"*"   # Array
    CRLF = b"\r\n" # Carriage return + line feed
    CRLF_STR = "\r\n" # CRLF as a string
    NULL = b"-1\r\n" # Null value


class RespDecoder:
    def __init__(self, data: bytes, encoding: str = "utf-8") -> None:
        # creates a file-like object for binary data that resides in memory, rather than on disk.
        self.buffer = io.BytesIO(data)  # Store bytes in RAM
        self.encoding = encoding

    def _read_buffer(self) -> bytes:
        data = self.buffer.readline()
        while not data.endswith(Symbol.CRLF.value):
            data += self.buffer.readline()
        return data

    def _decode(self, data: bytes) -> str:
        return data.rstrip(Symbol.CRLF.value).decode(self.encoding)

    def _parse_string(self) -> str:
        return self._decode(self.buffer.readline())

    def _parse_bulk_str(self, length: int) -> str | int | None:
        # Make sure to read CRLF 2 bytes
        result = self._decode(self.buffer.read(length + 2))
        # Convert to int
        try:
            result = int(result)
        except ValueError:
            return None
        return result

    def _parse_array(self, length: int) -> List[Any] | None:
        """Parse each element of the array"""
        result = []
        for _ in range(length):
            result.append(self.parse())
        return result

    def parse(self):
        start_byte = self.buffer.read(1)
        # match statement is supported in Python 3.10 and above.
        match start_byte:
            case Symbol.STRING.value:
                return self._parse_string()
            case Symbol.INTEGER.value:
                return int(self._parse_string())
            case Symbol.ARRAY.value:
                length = int(self._decode(self._read_buffer()))
                if length == -1:
                    return None
                return self._parse_array(length)
            case Symbol.BULK_STR.value:
                length = int(self._decode(self._read_buffer()))
                if length == -1:
                    return None
                return self._parse_bulk_str(length)
            case Symbol.ERROR.value:
                return None
            case _:
                logger.exception(f"Unknown OP: {start_byte}")
                return None


class RespEncoder:
    def __init__(self, encoding: str="utf-8") -> None:
        self.encoding = encoding

    def serialize(self, data: Any, is_error: bool=False) -> bytes:
        result = str()
        if is_error:
            result = f"-{data}{Symbol.CRLF_STR.value}"
        if data is None:
            result = f"{str(Symbol.NULL.value)}{Symbol.CRLF_STR.value}"
        if isinstance(data, str):
            result = f"+{data}{Symbol.CRLF_STR.value}"
        if isinstance(data, int):
            result = f":{data}{Symbol.CRLF_STR.value}"
        if isinstance(data, (list, tuple)):
            result = f"*{len(data)}{Symbol.CRLF_STR.value}"
            for item in data:
                result += f"{self.serialize(item, False)}"
        if not isinstance(data, (str, int, list, tuple, type(None))):
            logger.exception(f"Unsupported data type: {type(data)}")
            raise TypeError(f"Unsupported data type: {type(data)}")
        # Convert result to bytes.
        result = result.encode(self.encoding)
        return result
