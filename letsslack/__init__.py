import re
import random

from letsslack.messages import initial_messages
from letsslack.utils import *

ACTION_ID_YES = "join_status_yes"
ACTION_ID_MAYBE = "join_status_maybe"
ACTION_ID_NO = "join_status_no"

JOIN_BLOCK_ID = "join"
MAYBE_BLOCK_ID = "maybe"
NOTJOIN_BLOCK_ID = "notjoin"

ALL_BLOCKS = (JOIN_BLOCK_ID, MAYBE_BLOCK_ID, NOTJOIN_BLOCK_ID)

def generate_init_message():
    return random.choice(initial_messages)

def get_new_event_payload(event_name, user_id):
    message = {
        "response_type": "in_channel",
        "blocks": [
            {
                "block_id": "header",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\"Let's *{event_name}*\" - <@{user_id}>. Would you like to join?",
                }
            },
            {
                "type": "divider"
            },
            {
                "block_id": f"{JOIN_BLOCK_ID}_header",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Katniss*",
                }
            },
            {
                "block_id": JOIN_BLOCK_ID,
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": generate_init_message(),
                }
            },
            {
                "block_id": f"{MAYBE_BLOCK_ID}_header",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Cat*",
                }
            },
            {
                "block_id": MAYBE_BLOCK_ID,
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": generate_init_message(),
                }
            },
            {
                "block_id": f"{NOTJOIN_BLOCK_ID}_header",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Nope*",
                }
            },
            {
                "block_id": NOTJOIN_BLOCK_ID,
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": generate_init_message(),
                }
            },
            {
                "block_id": "buttons",
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "action_id": ACTION_ID_YES,
                        "text": {
                            "type": "plain_text",
                            "text": "Join!",
                        },
                        "style": "primary",
                    },
                    {
                        "type": "button",
                        "action_id": ACTION_ID_MAYBE,
                        "text": {
                            "type": "plain_text",
                            "text": "Maybe~",
                        },
                    },
                    {
                        "type": "button",
                        "action_id": ACTION_ID_NO,
                        "text": {
                            "type": "plain_text",
                            "text": "No",
                        },
                        "style": "danger",
                    },
                ],
            },
        ],
    }
    return message

def create_user_list(user_ids):
    users = "\n".join(user_ids)
    return f"```\n{users}\n```"

def add_user_to_current_message(message, block_id, user_id):

    embed_user_id = f"<@{user_id}>"
    blocks = message["blocks"]
    filtered_blocks = [
        (idx, block) for idx, block in enumerate(blocks)
        if block["block_id"] in ALL_BLOCKS
    ]

    user_ids = []

    if len(filtered_blocks) != len(ALL_BLOCKS):
        raise Exception(f"Number of blocks do not match.")
    else:
        for idx, block in filtered_blocks:
            orig_text = block["text"]["text"]
            pattern = re.compile(r"<@[a-zA-Z0-9]+>")
            if "```" in orig_text:
                user_ids = pattern.findall(orig_text)
                if embed_user_id not in user_ids:
                    user_ids.append(embed_user_id)
            else:
                user_ids = [embed_user_id]

    join_block = {
        "block_id": block_id,
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{create_user_list(user_ids)}",
        }
    }
    message["blocks"][idx] = join_block
    return message

def add_joiner(message, user_id):
    return add_user_to_current_message(message, JOIN_BLOCK_ID, user_id)

def add_mayber(message, user_id):
    return add_user_to_current_message(message, MAYBE_BLOCK_ID, user_id)

def add_nojoiner(message, user_id):
    return add_user_to_current_message(message, NOTJOIN_BLOCK_ID, user_id)
