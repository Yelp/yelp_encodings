from setuptools import find_packages
from setuptools import setup


def main():
    setup(
        name="yelp_encodings",
        url='https://github.com/Yelp/yelp_encodings',
        version="1.0.0",

        author='Buck Golemon',
        author_email='buck@yelp.com',
        description='string encodings invented and maintained by yelp',

        platforms='any',
        classifiers=[
            'License :: Public Domain',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
        ],

        packages=find_packages('.', exclude=('tests*',)),
    )


if __name__ == '__main__':
    exit(main())
