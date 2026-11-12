"""Unit tests for the ChartQuery plugin. The network is mocked."""

import io
import json
import urllib.error

import hermes_plugin_chartquery as plugin
import pytest
from hermes_plugin_chartquery import _client


class FakeContext:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.providers, self.tools = [], {}

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def register_web_search_provider(self, provider):
        self.providers.append(provider)

    def register_tool(self, name, toolset, schema, handler, check_fn=None, **kwargs):
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler, "check_fn": check_fn}


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Calls(list):
    """Records each request and answers it with the payload given to respond()."""

    def __init__(self, monkeypatch):
        super().__init__()
        self.monkeypatch = monkeypatch

    def respond(self, payload):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            return FakeResponse(json.dumps(payload).encode())

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def fail(self, status, body):
        def urlopen(request, timeout):
            self.append({"request": request, "timeout": timeout})
            raise urllib.error.HTTPError(request.full_url, status, "error", {}, io.BytesIO(json.dumps(body).encode()))

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)

    def unreachable(self):
        def urlopen(request, timeout):
            raise urllib.error.URLError("down")

        self.monkeypatch.setattr(_client.urllib.request, "urlopen", urlopen)


@pytest.fixture
def calls(monkeypatch):
    return Calls(monkeypatch)


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: "test-key" if name == _client.KEY_ENV else default)


@pytest.fixture
def no_key(monkeypatch):
    monkeypatch.setattr(_client, "get_secret", lambda name, default=None: default)


def query(request):
    return dict(_client.urllib.parse.parse_qsl(_client.urllib.parse.urlsplit(request.full_url).query))


def assert_auth(request):
    assert request.get_header("User-agent").startswith("hermes-plugin-chartquery/")
    assert request.get_header("X-api-key") == "test-key"


def tools():
    ctx = FakeContext()
    plugin.register(ctx)
    return ctx.tools


def run(name, args):
    return json.loads(tools()[name]["handler"](args, task_id="t1"))


def test_register_declares_every_tool():
    registered = tools()
    assert sorted(registered) == sorted(['chartquery_chart', 'chartquery_chart_from_prompt', 'chartquery_qrcode', 'chartquery_barcode', 'chartquery_diagram', 'chartquery_diagram_from_prompt', 'chartquery_usage'])
    for name, tool in registered.items():
        assert tool["toolset"] == "chartquery"
        assert tool["schema"]["name"] == name
        assert tool["schema"]["parameters"]["type"] == "object"


def test_tools_hidden_without_key(no_key):
    assert all(tool["check_fn"]() is False for tool in tools().values())


def test_tools_shown_with_key(api_key):
    assert all(tool["check_fn"]() is True for tool in tools().values())


def test_missing_key_returns_an_error(no_key, calls):
    assert "CHARTQUERY_API_KEY" in run('chartquery_chart', {'config': {'type': 'bar', 'data': {'labels': ['a'], 'datasets': [{'data': [1]}]}}})["error"]
    assert calls == []


def test_missing_required_argument(api_key, calls):
    assert "required" in run('chartquery_chart', {})["error"]
    assert calls == []


@pytest.mark.parametrize("name,args,url", [('chartquery_chart', {'config': {'type': 'bar', 'data': {'labels': ['a'], 'datasets': [{'data': [1]}]}}}, 'https://api.chartquery.com/v1/chart?share=true&query=%7B%22type%22%3A%22bar%22%2C%22data%22%3A%7B%22labels%22%3A%5B%22a%22%5D%2C%22datasets%22%3A%5B%7B%22data%22%3A%5B1%5D%7D%5D%7D%7D'), ('chartquery_chart_from_prompt', {'prompt': 'Bar chart of sales by month', 'raw_data': 'Jan,1\nFeb,2'}, 'https://api.chartquery.com/v1/chart/ai?share=true&prompt=Bar+chart+of+sales+by+month&raw_data=Jan%2C1%0AFeb%2C2'), ('chartquery_qrcode', {'data': 'https://example.com', 'format': 'png', 'size': 300}, 'https://api.chartquery.com/v1/qrcode?share=true&data=https%3A%2F%2Fexample.com&format=png&size=300'), ('chartquery_barcode', {'data': 'https://example.com', 'type': 'ean13', 'format': 'png'}, 'https://api.chartquery.com/v1/barcode?share=true&data=https%3A%2F%2Fexample.com&type=ean13&format=png'), ('chartquery_diagram', {'source': 'graph TD; A-->B'}, 'https://api.chartquery.com/v1/diagram?share=true&type=mermaid&query=graph+TD%3B+A--%3EB'), ('chartquery_diagram', {'source': 'a -> b', 'language': 'd2', 'format': 'png'}, 'https://api.chartquery.com/v1/diagram?share=true&type=d2&query=a+-%3E+b&format=png'), ('chartquery_diagram_from_prompt', {'prompt': 'Login flow', 'language': 'plantuml', 'format': 'png'}, 'https://api.chartquery.com/v1/diagram/ai?share=true&prompt=Login+flow&diagram_type=plantuml&output_format=png'), ('chartquery_chart_from_prompt', {'prompt': 'Sales', 'legend': 'false', 'width': 800}, 'https://api.chartquery.com/v1/chart/ai?share=true&prompt=Sales&legend=false&width=800'), ('chartquery_usage', {}, 'https://api.chartquery.com/v1/usage')])
def test_each_tool_calls_its_endpoint(api_key, calls, name, args, url):
    calls.respond({"ok": True})
    assert run(name, args) == {"ok": True}
    request = calls[0]["request"]
    assert request.full_url == url
    assert request.get_method() == "GET"
    assert_auth(request)


def test_api_error_message_is_returned(api_key, calls):
    calls.fail(400, {'error': 'Invalid query'})
    assert run('chartquery_chart', {'config': {'type': 'bar', 'data': {'labels': ['a'], 'datasets': [{'data': [1]}]}}}) == {"error": "ChartQuery: Invalid query"}


def test_network_error(api_key, calls):
    calls.unreachable()
    assert run('chartquery_chart', {'config': {'type': 'bar', 'data': {'labels': ['a'], 'datasets': [{'data': [1]}]}}}) == {"error": "ChartQuery: could not reach the API"}


def test_manifest_lists_every_tool():
    from pathlib import Path

    manifest = (Path(__file__).resolve().parents[1] / "plugin.yaml").read_text()
    listed = {line.strip()[2:] for line in manifest.splitlines() if line.strip().startswith("- chartquery_")}
    assert listed == set(tools())
