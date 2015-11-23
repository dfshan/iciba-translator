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


def pronounce(soup):
    ''' Find the pronounce of the word
    Args:
        bs: A BeautifulSoup object containing the page of word tranlation

    Returns:
        A string containing pronounce
    '''
    result = "Pronounce: "
    prons = soup.find("div", {"class": "base-speak"})
    if prons is None:
        return ""
    for pron in prons.find_all("span"):
        result += pron.string + " "
    return result

def basic_trans(soup):
    ''' Find the basic translation
    Args:
        bs: A BeautifulSoup object containing the page of word tranlation

    Returns:
        A sequence of strings containing all translations
    '''
    result = [u"基本释义:", ]
    base_trans = soup.find("ul", {"class": "base-list"})
    if base_trans is None:
        return result
    exist_trans = False
    for item in base_trans.contents:
        if isinstance(item, bs4.element.NavigableString):
            content = item.string.strip()
            if content:
                result.append(content)
        elif isinstance(item, bs4.element.Tag):
            category = item.find("span", {"class": "prop"})
            trans = item.find("p")
            if category is not None and trans is not None:
                if "chinese" in category["class"]:
                    result.append("%s: %s %s" % (
                        category.string.strip(),
                        trans.find("span").string,
                        trans.find("a").string))
                else:
                    result.append("%s %s" % (
                        category.string.strip(),
                        trans.string.strip().replace(
                            "                         ",
                            " ")))
    return result


def example_article(soup):
    ''' Find the example articles
    Args:
        bs: A BeautifulSoup object containing the page of word tranlation

    Returns:
        A sequence of dicts containing all articles by english, chinese, and from
    '''
    result = []
    articles = soup.find("div", {"class": "info-article article-tab"})
    if articles is None:
        return result
    for section in articles.find_all("div", {"class": "section-p"}):
        english = section.find("p", {"class": "p-english"}).contents[0]
        chinese = section.find("p", {"class": "p-chinese"}).string
        from_where = section.find("p", {"class": "p-from"}).string
        result.append({
            "english": english,
            "chinese": chinese,
            "from": from_where})
    return result

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
    result.extend([pronounce(soup), ""])
    result.extend(basic_trans(soup))
    result.extend(["", u"例句："])
    for item in example_article(soup):
        if item["english"] is not None:
            result.append(item["english"])
        if item["chinese"] is not None:
            result.append(item["chinese"])
        if item["from"] is not None:
            result.append(item["from"])
        result.append("")
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
