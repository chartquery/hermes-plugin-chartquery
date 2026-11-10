# ChartQuery for Hermes Agent

Gives [Hermes Agent](https://hermes-agent.nousresearch.com) tools to render charts, QR codes and barcodes as shareable images, through the ChartQuery API.

## Install

```sh
hermes plugins install chartquery
```

Hermes asks for `CHARTQUERY_API_KEY` during the install. Create a key in the [ChartQuery dashboard](https://app.chartquery.com).

## Tools

| Tool | What it does |
|---|---|
| `chartquery_chart` | Render a Chart.js v4 chart and return a public link to the image. Pass the full Chart.js config (type, data, options). |
| `chartquery_chart_from_prompt` | Describe a chart in plain English (and optionally pass raw data as CSV or JSON); ChartQuery builds it and returns a public link to the image. |
| `chartquery_qrcode` | Generate a QR code and return a public link to the image. |
| `chartquery_barcode` | Generate a barcode (Code 128, EAN-13, UPC and more) and return a public link to the image. |

The tools are hidden from the model until the API key is set.

## What it does on your machine

- **Network:** calls `https://api.chartquery.com` only, with your `CHARTQUERY_API_KEY`. Calls can use credits on your ChartQuery account ([pricing](https://www.chartquery.com/pricing)).
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
