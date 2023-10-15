"""
Very simple HTML crawl of a website.
"""
import asyncio
import random
import time
from logging import getLogger

import trio

from html_assassin.behavior.cdp_wrapper import test_open_url
from html_assassin.behavior.sst_utils import start_browser, get_coords, get_page_source, close_browser
from src.html_assassin.behavior.behavior import human_move

LOGGER = getLogger(__name__)


def main():
    print("Trying to start browser")
    dev_tools_url = start_browser([])
    trio.run(test_open_url, *[dev_tools_url])

    close_browser()


if __name__ == "__main__":
    main()
