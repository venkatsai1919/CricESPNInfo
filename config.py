import os

#TOKEN = os.environ.get("Token")
#URL = os.environ.get("URL")
TOKEN="1764854085:AAHjg8xaP5hP7rPop-ott0uSVCGJy2tHTTA"
URL="https://abb259c5f008.ngrok.io"
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(URL)
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'
