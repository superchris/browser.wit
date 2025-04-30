import enum
from typing import Dict, List
import browser
from browser.imports.poll import Pollable, poll
from browser.imports.global_ import get_window

class Browser(browser.Browser):
    def start(self):
        document = get_window().document()
        root = document.get_element_by_id("app").as_html_element()
        root_styles = root.style()
        root_styles.set_property("display", "flex", None)
        root_styles.set_property("gap", "10px", None)

        # add elements
        increase = document.create_element("button", None).as_html_button_element()
        increase.set_text_content("+")
        root.append_child(increase.as_node())
        label = document.create_element("span", None).as_html_span_element()
        label.set_text_content("Counter: ")
        root.append_child(label.as_node())
        output = document.create_element("span", None).as_html_span_element()
        root.append_child(output.as_node())
        decrease = document.create_element("button", None).as_html_button_element()
        decrease.set_text_content("-")
        root.append_child(decrease.as_node())

        # counter logic
        i = 0
        events = {
            Event.INCREASE: increase.onclick_subscribe(),
            Event.DECREASE: decrease.onclick_subscribe(),
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
