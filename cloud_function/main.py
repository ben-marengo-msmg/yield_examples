import base64


def main(request):
    payload_b64_encoded = request.get_json(silent=True)["message"]["data"]
    decoded = base64.b64decode(payload_b64_encoded)
    print(decoded)
    with open('request_payloads.jsonl', 'wb') as f:
        f.write(decoded)
