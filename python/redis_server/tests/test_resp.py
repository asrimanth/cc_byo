import pytest
from src.resp import RespDecoder, Symbol

def test_decode_simple_string():
    data = b"+OK\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == "OK"

def test_decode_error():
    data = b"-Error message\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() is None

def test_decode_integer():
    data = b":1000\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == 1000

def test_decode_bulk_string():
    data = b"$11\r\nhello world\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == "hello world"

def test_decode_null_bulk_string():
    data = b"$-1\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() is None

def test_decode_empty_bulk_string():
    data = b"$0\r\n\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == ""

def test_decode_array():
    data = b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == ["echo", "hello world"]

def test_decode_array_with_integer():
    data = b"*3\r\n$3\r\nget\r\n$3\r\nkey\r\n:1000\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == ["get", "key", 1000]

def test_decode_array_with_null_bulk_string():
    data = b"*2\r\n$3\r\nget\r\n$-1\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == ["get", None]

def test_decode_nested_array():
    data = b"*2\r\n*1\r\n$4\r\nping\r\n*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == [["ping"], ["get", "key"]]

def test_decode_large_integer():
    data = b":999999999999999999\r\n"
    decoder = RespDecoder(data)
    assert decoder.parse() == 999999999999999999

def test_decode_unknown_op(caplog):
    data = b"!unknown\r\n"
    decoder = RespDecoder(data)
    result = decoder.parse()
    assert result is None
    assert "Unknown OP" in caplog.text
