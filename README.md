
# python-libzim

Python bindings for [libzim](https://github.com/openzim/libzim).

## Quickstart

```bash
# Install from PyPI: https://pypi.org/project/libzim/
pip3 install libzim
```

Then import the writer models and methods using `from libzim import ...`:

```python3
# Writer API
from libzim import zimcreator, ZimArticle

with zimcreator('test.zim') as zc:
    zc.add_article(ZimArticle(
        content='''<!DOCTYPE html> 
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Zim Test</title>
            </head>
            <body>
                <h1> ñññ Unicode 🎉 ñññ </h1>
            </body>
        </html>
        ''',
            filename='index.html',
            url='A/index.html',
            title='Zim Test',
            should_compress=True,
            should_index=True,
            mime_type="text/html",
        ))

# Reader API coming soon...
from libzim import zimreader

with zimreader('test.zim') as zr:
    for article in zr.namespace('A'):
        print(article.url, article.filename, article.mime_type, article.title)
        print(article.content.decode())
```

---

## User Documentation

### Setup: Ubuntu/Debian `x86_64` (Recommended)

Install the python `libzim` package from PyPI.
```bash
pip3 install libzim
python -c "from libzim import ZimArticle"
```

The `x86_64` linux wheel automatically includes the `libzim.so` dylib and headers, but other platforms may need to install `libzim` and its headers manually.

#### Installing the `libzim` dylib and headers manually

```bash
# Install the `libzim` dylib and headers from a pre-built release
LIBZIM_VERSION=6.1.1
LIBZIM_RELEASE=libzim_linux-x86_64-$LIBZIM_VERSION
LIBZIM_LIBRARY_PATH=lib/x86_64-linux-gnu/libzim.so.$LIBZIM_VERSION
LIBZIM_INCLUDE_PATH=include/zim

wget -qO- https://download.openzim.org/release/libzim/$LIBZIM_RELEASE.tar.gz | tar -xz -C .
sudo mv $LIBZIM_RELEASE/$LIBZIM_LIBRARY_PATH /usr/lib/libzim.so
sudo mv $LIBZIM_RELEASE/$LIBZIM_INCLUDE_PATH /usr/include/zim
sudo ldconfig
```
If a pre-built release is not available for your platform, you can also [install `libzim` from source](https://github.com/openzim/libzim#dependencies).


## Setup: Docker (Optional)

```bash
docker build . --tag openzim:python-libzim

# Run a custom script inside the container
docker run -it openzim:python-libzim ./some_example_script.py

# Or use the python repl interactively
docker run -it openzim:python-libzim
>>> from libzim import ZimCreator, ZimArticle, ZimBlob
```

---

## Developer Documentation

**These instructions are for developers working on the `python-libzim` source code itself.** *If you are simply a user of the library and you don't intend to change its internal source code, follow the User Documentation instructions above instead.*

### Setup: Ubuntu/Debian

*Note: Make sure you've installed `libzim` dylib + headers first (see above).*

```bash
apt install coreutils wget git ca-certificates \
        g++ pkg-config libtool automake autoconf make meson ninja-build \
        liblzma-dev zlib1g-dev libicu-dev libgumbo-dev libmagic-dev

pip3 install --upgrade pip pipenv

git clone https://github.com/openzim/python-libzim
cd python-libzim
python setup.py build_ext
pipenv install --dev
pipenv run pip install -e .
pipenv run python -c "from libzim import ZimArticle"
```

### Setup: Docker

```bash
docker build . -f Dockerfile.dev --tag openzim:python-libzim-dev

docker run -it openzim:python-libzim-dev ./some_example_script.py

docker run -it openzim:python-libzim-dev
$ black . && flake8 . && pytest .
$ pipenv install --dev <newpackagehere>
$ python setup.py build_ext
$ python setup.py sdist bdist_wheel
$ python setup.py install
$ python -c "from libzim import ZimArticle"

```

---

## Common Tasks

### Rebuild Cython extension

```bash
rm libzim/libzim.cpp
rm -Rf build
rm -Rf *.so
python setup.py build_ext
python setup.py install
```

### Build package `stist` and `bdist_wheels` for PyPI
```bash
python setup.py sdist bdist_wheel

# upload to PyPI (caution: this is done automatically via Github Actions)
twine upload dist/*
```

### Run Tests

```bash
# Autoformat code with black
black --exclude=setup.py .
# Lint and check for errors with flake8
flake8 --exclude=setup.py .
# Typecheck with mypy (optional)
mypy .
# Run tests
pytest .
```



```bash
python setup.py build_ext -i
python tests/test_libzim.py

# or

./rebuild.sh
./run_tests
```
```bash
docker build --tag openzim:python-libzim .
docker run python-libzim -v .:/opt/python-libzim
docker run \
  --name=hera \
  --network=hera \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/certs:/certs \
  aschzero/hera:latest
```
```bash
docker-compose build
docker-compose run libzim /bin/bash
```

---

## API Reference

```python3
from libzim import ZimArticle, ZimBlob, ZimCreator

class ZimTestArticle(ZimArticle):
    content = '''<!DOCTYPE html> 
                <html class="client-js">
                <head><meta charset="UTF-8">
                <title>Monadical</title>
                </head>
                <h1> ñññ Hello, it works ñññ </h1></html>'''

    def __init__(self):
        ZimArticle.__init__(self)

    def is_redirect(self):
        return False

    def get_url(self):
        return "A/Monadical_SAS"

    def get_title(self):
        return "Monadical SAS"
    
    def get_mime_type(self):
        return "text/html"
    
    def get_filename(self):
        return ""
    
    def should_compress(self):
        return True

    def should_index(self):
        return True

    def get_data(self):
        return ZimBlob(self.content.encode('UTF-8'))

# Create a ZimTestArticle article

article = ZimTestArticle()

# Write the articles

import uuid
rnd_str = str(uuid.uuid1()) 
test_zim_file_path = "/opt/python-libzim/tests/kiwix-test"

with ZimCreator(test_zim_file_path + '-' + rnd_str + '.zim') as zc:
    zc.add_article(article)
    if not zc.mandatory_metadata_ok():
        zc.update_metadata(creator='python-libzim',
                                    description='Created in python',
                                    name='Hola',publisher='Monadical',
                                    title='Test Zim')

```
