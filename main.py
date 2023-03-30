#!/usr/bin/python3

# This is a script to convert an exported Notion Page (with subpages) in Markdown
# to a Notion Database. I needed this because I had been using the Notion Chrome
# extension to dump a bunch of URLs into a Notion "page", but decided later I wanted
# them in a structured Notion database. This tool reads a directory of Markdown files
# exported from a Notion page and stuffs the title and URL of each page into a
# Notion database.

import notion_client

import os
import re
from os import listdir
from os.path import isfile, join


# Dump of the original reading list page.
INDIR = "/Users/mdw/Downloads/f/Reading List 910f30d459cc4c4ca0d087c70aef2f32"

# The Notion database to import into.
DATABASE = "b264de3998384f839245bd54faa40d9c"

client = notion_client.Client(auth=os.environ["NOTION_TOKEN"])

files = [f for f in listdir(INDIR) if isfile(join(INDIR, f))]

pages = []

for file in files:
    with open(os.path.join(INDIR, file), "r") as infile:
        title_line = infile.readline()
        blank = infile.readline()
        url_line = infile.readline()

        m = re.match(r"# (.*)", title_line)
        if not m:
            print(f"WARNING: No title found in {file}")
        title = m.group(1)

        m = re.match(r"\[(.*)\]", url_line)
        if not m:
            print(f"WARNING: No URL found in {file}")
            continue
        url = m.group(1)

        pages.append((title, url))

for title, url in pages:
    print(f"Adding {title}...")
    new_page = {
        "Title": {"title": [{"text": {"content": title}}]},
        "URL": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": url},
                },
            ],
        },
    }
    client.pages.create(parent={"database_id": DATABASE}, properties=new_page)
