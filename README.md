# ChartQuery for Hermes Agent

Charts, diagrams, QR codes and barcodes for [Hermes Agent](https://hermes-agent.nousresearch.com), through the [ChartQuery](https://www.chartquery.com) API.

- **Charts** from a Chart.js config, or from a sentence and some raw data: ChartQuery's AI picks the chart type and builds it.
- **Diagrams** from Mermaid, D2, PlantUML, Graphviz and 24 more languages, or from a plain-words description.
- **QR codes** for links, emails, phone numbers and Wi-Fi networks, with colors and dot styles, and **barcodes** in 26 formats (EAN-13, UPC-A, Code 128, ITF-14, GS1-128…).

Every tool returns public links to the image, so Hermes can show it in the chat, send it on Telegram or Discord, or paste it in a document.

## Contents

- [Install](#install)
- [How it works](#how-it-works)
- [Tools](#tools)
- [Charts](#charts)
- [Diagrams](#diagrams)
- [QR codes and barcodes](#qr-codes-and-barcodes)
- [Example prompts](#example-prompts)
- [Credits and errors](#credits-and-errors)
- [What it does on your machine](#what-it-does-on-your-machine)

## Install

```sh
hermes plugins install chartquery
```

Hermes asks for `CHARTQUERY_API_KEY` during the install. Create a key in the [ChartQuery dashboard](https://app.chartquery.com).

Answer yes to `Enable 'chartquery' now?`, or run `hermes plugins enable chartquery` later. The tools join the `chartquery` toolset, which is on by default; turn it on or off in `hermes tools` like any other toolset. They stay hidden from the model until the API key is set.

## How it works

Each tool is one HTTPS call to `https://api.chartquery.com`, authenticated with your key. ChartQuery renders the image on its side, stores it and answers with links:

```json
{
  "id": "cq-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "render_url": "https://api.chartquery.com/v1/chart/render/cq-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "view_url": "https://api.chartquery.com/v1/chart/view/cq-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "embed_url": "<iframe src=\"https://api.chartquery.com/v1/chart/view/cq-…\" width=\"600\" height=\"400\"></iframe>",
  "expires_in": "3 days"
}
```

- `render_url` is the image itself: put it in a message, an `<img>` tag or a Markdown document.
- `view_url` is a page that shows the image, to open in a browser.
- `embed_url` is an `<iframe>` to embed it in a web page.
- `expires_in` says how long the links work: 3 days on the free plan (with a watermark), 6 months on paid plans.

Nothing is downloaded to your machine: the model gets the links and passes them on.

## Tools

| Tool | What it makes | Input | Credits |
|---|---|---|---|
| `chartquery_chart` | A Chart.js v4 chart (bar, line, pie, doughnut, radar, scatter, bubble, polar area, mixed) from its full config. | `config` | 5 |
| `chartquery_chart_from_prompt` | A chart from a description and optional raw data (CSV, JSON or text). The AI picks the type, colors and layout. | `prompt` | 10 |
| `chartquery_diagram` | A diagram from its source code in one of 28 languages. | `source` | 5 |
| `chartquery_diagram_from_prompt` | A diagram from a description. The AI writes it in Mermaid, D2, PlantUML or Graphviz. | `prompt` | 10 |
| `chartquery_qrcode` | A QR code, with colors, dot style, round shape and error correction. | `data` | 3 |
| `chartquery_barcode` | A barcode in one of 26 formats, with or without the value printed under it. | `data` | 3 |
| `chartquery_usage` | Your plan, credits used, credits left, renewal date and rate limit. | none | free |

## Charts

Two ways to make a chart:

- **`chartquery_chart`** takes a full [Chart.js v4](https://www.chartjs.org/docs/latest/) config. Use it when you know exactly what you want, or when the data comes from a tool and must be drawn as is:

  ```json
  {
    "type": "bar",
    "data": {
      "labels": ["Jan", "Feb", "Mar"],
      "datasets": [{"label": "Revenue", "data": [12400, 18900, 15200]}]
    },
    "options": {"plugins": {"title": {"display": true, "text": "Q1 revenue"}}}
  }
  ```

- **`chartquery_chart_from_prompt`** takes a sentence such as "line chart of monthly signups in 2026, blue, with the average as a dashed line" and the raw data in `raw_data`. Set `title`, `subtitle`, `legend`, `width`, `height`, `background` or `format` to override what the AI chose.

## Diagrams

`chartquery_diagram` renders source code. `language` is `mermaid` by default; the others are `d2`, `plantuml`, `c4plantuml`, `graphviz`, `bpmn`, `dbml`, `erd`, `excalidraw`, `nomnoml`, `structurizr`, `svgbob`, `ditaa`, `pikchr`, `tikz`, `vega`, `vegalite`, `wavedrom`, `wireviz`, `umlet`, `symbolator`, `blockdiag`, `seqdiag`, `actdiag`, `nwdiag`, `packetdiag`, `rackdiag` and `bytefield`.

```
graph TD
  A[Order placed] --> B{Paid?}
  B -->|yes| C[Ship]
  B -->|no| D[Send reminder]
```

`chartquery_diagram_from_prompt` writes the source for you from a description such as "sequence diagram of an OAuth login between the browser, our API and Google". Set `language` to choose the diagram language, or leave it to the AI.

Both take `format`: `svg` (default, sharp at any size), `png` (shows everywhere, including chat apps), `jpeg` or `pdf`.

## QR codes and barcodes

`chartquery_qrcode` encodes any text. Common forms:

| Content | `data` |
|---|---|
| A link | `https://example.com` |
| An email | `mailto:hello@example.com` |
| A phone number | `tel:+33612345678` |
| A text message | `SMSTO:+33612345678:Hello` |
| A Wi-Fi network | `WIFI:T:WPA;S:MyNetwork;P:my-password;;` |

Style it with `color`, `background` (or `transparent`), `dot_type` (`rounded`, `dots`, `classy`…), `shape: circle`, `size` and `margin`. Use `ec_level: H` when a logo will cover part of the code.

`chartquery_barcode` takes the value and a `type`: `ean13`, `ean8`, `upca`, `upce` for retail products, `code128` (default), `code39`, `code93` for general use, `itf14` and `gs1-128` for logistics, and 17 more. `show_text` prints the value under the bars; `height`, `color`, `background` and `rotation` adjust the look.

## Example prompts

- "Make a bar chart of our monthly revenue: Jan 12,400, Feb 18,900, Mar 15,200."
- "Turn this CSV into the chart that fits best and send it to me."
- "Draw the architecture of our app as a diagram: browser, API gateway, three services and Postgres."
- "Render this Mermaid flowchart as a PNG."
- "Make a sequence diagram of a Stripe checkout."
- "Create a round QR code with blue dots that opens https://example.com/menu."
- "Make a QR code that joins my Wi-Fi network 'Office' with the password I gave you."
- "Generate EAN-13 barcodes for these five products, with the number under the bars."

## Credits and errors

- Credits per call: 5 for a chart or diagram from code, 10 when the AI builds it from a prompt, 3 for a QR code or barcode; `chartquery_usage` is free. The cost is at the end of each tool's description, so the model knows it before it calls. Plans and prices: [chartquery.com/pricing](https://www.chartquery.com/pricing).
- Errors come back to the model as `{"error": "ChartQuery: <message>"}` with the API's own message (invalid key, no credits left, invalid chart config or diagram syntax), so it can fix the input and try again.
- Calls time out after 60 seconds.

## What it does on your machine

- **Network:** calls `https://api.chartquery.com` only, with your `CHARTQUERY_API_KEY`. Calls use credits on your ChartQuery account. The data you chart is sent to ChartQuery, and the images are stored there behind public links until they expire.
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed.

## Contact

- Source: https://github.com/chartquery/hermes-plugin-chartquery
- ChartQuery: https://www.chartquery.com
- Issues: https://github.com/chartquery/hermes-plugin-chartquery/issues

## License

MIT
