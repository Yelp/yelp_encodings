from setuptools import find_packages
from setuptools import setup


def main():
    setup(
        name="yelp_encodings",
        url='https://github.com/Yelp/yelp_encodings',
        version="2.0.0",

        author='Buck Golemon',
        author_email='buck@yelp.com',
        description='string encodings invented and maintained by yelp',

        platforms='any',
        classifiers=[
            'License :: Public Domain',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
        ],
        install_requires=[
            'typing-extensions'
        ],
        python_requires='>=3.7',
        package_data={
            "yelp_encodings": ["py.typed"],
        },
        packages=find_packages('.', exclude=('tests*',)),
    )


if __name__ == '__main__':
    exit(main())
