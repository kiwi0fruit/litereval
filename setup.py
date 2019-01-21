from setuptools import setup, find_packages

import os
import io
import versioneer

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='litereval',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description="Wrapper around ast.literal_eval with new {foo='bar', key=None} dict syntax.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/kiwi0fruit/litereval',

    author='Peter Zagubisalo',
    author_email='peter.zagubisalo@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # keywords='sample setuptools development',
    packages=find_packages(exclude=['docs', 'tests']),

    # install_requires=[],
    python_requires='>=3.6',
)
