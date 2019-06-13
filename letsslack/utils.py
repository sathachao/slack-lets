import time
import hmac

import starlette.requests


async def validate_request(request: starlette.requests.Request, signing_secret: bytes):
    timestamp = request.headers["X-Slack-Request-Timestamp"]

    if abs(time.time() - float(timestamp)) > 60:
        return False

    body = await request.body()

    sig_basestring = f"v0:{timestamp}:{body}"
    hex_digest = hmac.digest(signing_secret, sig_basestring, "sha256").hexdigest()
    sig = f"v0={hex_digest}"

    slack_signature = request.headers["X-Slack-Signature"]
    return True if hmac.compare_digest(sig, slack_signature) else False
