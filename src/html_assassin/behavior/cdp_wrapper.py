from logging import getLogger
from typing import Tuple

from cdp import page, runtime, browser

LOGGER = getLogger(__name__)


def evaluate_js(script: str):
    evaluation_result = runtime.evaluate(script)
    LOGGER.info(evaluation_result)
    return evaluation_result


def get_coordinates_matching_selector(selector: str):
    ver = browser.get_version()
    LOGGER.info(browser.get_version())
    get_element_coordinates = f"""
        var selected_element_coordinates = document.querySelector('{selector}');
        if (selected_element_coordinates) {{return JSON.stringify(selected_element_coordinates.getClientRects()); }}
    """
    element_coordinates = evaluate_js(get_element_coordinates)


"""
async function getCoords(css_selector) {
    let client;
try {
// connect to endpoint
client = await CDP();
// extract domains
const { Page, Runtime, DOM } = client;
// enable events then start!
await Promise.all([Runtime.enable()]);

let result = null;
let clientRectCmd = `var targetCoordEl = document.querySelector('${css_selector}'); if (targetCoordEl) { JSON.stringify(targetCoordEl.getClientRects()); }`;

result = await Runtime.evaluate({
expression: clientRectCmd,
});

// get offset screen positioning
const screenPos = await Runtime.evaluate({
    expression: "JSON.stringify({offsetY: window.screen.height - window.innerHeight, offsetX: window.screen.width - window.innerWidth})"
});

let offset = JSON.parse(screenPos.result.value);
let clientRect = null;

try {
clientRect = JSON.parse(result.result.value)["0"];
} catch(err) {
return null;
}

let retVal =  {
x: offset.offsetX + clientRect.x,
y: offset.offsetY + clientRect.y,
width: clientRect.width,
height: clientRect.height,
};
console.log(JSON.stringify(retVal));
return retVal;
} catch (err) {
console.error(err);
} finally {
if (client) {
    await client.close();
}
}
}"""
