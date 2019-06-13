# Let's

Let's, at its core, is intended to be a sandbox project for me to experiment with Slack API.
Let's basically provides commands for announcing activities or events, and asking for responses from people on Slack.

## Dependencies

- Python 3.6+
- Pipenv (optional)

## Installation

### Using Virtualenv

```sh
pip install -r requirements.txt
```

### Using Pipenv

```sh
pipenv install
```

## Usage

**CAUTION**: Let's is still under heavy development, hence there may still be a lot of uninteded behaviours \
\
For local deployment, it is suggested to use accessible tools for exposing local servers, e.g., [Serveo](https://serveo.net/), or [ngrok](https://ngrok.com/).

### Using Serveo

```sh
# Start Let's server

SIGNING_SECRET="YOUR SLACK APP'S SIGNING SECRET"
BOT_TOKEN="YOUR SLACK APP'S BOT TOKEN"

python main.py # App will run on localhost:6000

# ---
# Start another terminal and run these

SUBDOMAIN="subdomainyouwant"

# If your requested subdomain already exists, just use another subdomain.
ssh -R $SUBDOMAIN:443:localhost:6000 serveo.net
```
