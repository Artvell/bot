# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os
from flask_dashboard.app.config import bot_token
import hmac


def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        if data[key] is not None:
            string_arr.append(key+"="+data[key])
    string_cat = '\n'.join(string_arr)
    return string_cat

def verify_user(tg_data):
    """Verify user from telegram"""
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(bot_token.encode('utf-8')).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string,'utf-8')
    hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
    if hmac_string == tg_data['hash']:
        return True
    return False

