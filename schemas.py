"""Tool schemas (what the model reads) and how each tool maps to the API."""

# name: (description, JSON schema of the arguments, API path, {argument: API parameter}, fixed parameters)
TOOLS = {
    'chartquery_chart': (
        'Render a Chart.js v4 chart (bar, line, pie, doughnut, radar, scatter, bubble, polarArea, mixed) from its full config and return public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 5 credits per call.',
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
        "Describe a chart in plain words, optionally with the raw data as CSV, JSON or text (Jan: 12400, Feb: 18900…); ChartQuery's AI picks the chart type, builds it and returns public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 10 credits per call.",
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
                },
                "title": {
                    "type": "string",
                    "description": "Chart title, instead of the one the AI picks."
                },
                "subtitle": {
                    "type": "string",
                    "description": "Chart subtitle."
                },
                "legend": {
                    "type": "string",
                    "enum": [
                        "top",
                        "bottom",
                        "left",
                        "right",
                        "chartArea",
                        "false"
                    ],
                    "description": "Legend position, or false to hide it. Default: top."
                },
                "format": {
                    "type": "string",
                    "enum": [
                        "png",
                        "svg"
                    ],
                    "description": "Image format. Default: png."
                },
                "width": {
                    "type": "integer",
                    "minimum": 50,
                    "maximum": 4000,
                    "description": "Image width in pixels. Default: 1200."
                },
                "height": {
                    "type": "integer",
                    "minimum": 50,
                    "maximum": 4000,
                    "description": "Image height in pixels. Default: 600."
                },
                "background": {
                    "type": "string",
                    "description": "Background color as hex, for example #ffffff (default) or #0f172a."
                }
            },
            "required": [
                "prompt"
            ]
        },
        '/v1/chart/ai',
        {'prompt': 'prompt', 'raw_data': 'raw_data', 'title': 'title', 'subtitle': 'subtitle', 'legend': 'legend', 'format': 'format', 'width': 'width', 'height': 'height', 'background': 'background'},
        {'share': 'true'},
    ),
    'chartquery_qrcode': (
        'Generate a QR code for a URL, email, phone number, Wi-Fi network or any text, with custom colors and dot styles, and return public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 3 credits per call.',
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Text to encode: a URL, mailto:, tel:, SMSTO:, a WIFI:T:WPA;S:<network>;P:<password>;; string, or any text."
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
                },
                "color": {
                    "type": "string",
                    "description": "Dot color as hex, for example #6366f1. Default: #000."
                },
                "background": {
                    "type": "string",
                    "description": "Background color as hex, or transparent. Default: #fff."
                },
                "dot_type": {
                    "type": "string",
                    "enum": [
                        "square",
                        "rounded",
                        "dots",
                        "diamond",
                        "classy",
                        "classy-rounded",
                        "extra-rounded",
                        "vertical-line",
                        "horizontal-line",
                        "small-square",
                        "tiny-square"
                    ],
                    "description": "Dot style. Default: square."
                },
                "shape": {
                    "type": "string",
                    "enum": [
                        "square",
                        "circle"
                    ],
                    "description": "Overall shape: square (default) or circle."
                },
                "ec_level": {
                    "type": "string",
                    "enum": [
                        "L",
                        "M",
                        "Q",
                        "H"
                    ],
                    "description": "Error correction: L (7%), M (15%, default), Q (25%) or H (30%, still readable with a logo on top)."
                },
                "margin": {
                    "type": "integer",
                    "description": "Quiet zone around the code, in modules. Default: 4."
                }
            },
            "required": [
                "data"
            ]
        },
        '/v1/qrcode',
        {'data': 'data', 'format': 'format', 'size': 'size', 'color': 'color', 'background': 'background', 'dot_type': 'dot_type', 'shape': 'shape', 'ec_level': 'ec_level', 'margin': 'margin'},
        {'share': 'true'},
    ),
    'chartquery_barcode': (
        'Generate a barcode (EAN-13, UPC-A, Code 128, ITF-14, GS1-128 and 20 more types) and return public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 3 credits per call.',
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Value to encode."
                },
                "type": {
                    "type": "string",
                    "enum": [
                        "code128",
                        "code39",
                        "code39ext",
                        "code93",
                        "code93ext",
                        "ean13",
                        "ean8",
                        "ean5",
                        "ean2",
                        "upca",
                        "upce",
                        "itf",
                        "itf14",
                        "codabar",
                        "msi",
                        "pharmacode",
                        "code11",
                        "gs1-128",
                        "gs1-databar",
                        "gs1-databar-limited",
                        "gs1-databar-expanded",
                        "identcode",
                        "leitcode",
                        "postnet",
                        "planet",
                        "plessey"
                    ],
                    "description": "Barcode type. Retail: ean13, ean8, upca, upce. General: code128 (default), code39, code93. Logistics: itf14, gs1-128."
                },
                "format": {
                    "type": "string",
                    "description": "Image format.",
                    "enum": [
                        "svg",
                        "png"
                    ]
                },
                "show_text": {
                    "type": "boolean",
                    "description": "Print the value under the bars."
                },
                "height": {
                    "type": "integer",
                    "description": "Bar height in pixels. Default: 80."
                },
                "color": {
                    "type": "string",
                    "description": "Bar color as hex. Default: #000."
                },
                "background": {
                    "type": "string",
                    "description": "Background color as hex, or transparent. Default: #fff."
                },
                "rotation": {
                    "type": "integer",
                    "enum": [
                        0,
                        90,
                        180,
                        270
                    ],
                    "description": "Rotation in degrees. Default: 0."
                }
            },
            "required": [
                "data"
            ]
        },
        '/v1/barcode',
        {'data': 'data', 'type': 'type', 'format': 'format', 'show_text': 'show_text', 'height': 'height', 'color': 'color', 'background': 'background', 'rotation': 'rotation'},
        {'share': 'true'},
    ),
    'chartquery_diagram': (
        'Render a diagram from its source code: Mermaid (flowcharts, sequence, class, state, Gantt, ER), D2, PlantUML, Graphviz, BPMN, DBML, Excalidraw, Vega-Lite and 20 more languages. Returns public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 5 credits per call.',
        {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Diagram source code, for example: graph TD; A[Start] --> B{OK?}; B -->|yes| C[End]"
                },
                "language": {
                    "type": "string",
                    "enum": [
                        "mermaid",
                        "graphviz",
                        "plantuml",
                        "d2",
                        "svgbob",
                        "nomnoml",
                        "blockdiag",
                        "seqdiag",
                        "actdiag",
                        "nwdiag",
                        "bpmn",
                        "erd",
                        "excalidraw",
                        "ditaa",
                        "vega",
                        "vegalite",
                        "wavedrom",
                        "wireviz",
                        "c4plantuml",
                        "structurizr",
                        "tikz",
                        "pikchr",
                        "umlet",
                        "symbolator",
                        "packetdiag",
                        "rackdiag",
                        "bytefield",
                        "dbml"
                    ],
                    "description": "Diagram language. Default: mermaid."
                },
                "format": {
                    "type": "string",
                    "enum": [
                        "svg",
                        "png",
                        "jpeg",
                        "pdf"
                    ],
                    "description": "Image format. Default: svg; png displays everywhere."
                }
            },
            "required": [
                "source"
            ]
        },
        '/v1/diagram',
        {'source': 'query', 'language': 'type', 'format': 'format'},
        {'share': 'true', 'type': 'mermaid'},
    ),
    'chartquery_diagram_from_prompt': (
        "Describe a diagram in plain words (a process, an architecture, a sequence of calls, a database schema); ChartQuery's AI writes it in Mermaid, D2, PlantUML or Graphviz and returns public links to the image. Returns JSON with render_url (the image), view_url (a page to open), embed_url (HTML to embed) and expires_in. Costs 10 credits per call.",
        {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "What to draw: the kind of diagram, the entities and how they connect (max 1000 characters)."
                },
                "language": {
                    "type": "string",
                    "enum": [
                        "mermaid",
                        "d2",
                        "plantuml",
                        "graphviz"
                    ],
                    "description": "Preferred diagram language. The AI chooses when omitted."
                },
                "format": {
                    "type": "string",
                    "enum": [
                        "svg",
                        "png",
                        "jpeg",
                        "pdf"
                    ],
                    "description": "Image format. Default: svg; png displays everywhere."
                }
            },
            "required": [
                "prompt"
            ]
        },
        '/v1/diagram/ai',
        {'prompt': 'prompt', 'language': 'diagram_type', 'format': 'output_format'},
        {'share': 'true'},
    ),
    'chartquery_usage': (
        'Your ChartQuery account: plan, credits used, credits left, renewal date and rate limit. Free.',
        {
            "type": "object",
            "properties": {},
            "required": []
        },
        '/v1/usage',
        {},
        {},
    ),
}
