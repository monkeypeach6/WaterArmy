import base64
import hashlib
import os
import re
import json
import requests
from rewrite import rewrite
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session, TokenUpdated
from flask import Flask, request, redirect, session, url_for, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)

client_id = "SFA3WjhlbUJWaHpHcngyMUVlVko6MTpjaQ"
client_secret = "KbeekJ5cyciRFwfwJWWEOSldTBZEABtBWcRXGJ0WZeJKTv3lAQ"
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = "http://127.0.0.1:5000/oauth/callback"

scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

content = "We've identified an issue affecting new mining sessions and showing negative timers. Our team is actively working on a fix. In the meantime, try logging out and in to initiate a new session."
language = "Japanese"
style = "cute"
re_content = rewrite(content, style, language)


def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)


def post_tweet(payload, token):
    print("Tweeting!")
    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        },
    )


@app.route("/")
def demo():
    global twitter
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    st_token = '"{}"'.format(token)
    j_token = json.loads(st_token)
    filename = 'token.json'
    with open(filename, 'w') as file:
        json.dump(j_token, file)
    payload = {"text": "{}".format(re_content)}
    response = post_tweet(payload, token).json()
    return response


if __name__ == "__main__":
    app.run()
