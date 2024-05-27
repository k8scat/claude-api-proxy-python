from flask import Flask, request, Response, redirect
import requests
import re

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        return Response(None, status=204, headers=CORS_HEADERS)
    
    if path == "":
        return redirect("https://api.0pena1.com/", code=301)

    upstream_url = f'https://api.anthropic.com/{path}'
    headers = pick_headers(request.headers, ['content-type', 'x-api-key', 'accept-encoding', 'anthropic-version'])
    headers.update(CORS_HEADERS)
    
    response = requests.request(
        method=request.method,
        url=upstream_url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
        allow_redirects=False,
        stream=True
    )

    response_headers = remove_content_encoding(response.headers.copy())
    
    return Response(
        response.iter_content(chunk_size=1024),
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        headers=response_headers
    )

def pick_headers(headers, keys):
    picked_headers = {}
    for key in headers:
        if any(key == k or (isinstance(k, re.Pattern) and k.match(key)) for k in keys):
            picked_headers[key] = headers[key]
    return picked_headers

def remove_content_encoding(headers):
    headers.pop('content-encoding', None)
    return headers

if __name__ == '__main__':
    app.run(port=80)