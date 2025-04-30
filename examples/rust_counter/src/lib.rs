use std::collections::HashMap;

wit_bindgen::generate!({
    path: "../../wit",
    world: "browser",
    with: {
        "wasi:io/poll@0.2.2": wasi::io::poll,
    },
});

use crate::webidl::browser::global;

struct MyComponent;

impl Guest for MyComponent {
    fn start() {
        let document = global::get_window().document().unwrap();
        let root = document.get_element_by_id("app").unwrap().as_html_element().unwrap();
        let root_styles = root.style();
        root_styles.set_property("display", "flex", None);
        root_styles.set_property("gap", "10px", None);

        // add elements
        let increase = document.create_element("button", None).as_html_button_element().unwrap();
        increase.set_text_content(Some("+"));
        root.append_child(&increase.as_node());
        let label = document.create_element("span", None).as_html_span_element().unwrap();
        label.set_text_content(Some("Counter: "));
        root.append_child(&label.as_node());
        let output = document.create_element("span", None).as_html_span_element().unwrap();
        root.append_child(&output.as_node());
        let decrease = document.create_element("button", None).as_html_button_element().unwrap();
        decrease.set_text_content(Some("-"));
        root.append_child(&decrease.as_node());

        // counter logic
        let mut i = 0;
        let mut events = HashMap::new();
        events.insert(
            Event::Increase,
            increase.onclick_subscribe(),
        );
        events.insert(
            Event::Decrease,
            decrease.onclick_subscribe(),
        );
        loop {
            output.set_text_content(Some(&i.to_string()));
            for event in block_on(&mut events) {
                match event {
                    Event::Increase => i += 1,
                    Event::Decrease => i -= 1,
                }
            }
        }
    }
}

#[derive(Clone, Hash, Eq, PartialEq, Debug)]
enum Event {
    Increase,
    Decrease,
}

fn block_on(events: &mut HashMap<Event, wasi::io::poll::Pollable>) -> Vec<Event> {
    let events_vec = events
        .iter()
        .collect::<Vec<(&Event, &wasi::io::poll::Pollable)>>();
    let pollables = events_vec.iter().map(|(_, p)| *p).collect::<Vec<_>>();

    let resolved_events = wasi::io::poll::poll(&pollables)
        .into_iter()
        .map(|i| events_vec[i as usize].0.clone())
        .collect::<Vec<Event>>();
    let mut output = vec![];
    for event in resolved_events {
        output.push(event);
    }
    output
}

export!(MyComponent);
