# -*- coding: utf-8 -*-
import testify as T
from yelp_encodings import internet_encoding

# Define some interesting unicode inputs
class UNICODE:
    ascii = u'A' # The most basic of unicode.
    latin1 = ascii + u'ü' # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = latin1 + u'€' # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + u'Ł' # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + u'🐵' # Monkey-face emoji. This requires at least a three-byte encoding.


class InternetEncodingTestCase(T.TestCase):

    @T.setup
    def setup(self):
        internet_encoding.register()

    def test_256bytes(self):
        all_bytes = ''.join(chr(i) for i in range(256))
        T.assert_equal(256, len(all_bytes))

        decoded = all_bytes.decode('internet')
        T.assert_equal(256, len(decoded))

        decode_map = dict(zip(all_bytes, decoded))
        T.assert_equal(decode_map['\x80'], u'\x80')
        T.assert_equal(decode_map['\x81'], u'\x81')  # The unknown glyph.

        # Raw non-utf8 bytes should decode the same as windows-1252-replace.
        expected = all_bytes.decode('latin1')
        T.assert_equal(expected, decoded)

        T.assert_equal(decoded.encode('utf8'), decoded.encode('internet'))
        T.assert_equal(decoded, decoded.encode('internet').decode('internet'))  # Idempotency.

    def test_256bytes_replace(self):
        all_bytes = ''.join(chr(i) for i in range(256))
        T.assert_equal(256, len(all_bytes))

        decoded = all_bytes.decode('internet', 'replace')
        T.assert_equal(256, len(decoded))

        decode_map = dict(zip(all_bytes, decoded))
        T.assert_equal(decode_map['\x80'], u'�')
        T.assert_equal(decode_map['\x81'], u'�')  # The unknown glyph.

        # Raw non-utf8 bytes should decode the same as windows-1252-replace.
        expected = all_bytes.decode('utf-8', 'replace')
        T.assert_equal(expected, decoded)

        T.assert_equal(decoded.encode('utf8'), decoded.encode('internet'))
        T.assert_equal(decoded, decoded.encode('internet').decode('internet'))  # Idempotency.

    def test_win1252bytes(self):
        win1252_bytes = ''.join(sorted(set(chr(i) for i in range(256)) - set('\x81\x8d\x8f\x90\x9d')))
        T.assert_equal(251, len(win1252_bytes))

        decoded = win1252_bytes.decode('internet')
        T.assert_equal(251, len(decoded))

        decode_map = dict(zip(win1252_bytes, decoded))
        T.assert_equal(decode_map['\x80'], u'€')

        # Raw non-utf8 bytes should decode the same as windows-1252-replace.
        expected = win1252_bytes.decode('windows-1252')
        T.assert_equal(expected, decoded)

        T.assert_equal(decoded.encode('utf8'), decoded.encode('internet'))
        T.assert_equal(decoded, decoded.encode('internet').decode('internet'))  # Idempotency.

    def test_is_like_utf8(self):
        encoded = UNICODE.utf8.encode('internet')

        T.assert_equal(UNICODE.utf8.encode('utf8'), encoded)
        T.assert_equal(UNICODE.utf8, encoded.decode('utf8'))
        T.assert_equal(UNICODE.utf8, encoded.decode('internet'))

    def test_is_like_windows1252(self):
        encoded = UNICODE.utf8.encode('windows-1252', 'ignore')

        T.assert_equal(UNICODE.win1252.encode('windows-1252'), encoded)
        T.assert_equal(UNICODE.win1252, encoded.decode('internet'))


if __name__ == '__main__':
    T.run()
