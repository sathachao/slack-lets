import os
import sys
import secrets
import json
from typing import Dict, Any, Text

import requests
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks
import uvicorn

import letsslack

try:
    SIGNING_SECRET = os.environ["SIGNING_SECRET"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    pass

async def respond_to_slack_response_url(response_url, payload: Dict[Text, Any]):
    # headers = {"Content-Type": "application/json"}
    resp = requests.post(response_url, json=payload)
    print(resp.content)

app = Starlette(debug=True)

@app.route("/", methods=["GET", "POST"])
async def hello(request):

    form = await request.form()
    user_id = form["user_id"]
    expd_name = form["text"]

    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> has created a new expedition *{expd_name}*. Would you like to join?",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Join! :disappointed:",
                        "emoji": True,
                        "style": "",
                    },
                    "value": "click_me_123"
                },
            },
        ]
    }
    tasks = BackgroundTasks()
    tasks.add_task(respond_to_slack_response_url, message)
    return JSONResponse(status_code=200, background=tasks)

@app.route("/new_expedition", methods=["POST"])
async def create_event(request):
    if not letsslack.validate_request(request, SIGNING_SECRET):
        return JSONResponse(status_code=401)

    form = await request.form()

    user_id = form["user_id"]
    event_name = form["text"]
    response_url = form["response_url"]

    payload = letsslack.get_new_event_payload(event_name, user_id)
    print(payload)

    return JSONResponse(payload, 200)

@app.route("/callback", methods=["POST"])
async def callback(request):
    # if not await letsslack.validate_request(request, SIGNING_SECRET):
    #     return JSONResponse(status_code=401)
    form = await request.form()
    actions = form["payload"]
    callback_info = json.loads(actions)
    print(callback_info)

    response_url = callback_info["response_url"]
    actions = callback_info["actions"]
    user_id = callback_info["user"]["id"]
    message = callback_info["message"]

    for action in actions:
        action_id = action["action_id"]
        if action_id == letsslack.ACTION_ID_YES:
            message = letsslack.add_joiner(message, user_id)
        elif action_id == letsslack.ACTION_ID_MAYBE:
            message = letsslack.add_mayber(message, user_id)
        elif action_id == letsslack.ACTION_ID_NO:
            message = letsslack.add_nojoiner(message, user_id)
        else:
            raise ValueError(f"Unknown action ID '{action_id}'")
    
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {BOT_TOKEN}"}
    response = requests.post(response_url, headers=headers, json=message)

    # TODO: Handle erroneous request
    print(response.status_code)
    print(response.content)

    return JSONResponse()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=6000)
