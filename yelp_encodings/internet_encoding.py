# -*- coding: utf-8 -*-
"""
A codec suitable for decoding bytes which come from the internet with ill-defined encoding.
We first try to decode with utf8, then fall back to latin1 (latin1html5, really)
"""
import codecs
import encodings.cp1252

# -- Codec APIs --

encode = codecs.utf_8_encode


def internet_decode(input, errors='strict', final=False):
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
    except UnicodeEncodeError:
        # Was that thing already unicode? Then it's already decoded.
        if isinstance(input, unicode):
            return (input, len(input))
        else:
            raise


def decode(input, errors='strict'):
    return internet_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.utf_8_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = internet_decode


class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_8_encode


class StreamReader(codecs.StreamReader):
    decode = internet_decode


# -- codecs API --

codec_map = {
    'internet': codecs.CodecInfo(
        name='internet',
        encode=encode,
        decode=decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )
}


def register():
    """perform the codec registration."""
    codecs.register(codec_map.get)
