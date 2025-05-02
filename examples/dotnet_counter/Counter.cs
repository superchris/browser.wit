namespace BrowserWorld;

using BrowserWorld.wit.imports.webidl.browser;
using BrowserWorld.wit.imports.wasi.io.v0_2_2;

public class BrowserWorldImpl : IBrowserWorld
{
    public static void Start()
    {
        var document = GlobalInterop.GetWindow().Document()!;
        var root = document.GetElementById("app")!.AsHtmlElement()!;
        var root_styles = root.Style();
        root_styles.SetProperty("display", "flex", null);
        root_styles.SetProperty("gap", "10px", null);

        // add elements
        var increase = document.CreateElement("button", null).AsHtmlButtonElement()!;
        increase.SetTextContent("+");
        root.AppendChild(increase.AsNode());
        var label = document.CreateElement("span", null).AsHtmlSpanElement()!;
        label.SetTextContent("Counter: ");
        root.AppendChild(label.AsNode());
        var output = document.CreateElement("span", null).AsHtmlSpanElement()!;
        root.AppendChild(output.AsNode());
        var decrease = document.CreateElement("button", null).AsHtmlButtonElement()!;
        decrease.SetTextContent("-");
        root.AppendChild(decrease.AsNode());

        // counter logic
        var i = 0;
        var events = new Dictionary<Event, IPoll.Pollable>
        {
            { Event.Increase, increase.AsHtmlElement()!.OnclickSubscribe() },
            { Event.Decrease, decrease.AsHtmlElement()!.OnclickSubscribe() },
        };
        while (true)
        {
            output?.SetTextContent(i.ToString());
            foreach (var e in BlockOn(events))
            {
                switch (e)
                {
                    case Event.Increase:
                        i += 1;
                        break;
                    case Event.Decrease:
                        i -= 1;
                        break;
                }
            }
        }
    }

    static List<Event> BlockOn(Dictionary<Event, IPoll.Pollable> events) {
        var events_vec = new List<(Event, IPoll.Pollable)>();
        foreach (var (e, p) in events)
        {
            events_vec.Add((e, p));
        }

        var pollables = new List<IPoll.Pollable>();
        foreach (var (_, pollable) in events_vec)
        {
            pollables.Add(pollable);
        }

        var resolved_events = new List<Event>();
        foreach (var i in PollInterop.Poll(pollables))
        {
            resolved_events.Add(events_vec[(int)i].Item1);
        }

        return resolved_events;
    }
}

enum Event {
    Increase,
    Decrease,
}
