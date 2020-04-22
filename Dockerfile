# A minimal runtime environment for python-libzim using pre-built releases.
# Usage:
#     docker build . --tag openzim:python-libzim
#     docker run -it openzim:python-libzim
#     >>> from libzim import ZimCreator, ZimArticle, ZimBlob
#     docker run -it openzim:python-libzim ./some_example_script.py

FROM python:3.7-buster

ENV LIBZIM_VERSION 6.1.1
ENV LIBZIM_RELEASE libzim_linux-x86_64-$LIBZIM_VERSION
ENV LIBZIM_LIBRARY_PATH lib/x86_64-linux-gnu/libzim.so.$LIBZIM_VERSION
ENV LIBZIM_INCLUDE_PATH include/zim

# Install libzim from pre-built release
RUN wget -qO- https://download.openzim.org/release/libzim/$LIBZIM_RELEASE.tar.gz \
    | tar -xz -C . \
    && mv $LIBZIM_RELEASE/$LIBZIM_LIBRARY_PATH /usr/lib/libzim.so \
    && mv $LIBZIM_RELEASE/$LIBZIM_INCLUDE_PATH /usr/include/zim \
    && ldconfig

# Install python dependencies
RUN pip3 install --no-cache-dir --upgrade \
    pip cython==0.29.6 setuptools wheel pytest

# Install python-libzim from local source
ADD . /opt/python-libzim
WORKDIR /opt/python-libzim
RUN pip install -e .
VOLUME /opt/python-libzim

ENTRYPOINT ["/usr/bin/env", "python3"]
