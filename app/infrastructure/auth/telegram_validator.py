import hashlib
import hmac
import urllib.parse
import json

def validate_tma_init_data(init_data: str, bot_token: str) -> dict:

    parsed_data = urllib.parse.parse_qsl(init_data)
    data_dict = dict(parsed_data)


    received_hash = data_dict.pop('hash', None)
    if not received_hash:
        raise ValueError("Втрачено поле hash від Тelegram")
    
    sorted_items = sorted(data_dict.items(), key=lambda x: x[0])
    
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_items])

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != received_hash:
        raise ValueError("Невірний підпис Telegram")

    user_data_str = data_dict.get('user', '{}')
    return json.loads(user_data_str)