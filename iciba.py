#!/usr/bin/env python2
# -*- coding: utf-8 -*-
''' Copyright 2015 dfshan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import argparse
import urllib2
import bs4
from bs4 import BeautifulSoup


def iciba(word):
    ''' Translate the word
    Args:
        word: A string representing the word to be translated

    Returns:
        A sequence of strings containing all translations
    '''
    result = []
    url = "http://www.iciba.com/" + word
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    base_trans = soup.find("ul", {"class": "base-list"})
    error_msg = "There is no translation..."
    if base_trans is None:
        return result
    exist_trans = False
    for item in base_trans.contents:
        if isinstance(item, bs4.element.NavigableString):
            content = item.string.strip()
            if content:
                result.append(content)
        elif isinstance(item, bs4.element.Tag):
            category = item.find("span", {"class": "prop"}).string
            trans = item.find("p").string
            if category is not None and trans is not None:
                result.append("%s %s" % (
                    category.strip(),
                    trans.strip().replace("                         ", " ")))
    return result


def main():
    parser = argparse.ArgumentParser(
            description="Translate by iCIBA (www.iciba.com)")
    parser.add_argument("word", help="The word to be translated")
    args = parser.parse_args()
    trans = iciba(args.word)
    if len(trans) == 0:
        print "Oh, there is no translation..."
    else:
        for item in trans:
            print item

if __name__ == "__main__":
    main()
