#!/usr/bin/env python3

import os
import sys
import tempfile
import pathlib
import uuid
import shutil
import unittest
from ctypes.util import find_library

BASE_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / 'cython_build'))
sys.path.insert(0, str(BASE_DIR))

if not find_library('zim'):
    raise ImportError('Missing libzim.so or libzim.a dylib in system libs')

from libzim import ZimArticle, ZimBlob, ZimCreator


class ZimTestArticle(ZimArticle):
    content = '''<!DOCTYPE html> 
                <html class="client-js">
                <head><meta charset="UTF-8">
                <title>Monadical</title>
                </head>
                <h1> ñññ Hello, it works ñññ </h1></html>'''

    def is_redirect(self):
        return False

    @property
    def can_write(self):
        return True

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
       

class TestZimCreator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_article = ZimTestArticle()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_article(self):
        zim_creator = ZimCreator(
            os.path.join(self.test_dir, 'test_zim_creator.zim'),
            main_page="welcome",
            index_language="eng",
            min_chunk_size=2048,
        )
        zim_creator.add_article(self.test_article)
        # Set mandatory metadata
        zim_creator.update_metadata(
            creator='python-libzim',
            description='Created in python',
            name='Hola',
            publisher='Monadical',
            title='Test Zim',
        )
        zim_creator.finalize()

    def test_article_metadata(self):
        zim_creator = ZimCreator(
            os.path.join(self.test_dir, f'test-metadata-{uuid.uuid1()}.zim'),
            main_page="welcome",
            index_language="eng",
            min_chunk_size= 2048,
        )
        zim_creator.update_metadata(**TEST_METADATA)
        self.assertEqual(zim_creator._get_metadata(), TEST_METADATA)
        zim_creator.finalize()

    def test_check_mandatory_metadata(self):
        zim_creator = ZimCreator(
            os.path.join(self.test_dir, f'test-metadata-{uuid.uuid1()}.zim'),
            main_page="welcome",
            index_language="eng",
            min_chunk_size= 2048,
        )
        self.assertFalse(zim_creator.mandatory_metadata_ok())
        zim_creator.update_metadata(
            creator='python-libzim',
            description='Created in python',
            name='Hola',
            publisher='Monadical',
            title='Test Zim',
        )
        self.assertTrue(zim_creator.mandatory_metadata_ok())



if __name__ == '__main__':
    unittest.main()



# TODO: test larger zim datasets
# https://wiki.kiwix.org/wiki/Content_in_all_languages
# https://wiki.openzim.org/wiki/Metadata

TEST_METADATA = { 
    # Mandatory
    "Name" : "wikipedia_fr_football",
    "Title": "English Wikipedia",
    "Creator": "English speaking Wikipedia contributors",
    "Publisher": "Wikipedia user Foobar",
    "Date": "2009-11-21",
    "Description": "All articles (without images) from the english Wikipedia",
    "Language": "eng",
    # Optional
    "Longdescription": "This ZIM file contains all articles (without images) from the english Wikipedia by 2009-11-10. The topics are ...",
    "Licence": "CC-BY",
    "Tags": "wikipedia;_category:wikipedia;_pictures:no;_videos:no;_details:yes;_ftindex:yes",
    "Flavour": "nopic",
    "Source": "https://en.wikipedia.org/",
    "Counter": "image/jpeg=5;image/gif=3;image/png=2",
    "Scraper": "mwoffliner 1.2.3"
}
