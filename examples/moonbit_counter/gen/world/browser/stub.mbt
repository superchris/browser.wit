// Generated by `wit-bindgen` 0.41.0.

pub fn start() -> Unit {
      let document = @global.get_window().document().unwrap()
      let root = document.get_element_by_id("app").unwrap().as_html_element().unwrap();
      let root_styles = root.style()
      root_styles.set_property("display", "flex", None);
      root_styles.set_property("gap", "10px", None);

      // add elements
      let increase = document.create_element("button", None).as_html_button_element().unwrap()
      increase.set_text_content(Some("+"))
      let _ = root.append_child(increase.as_node())
      let label = document.create_element("span", None).as_html_span_element().unwrap()
      label.set_text_content(Some("Counter: "))
      let _ = root.append_child(label.as_node())
      let output = document.create_element("span", None).as_html_span_element().unwrap()
      let _ = root.append_child(output.as_node())
      let decrease = document.create_element("button", None).as_html_button_element().unwrap()
      decrease.set_text_content(Some("-"))
      let _ = root.append_child(decrease.as_node())

      // counter logic
      let mut i = 0;
      let events: Map[Event, @poll.Pollable] = {}
      events.set(Event::Increase, increase.onclick_subscribe())
      events.set(Event::Decrease, decrease.onclick_subscribe())
      while true {
            output.set_text_content(Some(i.to_string()));
            for event in block_on(events) {
                  match event {
                        Event::Increase => i += 1;
                        Event::Decrease => i -= 1;
                  }
            }
      }
}

priv enum Event {
    Increase
    Decrease
} derive(Eq, Hash, Show)

fn block_on(events: Map[Event, @poll.Pollable]) -> Array[Event] {
      let events_vec: Array[(Event, @poll.Pollable)] = events.iter().to_array()
      let pollables: Array[@poll.Pollable] = events_vec.iter().map(fn { (_, p) => p }).collect();
      let output: Array[Event] = @poll.poll(pollables).iter().map(fn {(i) => events_vec[i.reinterpret_as_int()].0 }).to_array();
      output
}
