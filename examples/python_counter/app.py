import enum
from typing import Dict, List
import browser
from browser.imports.poll import Pollable, poll
from browser.imports.global_ import get_window

class Browser(browser.Browser):
    def start(self):
        document = get_window().document()
        root = document.get_element_by_id("app").as_node()
        root_styles = root.as_element().as_html_element().style()
        root_styles.set_property("display", "flex", None)
        root_styles.set_property("gap", "10px", None)

        # add elements
        increase = document.create_element("button", None)
        increase.as_node().set_text_content("+")
        root.append_child(increase.as_node())
        label = document.create_element("span", None).as_node()
        label.set_text_content("Counter: ")
        root.append_child(label)
        output = document.create_element("span", None).as_node()
        root.append_child(output)
        decrease = document.create_element("button", None)
        decrease.as_node().set_text_content("-")
        root.append_child(decrease.as_node())

        # counter logic
        i = 0
        events = {
            Event.INCREASE: increase.as_html_element().onclick_subscribe(),
            Event.DECREASE: decrease.as_html_element().onclick_subscribe(),
        }
        while True:
            output.set_text_content(str(i))
            for event in block_on(events):
                match event:
                    case Event.INCREASE:
                        i += 1
                    case Event.DECREASE:
                        i -= 1


class Event(enum.Enum):
    INCREASE = 1,
    DECREASE = 2,

def block_on(events: Dict[Event, Pollable]) -> List[Event]:
    events_vec = list(events.keys())
    output = []
    for i in poll(list(events.values())):
        output.append(events_vec[i])
    return output
