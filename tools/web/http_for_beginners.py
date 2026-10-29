"""[EXTRA] HTTP requests from Python (and PowerShell example).

WHEN:
- You need to GET `/challenge` or `/login`.
- You need to POST JSON to `/vault` with `X-Signature` header.
- PowerShell keeps breaking the quotes in your JSON.

Never assume HTTP status alone means success. Read the response body.
401 often means missing/invalid authentication. 403 often means forbidden.
"""
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_url(url):
    # This follows ordinary HTTP redirects by default.
    request = Request(url, method="GET")
    return send_request(request)


def post_json(url, data, extra_headers=None):
    # Dict -> JSON bytes; this does NOT preserve duplicate keys.
    body = json.dumps(data, separators=(",", ":")).encode()
    headers = {"Content-Type": "application/json"}
    headers.update(extra_headers or {})
    return send_request(Request(url, data=body, headers=headers, method="POST"))


def post_exact_json_bytes(url, raw_bytes, extra_headers=None):
    # For JSON duplicate key experiments, use EXACT bytes, not Python dict!
    headers = {"Content-Type": "application/json"}
    headers.update(extra_headers or {})
    return send_request(Request(url, data=raw_bytes, headers=headers, method="POST"))


def send_request(request):
    try:
        response = urlopen(request, timeout=5)
    except HTTPError as problem:
        # Even HTTP 401/403 can contain a useful JSON error message.
        response = problem
    with response:
        result = response.read()
        print("HTTP STATUS:", response.status)
        print("BODY:", result.decode("utf-8", errors="replace"))
        return response.status, result


if __name__ == "__main__":
    print("PowerShell version that avoids quoting problems:")
    print('curl.exe -i "http://HOST:PORT/challenge"')
    print('curl.exe -i -X POST "http://HOST:PORT/vault" -H "Content-Type: application/json" --data-binary "@request.json"')
    print("Edit HOST, PORT and request.json. No network action is performed in this demo.")
