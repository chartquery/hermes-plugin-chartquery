"""Tool schemas (what the model reads) and how each tool maps to the API."""

# name: (description, JSON schema of the arguments, API path, {argument: API parameter}, fixed parameters)
TOOLS = {
    'chartquery_chart': (
        'Render a Chart.js v4 chart and return a public link to the image. Pass the full Chart.js config (type, data, options).',
        {
            "type": "object",
            "properties": {
                "config": {
                    "type": "object",
                    "description": "Chart.js v4 configuration object."
                }
            },
            "required": [
                "config"
            ]
        },
        '/v1/chart',
        {'config': 'query'},
        {'share': 'true'},
    ),
    'chartquery_chart_from_prompt': (
        'Describe a chart in plain English (and optionally pass raw data as CSV or JSON); ChartQuery builds it and returns a public link to the image.',
        {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "What to chart: type, data, labels, title (max 1000 characters)."
                },
                "raw_data": {
                    "type": "string",
                    "description": "Optional data as CSV or JSON."
                }
            },
            "required": [
                "prompt"
            ]
        },
        '/v1/chart/ai',
        {'prompt': 'prompt', 'raw_data': 'raw_data'},
        {'share': 'true'},
    ),
    'chartquery_qrcode': (
        'Generate a QR code and return a public link to the image.',
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Text or URL to encode."
                },
                "format": {
                    "type": "string",
                    "description": "Image format.",
                    "enum": [
                        "svg",
                        "png"
                    ]
                },
                "size": {
                    "type": "integer",
                    "description": "Size in pixels (default 200).",
                    "minimum": 50,
                    "maximum": 2000
                }
            },
            "required": [
                "data"
            ]
        },
        '/v1/qrcode',
        {'data': 'data', 'format': 'format', 'size': 'size'},
        {'share': 'true'},
    ),
    'chartquery_barcode': (
        'Generate a barcode (Code 128, EAN-13, UPC and more) and return a public link to the image.',
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Value to encode."
                },
                "type": {
                    "type": "string",
                    "description": "Barcode type, for example code128 (default), ean13 or upca."
                },
                "format": {
                    "type": "string",
                    "description": "Image format.",
                    "enum": [
                        "svg",
                        "png"
                    ]
                }
            },
            "required": [
                "data"
            ]
        },
        '/v1/barcode',
        {'data': 'data', 'type': 'type', 'format': 'format'},
        {'share': 'true'},
    ),
}
