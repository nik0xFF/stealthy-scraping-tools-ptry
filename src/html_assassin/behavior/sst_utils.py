import time
import os
import sys
import random
import math
import json
import subprocess
from logging import getLogger
from pathlib import Path
from html_assassin.behavior.cdp_wrapper import get_coordinates_matching_selector, evaluate_js
LOGGER = getLogger(__name__)


def goto(url):
    script_path = get_script_path("goto.js")
    cmd = f"node {script_path} '{url}'"
    sub_process = subprocess.check_output(cmd, shell=True)
    return sub_process


def get_script_path(name):
    return os.path.join(Path(__file__).parent.parent, "cdp/" + name)


def get_page_source():
    cmd = "node " + get_script_path("page_source.js")
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def get_coords(selector, randomize_within_bcr=True, highlight_bb=True):
    """

    :param selector: The CSS selector to get the coords for
    :param randomize_within_bcr: select a random coordinate within the bounding box height
    :param highlight_bb:  visually highlight the bounding box for debugging purposes
    :return:
    """

    coords = get_coordinates_matching_selector(selector)
    coords = coords.decode()

    try:
        parsed = json.loads(coords)
        x, y, width, height = (
            parsed["x"],
            parsed["y"],
            parsed["width"],
            parsed["height"],
        )

        if randomize_within_bcr:
            # print(x, y, parsed['width'], parsed['height'])
            x += random.randint(0, math.floor(parsed["width"] / 4))
            y += random.randint(0, math.floor(parsed["height"] / 4))

        if highlight_bb:
            # Just add a red thick border around the CSS selector
            cmd = (
                    """var el = document.querySelector('"""
                    + selector
                    + """'); if (el) { el.style.border = "2px solid #ff0000"; }"""
            )
            evaluate_js(cmd)

    except Exception as e:
        print("getCoords() failed with Error: {}".format(e))
        return None

    return x, y


def start_browser(
        args, start_in_temp_dir=False, chrome_profile='--profile-directory="Default"'
):
    temp_dir_str = ""
    if start_in_temp_dir:
        temp_dir_str = "--user-data-dir=/tmp"

    arg_str = " ".join(args)

    if os.getenv("DOCKER") == "1":
        start_cmd = (
            "google-chrome --remote-debugging-port=9222"
            " --no-sandbox --disable-notifications --start-maximized"
            " --no-first-run --no-default-browser-check 1 > ./logs/out.log 2 > ./logs/err.log &"
        )
    else:
        log_dir = os.getenv("LOG_DIRECTORY")
        if sys.platform == "darwin":
            # On MacOS Monterey, we need to start Google Chrome
            # in fullscreen mode to get the correct coordinates.
            chrome_path = "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome"
            start_cmd = (
                f"{chrome_path} --remote-debugging-port=9222 --start-maximized {temp_dir_str} {chrome_profile}"
                f" --disable-notifications --start-fullscreen {arg_str} 1> {log_dir}/out.log 2> {log_dir}/err.log &"
            )
        else:
            start_cmd = (
                f"google-chrome --remote-debugging-port=9222"
                f" --start-maximized --disable-notifications {arg_str} 1> {log_dir}out.log 2> {log_dir}err.log &"
            )

    LOGGER.debug(start_cmd)
    subprocess.Popen([start_cmd], shell=True)
    time.sleep(random.uniform(3, 4))


def close_browser():
    LOGGER.info("Closing browser")
    kill_chrome_cmd = ['killall', '-9']
    if sys.platform == "darwin":
        kill_chrome_cmd.append('Google Chrome')
    else:
        kill_chrome_cmd.append('chrome')

    subprocess.run(kill_chrome_cmd)
