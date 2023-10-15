from logging import getLogger
from trio_cdp import runtime, browser, open_cdp, target, page, dom

LOGGER = getLogger(__name__)


async def test_open_url(url):
    async with open_cdp(url) as conn:
        # Find the first available target (usually a browser tab).
        targets = await target.get_targets()
        target_id = targets[0].target_id

        # Create a new session with the chosen target.
        async with conn.open_session(target_id) as session:

            await page.enable()
            async with session.wait_for(page.LoadEventFired):
                await page.navigate('https://www.itworks.com')

            # Extract the page title.
            root_node = await session.execute(dom.get_document())
            title_node_id = await session.execute(dom.query_selector(root_node.node_id, 'title'))
            html = await session.execute(dom.get_outer_html(title_node_id))
            print(html)


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
