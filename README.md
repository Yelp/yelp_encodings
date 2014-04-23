# yelp_encodings

[![Build Status](https://travis-ci.org/Yelp/yelp_encodings.svg)](https://travis-ci.org/Yelp/yelp_encodings)

yelp_encodings is a Python library created by Yelp to help handle unknown character encodings. That is, when the data you're getting may not be Unicode, it'll effortlessly convert it to Unicode for you.

## Installation

Installing is easy! The package lives on PyPI so just run

```
$ pip install yelp_encodings
```

And you're done!

## Usage

Import the library and just call ``decode`` with the data you want to decode

```
from yelp_encodings import internet

string = 'hello world'
internet.decode(string) # => (u'hello world!', 12)

string = 'Hêllô wõrld'
internet.decode(string) # => (u'H\xeall\xf4 w\xf5rld', 14)
```
