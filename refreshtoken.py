import random

import psycopg2
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session
import json
import requests
import main
from rewrite import rewrite

conn = psycopg2.connect(
    "postgresql://salad:k5OopjkJaAZeWTYoy0eD3g@bitmon-8883.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")

cur = conn.cursor()

cur.execute('SELECT tweet_id FROM "Tweets"')

tables = cur.fetchall()

print(tables)
