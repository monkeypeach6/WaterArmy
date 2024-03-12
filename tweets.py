import main
import json
client_id = "NlNDVzNobC1INFljZll3ZjFxZHk6MTpjaQ"
client_secret = "T4G1mwQ9862ljR96L9pIHWBQjMaYncSz65yzlzbeCUmIyM5ovM"

twitter = main.make_token()

token_url = "https://api.twitter.com/2/oauth2/token"

t = main.r.get("token")
bb_t = t.decode("utf8").replace("'", '"')
data = json.loads(bb_t)

refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"],
)

st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)

main.r.set("token", j_refreshed_token)
doggie_fact = main.parse_dog_fact()
payload = {"text": "{}".format(doggie_fact)}

main.post_tweet(payload, refreshed_token)