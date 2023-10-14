"""
Very simple HTML crawl of a website.
"""

import random
import time
from logging import getLogger

from html_assassin.behavior.sst_utils import start_browser, get_coords, get_page_source, close_browser
from src.html_assassin.behavior.behavior import human_move

LOGGER = getLogger(__name__)


def main():
    print("Trying to start browser")
    start_browser(["https://www.homegate.ch/de\n"])

    # do a bit of random moving around
    # to fool bot systems
    coords = get_coords('[class="SearchBar_searchLayer_trzv7"]', highlight_bb=True)
    print("Clicking on coordinates " + str(coords))
    human_move(*coords)
    time.sleep(random.uniform(0.5, 1.0))

    # close the browser
    close_browser()


if __name__ == "__main__":
    main()
