"""
A codec suitable for decoding bytes which come from the internet with ill-defined encoding.
We first try to decode with utf8, then fall back to latin1 (latin1html5, really)
"""
import codecs
import encodings.cp1252
from typing import cast
from typing import Tuple

from typing_extensions import Protocol

# -- Codec APIs --

encode = codecs.utf_8_encode


def internet_decode(
    input: bytes, errors: str = "strict", final: bool = False
) -> Tuple[str, int]:
    """The core decoding function"""
    try:
        # First try utf-8. This should be the usual case by far.
        return codecs.utf_8_decode(input, errors, final)
    except UnicodeDecodeError:
        try:
            # If that fails, try windows-1252 (aka cp1252), which defines more characters than latin1,
            # but will fail for five particular bytes: 0x81, 0x8D, 0x8F, 0x90, 0x9D
            return codecs.charmap_decode(input, errors, encodings.cp1252.decoding_table)
        except UnicodeDecodeError:
            # and finally, try latin-1, which never fails, but defines 27 less characters than cp1252.
            return codecs.latin_1_decode(input, errors)


def decode(input: bytes, errors: str = "strict") -> Tuple[str, int]:
    return internet_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes:
        return codecs.utf_8_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(
        self, input: bytes, errors: str = "strict", final: bool = False
    ) -> Tuple[str, int]:
        return internet_decode(input, errors, final)


class StreamWriter(codecs.StreamWriter):
    def encode(self, input: str, errors: str = "strict") -> Tuple[bytes, int]:
        return codecs.utf_8_encode(input, errors)


class StreamReader(codecs.StreamReader):
    def decode(self, input: bytes, errors: str = "strict") -> Tuple[str, int]:
        return internet_decode(input, errors)


# -- codecs API --

# From typeshed.stdlibs.codecs
class _Encoder(Protocol):
    def __call__(
        self, input: str, errors: str = ...
    ) -> Tuple[bytes, int]:  # pragma: no cover
        ...  # signature of Codec().encode


codec_map = {
    "internet": codecs.CodecInfo(
        name="internet",
        encode=cast(_Encoder, encode),
        decode=decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )
}


def register() -> None:
    """perform the codec registration."""
    codecs.register(codec_map.get)
