import pytest

import yelp_encodings.internet

PY2 = str is bytes


# Define some interesting unicode inputs
class UNICODE:
    ascii = "A"  # The most basic of unicode.
    latin1 = ascii + "ü"  # U-umlaut. This is defined in latin1 but not ascii.
    win1252 = (
        latin1 + "€"
    )  # Euro sign. This is defined in windows-1252, but not latin1.
    bmp = win1252 + "Ł"  # Polish crossed-L. This requires at least a two-byte encoding.
    utf8 = bmp + "🐵"  # Monkey-face emoji. This requires at least a three-byte encoding.


@pytest.fixture(scope="module")
def setup():
    import yelp_encodings.internet

    yelp_encodings.internet.register()


pytestmark = pytest.mark.usefixtures("setup")


def test_256bytes():
    if PY2:
        all_bytes = "".join(chr(i) for i in range(256))  # pragma: no cover
    else:
        all_bytes = bytes(range(256))  # pragma: no cover
    assert 256 == len(all_bytes)

    decoded = all_bytes.decode("internet")
    assert 256 == len(decoded)

    decode_map = dict(zip(all_bytes, decoded))
    assert decode_map["\x80" if PY2 else 0x80] == "\x80"
    assert decode_map["\x81" if PY2 else 0x81] == "\x81"  # The unknown glyph.

    # Raw non-utf8 bytes should decode the same as windows-1252-replace.
    expected = all_bytes.decode("latin1")
    assert expected == decoded

    assert decoded.encode("utf8") == decoded.encode("internet")
    assert decoded == decoded.encode("internet").decode("internet")  # Idempotency.


def test_256bytes_replace():
    if PY2:
        all_bytes = "".join(chr(i) for i in range(256))  # pragma: no cover
    else:
        all_bytes = bytes(range(256))  # pragma: no cover
    assert 256 == len(all_bytes)

    decoded = all_bytes.decode("internet", "replace")
    assert 256 == len(decoded)

    decode_map = dict(zip(all_bytes, decoded))
    assert decode_map["\x80" if PY2 else 0x80] == "�"
    assert decode_map["\x81" if PY2 else 0x81] == "�"  # The unknown glyph.

    # Raw non-utf8 bytes should decode the same as windows-1252-replace.
    expected = all_bytes.decode("utf-8", "replace")
    assert expected == decoded

    assert decoded.encode("utf8") == decoded.encode("internet")
    assert decoded == decoded.encode("internet").decode("internet")  # Idempotency.


def test_win1252bytes():
    if PY2:
        win1252_bytes = "".join(
            sorted({chr(i) for i in range(256)} - set("\x81\x8d\x8f\x90\x9d"))
        )  # pragma: no cover
    else:
        win1252_bytes = bytes(
            sorted(set(range(256)) - {0x81, 0x8D, 0x8F, 0x90, 0x9D})
        )  # pragma: no cover
    assert 251 == len(win1252_bytes)

    decoded = win1252_bytes.decode("internet")
    assert 251 == len(decoded)

    decode_map = dict(zip(win1252_bytes, decoded))
    assert decode_map["\x80" if PY2 else 0x80] == "€"

    # Raw non-utf8 bytes should decode the same as windows-1252-replace.
    expected = win1252_bytes.decode("windows-1252")
    assert expected == decoded

    assert decoded.encode("utf8") == decoded.encode("internet")
    assert decoded == decoded.encode("internet").decode("internet")  # Idempotency.


def test_is_like_utf8():
    encoded = UNICODE.utf8.encode("internet")

    assert UNICODE.utf8.encode("utf8") == encoded
    assert UNICODE.utf8 == encoded.decode("utf8")
    assert UNICODE.utf8 == encoded.decode("internet")


def test_is_like_windows1252():
    encoded = UNICODE.utf8.encode("windows-1252", "ignore")

    assert UNICODE.win1252.encode("windows-1252") == encoded
    assert UNICODE.win1252 == encoded.decode("internet")


def test_unicode():
    assert UNICODE.utf8.encode("utf8").decode("internet") == UNICODE.utf8


def test_incremental_encode():
    from codecs import iterencode

    encoded = iterencode((c for c in UNICODE.utf8), "internet")
    encoded = b"".join(encoded)
    assert encoded == UNICODE.utf8.encode("UTF-8")


def test_incremental_decode():
    decoder = yelp_encodings.internet.IncrementalDecoder()
    result = decoder.decode(b"hello world", True)
    assert result == "hello world"


def test_streaming_encode(tmp_path):
    from codecs import open as codecs_open

    writeme_file = tmp_path / "writeme"
    writeme = codecs_open(writeme_file, mode="w", encoding="internet")
    writeme.write(UNICODE.utf8)
    writeme.close()

    assert writeme_file.read_bytes() == UNICODE.utf8.encode("utf8")


def test_streaming_decode(tmp_path):
    from codecs import open as codecs_open

    readme_file = tmp_path / "readme"
    readme_file.write_bytes(UNICODE.utf8.encode("utf8"))

    readme = codecs_open(readme_file, mode="r", encoding="internet")
    assert readme.read() == UNICODE.utf8


if __name__ == "__main__":
    import sys

    sys.argv.insert(0, "py.test")
    exit(pytest.main())
