# yelp\_encodings

[![Build Status](https://travis-ci.org/Yelp/yelp_encodings.svg)](https://travis-ci.org/Yelp/yelp\_encodings)

`yelp_encodings` contains an 'internet' encoding which is appropriate for dealing with poorly encoded bytes coming from
internet clients. The internet encoding will always succeed in decoding any bytestring. This is most often useful for
logging bad requests. 


## Installation

For a primer on pip and virtualenv, see the [Python Packaging User Guide](https://python-packaging-user-guide.readthedocs.org/en/latest/tutorial.html).

TL;DR: `pip install yelp_encodings`


## Usage

Once you've registered the codec with python, you can use it anywhere in your app.

```python
>>> from yelp_encodings import internet
>>> internet.register()

>>> euro = u'€'

>>> print(euro.encode('UTF-8').decode('internet'))
€

>>> print(euro.encode('cp1252').decode('internet'))
€

```
