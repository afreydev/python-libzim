#!/usr/bin/env python3
"""
python-libzim (aka libzim)

To compile or run this project, you must first get the libzim headers & binary:

 - You can get the headers here and build and install the binary from source:
   https://github.com/openzim/libzim

 - Or you can download a full prebuilt release (if one exists for your platform):
   https://download.openzim.org/release/libzim/

   cd /tmp && wget -qO- https://download.openzim.org/release/libzim/libzim_linux-x86_64-6.1.1.tar.gz | tar -xz -C .
   # to install libzim system-wide, move the headers and dylib into the system paths 
   mv libzim_linux-x86_64-6.1.1/include/zim /usr/include/zim
   mv libzim_linux-x86_64-6.1.1/lib/x86_64-linux-gnu/libzim.so.6 /usr/lib/libzim.so
   # or, set these vars to make the compiler to search specific paths for libzim .h and .so files
   export LIBZIM_INCLUDE_DIR=/tmp/libzim_linux-x86_64-6.1.1/include
   export LIBZIM_LIBRARY_DIR=/tmp/libzim_linux-x86_64-6.1.1/lib/x86_64-linux-gnu

To rebuild the cython extension, sdist, and bdist wheels:
    rm libzim/libzim.cpp
    rm -rf dist
    rm -rf build
    rm -rf libzim.egg-info
    rm *.so
    python setup.py build_ext --inplace
    python setup.py sdist bdist_wheel
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    pip install --index-url https://test.pypi.org/simple/ libzim
"""
import os
from pathlib import Path
from setuptools import setup, Extension
from ctypes.util import find_library
from Cython.Build import cythonize


PACKAGE_NAME = "libzim"
VERSION = "6.1.1"  # pegged to be the same version as libzim since they are always released together
LICENSE = "GPLv3"
DESCRIPTION = "The official Python API for creating and interacting with ZIM files using libzim"
AUTHOR = "Monadical Inc."
AUTHOR_EMAIL = "jdc@monadical.com"
GITHUB_URL = "https://github.com/openzim/python-libzim"

BASE_DIR = Path(__file__).parent
LIBZIM_CYTHON_DIR = 'libzim'

INCLUDE_DIRS = [str(BASE_DIR / LIBZIM_CYTHON_DIR), str(BASE_DIR / 'include')]
LIBRARY_DIRS = [str(BASE_DIR / 'lib')]

# use this option if you wish to manually specify the path to a prebuilt libzim release (.so and .h files)
# set it to the path of the unzipped libzim subfolder containing zim/*.h
LIBZIM_INCLUDE_DIR = os.getenv('LIBZIM_INCLUDE_DIR')
if LIBZIM_INCLUDE_DIR:
    if (Path(LIBZIM_INCLUDE_DIR) / 'zim/zim.h').exists():
        INCLUDE_DIRS.insert(0, str(LIBZIM_INCLUDE_DIR))
    else:
        raise Exception(
            f'Could not find zim/*.h files in LIBZIM_INCLUDE_DIR={LIBZIM_INCLUDE_DIR}\n'
            f'    Hint: git clone --depth 1 -b tags/{VERSION} https://github.com/openzim/libzim libzim_cpp'
            '          export LIBZIM_INCLUDE_DIR=$PWD/libzim_cpp/include'
        )


# use this option to manually specify the libzim dynamic library (aka "shared object") dir
# set it to the path of the unzipped libzim subfolder containing libzim.so
LIBZIM_LIBRARY_DIR = os.getenv('LIBZIM_LIBRARY_DIR')
if LIBZIM_LIBRARY_DIR:
    if not ((Path(LIBZIM_LIBRARY_DIR) / 'libzim.so').exists() or (Path(LIBZIM_LIBRARY_DIR) / 'libzim.a').exists()):
        potential_dylibs = [f for f in Path(LIBZIM_LIBRARY_DIR).iterdir() if 'libzim.so' in str(f)]
        raise Exception(
            f'Could not find libzim.so file in LIBZIM_LIBRARY_DIR={LIBZIM_LIBRARY_DIR}\n' +
            (
                f'    Hint: ln -s {potential_dylibs[0].name} {LIBZIM_LIBRARY_DIR}/libzim.so'
                if potential_dylibs else
                f'    Hint: LIBZIM_LIBRARY_DIR should look something like .../libzim_linux-x86_64-{VERSION}/lib/x86_64-linux-gnu'
            )
        )
    LIBRARY_DIRS.insert(0, str(LIBZIM_LIBRARY_DIR))
else:
    # the default is to dynamically link (finds externally installed libzim on user's system)
    if not (find_library('zim')):
        print(
            '[!] Warning: Could not find libzim.so in available system libraries\n'
            '    Hint: Install it from source from https://github.com/openzim/libzim\n'
            '          or download a prebuilt zim release and set the env varaibles to point to it:\n'
            f'    LIBZIM_INCLUDE_DIR=/libzim_linux-x86_64-{VERSION}/include\n'
            f'    LIBZIM_LIBRARY_DIR=/libzim_linux-x86_64-{VERSION}/lib/x86_64-linux-gnu'
        )


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    url=GITHUB_URL,
    project_urls={
        'Source': GITHUB_URL,
        'Bug Tracker': f'{GITHUB_URL}/issues',
        'Changelog': f'{GITHUB_URL}/releases',
        'Documentation': f'{GITHUB_URL}/blob/master/README.md',
        'Donate': 'https://www.kiwix.org/en/support-us/',
    },
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=(BASE_DIR / 'README.md').read_text(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    include_package_data=True,
    ext_modules=cythonize(
        [
            Extension(
                PACKAGE_NAME,
                sources=[
                    f"{LIBZIM_CYTHON_DIR}/*.pyx",
                    f"{LIBZIM_CYTHON_DIR}/lib.cxx",
                ],
                include_dirs=INCLUDE_DIRS,
                libraries=["zim"],
                library_dirs=LIBRARY_DIRS,
                extra_compile_args=[
                  "-std=c++11",
                  "-Wall",
                  "-Wextra",
                ],
                language="c++",
            )
        ],
        compiler_directives={"language_level" : "3"},
    ),
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Topic :: Utilities",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Sociology :: History",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: System Administrators",
        
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # "Typing :: Typed",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
)
