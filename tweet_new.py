import random

import psycopg2
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session
import json
import requests
import main
from rewrite import rewrite

conn = psycopg2.connect(
    "postgresql://bitmon:1JkSMTVAhO2wBTnx7Lk83w@poison-llama-8698.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")

styles = ["cute", "inflammatory", "serious"]
languages = ["English", "Chinese", "Japanese"]

token_url = "https://api.twitter.com/2/oauth2/token"
scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]
redirect_uri = ""


def get_tweets():  # id, content
    cur = conn.cursor()

    one_day_ago = datetime.now() - timedelta(days=1)

    query = """
    SELECT id, Content FROM Tweets
    WHERE IsTweet =0 AND CreatedAt < %s;
    """

    cur.execute(query, (one_day_ago))
    items = cur.fetchall()

    cur.close()

    return items


def get_kols():  # id, language, clientid, clientsecret, token
    cur = conn.cursor()

    for lan in languages:
        query = """
        SELECT ID, Lan, ClientID, ClientSecret, Token FROM BotKols
        WHERE Lan = %s
        ORDER BY RANDOM()
        LIMIT 5;
        """
        cur.execute(query, (lan,))

        # 获取并打印结果
        items = cur.fetchall()

        return items


tweets = get_tweets()
for tweet in tweets:
    content = tweet[1]

    kols = get_kols()
    for kol in kols:
        kol_id = kol[0]
        language = kol[1]
        style = random.randint(0, 2)
        re_content = rewrite(content, styles[style], language)
        payload = {"text": "{}".format(re_content)}
        client_id = kol[2]
        client_secret = kol[3]
        token_json = kol[4]
        bb_t = token_json.Decode("utf8").replace("'", '"')
        token = json.loads(bb_t)
        twitter = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
        refreshed_token = twitter.refresh_token(
            client_id=client_id,
            client_secret=client_secret,
            token_url=token_url,
            refresh_token=token["refresh_token"]
        )
        st_refreshed_token = '"{}"'.format(refreshed_token)
        j_refreshed_token = json.loads(st_refreshed_token)

        cur = conn.cursor()

        update_query = """
        UPDATE kol
        SET token = %s
        WHERE id = %s;
        """

        cur.execute(update_query, (j_refreshed_token, kol_id))
        conn.commit()
        cur.close()

        main.post_tweet(payload, refreshed_token)


cur = conn.cursor()
ids = [tweet[0] for tweet in tweets]  # 从查询结果中提取id

# 更新 IsTweet 状态
update_query = """
UPDATE Tweets
SET IsTweet = 1
WHERE id = ANY(%s);
"""

# 执行更新
cur.execute(update_query, (ids,))


conn.commit()
conn.close()