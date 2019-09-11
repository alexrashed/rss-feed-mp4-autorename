#!/usr/bin/env python3
import logging
import os
import re
import string
import feedparser
import time
import sys


def regex_glob(exp):
    m = re.compile(exp)
    return [f for f in os.listdir('./') if m.search(f)]


def format_title(title):
    title = title.replace(': ', ' - ')
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(char for char in title if char in valid_chars)


def get_new_filename(parsed_feed, old_filename):
    entry = next(iter([entry for entry in parsed_feed.entries if len([link for link in entry.links if link.href.endswith(old_filename)]) > 0]), None)
    new_filename = None
    if entry is not None:
        title = entry.title
        title_formatted = format_title(title)
        published = entry.published_parsed
        published_formatted = time.strftime('%Y-%m-%d - %H%M', published)
        new_filename = '%s - %s.mp4' % (published_formatted, title_formatted)
    return new_filename


def main():
    feed_url = sys.argv[1]
    old_filenames = regex_glob(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{4}_.*\.mp4$')
    if len(old_filenames) > 0:
        logging.info('Downloading feed from URL %s' % feed_url)
        parsed_feed = feedparser.parse(feed_url)
        for old_filename in old_filenames:
            new_filename = get_new_filename(parsed_feed, old_filename)
            if new_filename is not None:
                logging.info('Renaming %s to %s.' % (old_filename, new_filename))
                os.rename(old_filename, new_filename)


if __name__ == '__main__':
    main()
