import requests
import hashlib
from datetime import timedelta
from redis_rate_limit import RateLimit, TooManyRequests

from ..internals.cache.redis import get_conn

from flask import current_app

def is_password_compromised(password):
    h = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five = h[0:5]
    rest = h[5:]

    try:
        resp = requests.get('https://api.pwnedpasswords.com/range/' + first_five)
        if rest in resp.text:
            return True
    except Exception as e:
        current_app.logger.error('Error calling pwnedpasswords API: ' + str(e))
        return False

    return False

def is_rate_limited(r, key: str, limit: int, period: timedelta):
    if r.setnx(key, limit):
        r.expire(key, int(period.total_seconds()))
    bucket_val = r.get(key)
    if bucket_val and int(bucket_val) > 0:
        r.decrby(key, 1)
        return False
    return True

def is_login_rate_limited(account_id):
    return is_rate_limited(get_conn(), f'ratelimit:login:{account_id}', 10, timedelta(seconds=300))

def is_upload_rate_limited(ip_address):
    return is_rate_limited(get_conn(), f'ratelimit:uploads:{ip_address}', 10, timedelta(seconds=60 * 60 * 24))
