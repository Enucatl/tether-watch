import click
import logging
import logging.config
import requests
import json
import datetime
import telegram
import os
import time


from log_config import log_config


@click.command()
@click.option("-n", default=60, type=int, help="watch every n seconds")
@click.option("-v", "--verbose", count=True)
def main(n, verbose):
    url = "http://omniexplorer.info/ask.aspx"
    address = "3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL"
    logger = logging.getLogger(__name__)
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot = telegram.Bot(token=token)
    logging.config.dictConfig(log_config(verbose))
    params = {
        "api": "gethistory",
        "address": address
    }
    latest_txid = 0
    while True:
        try:
            response = requests.get(url, params=params).json()
            latest_transaction = response["transactions"][0]
            params = {
                "api": "gettx",
                "txid": latest_transaction
            }
            response = requests.get(url, params=params)
            t = json.loads("{" + response.text + "}")
            logger.debug("latest transaction %s", t)
            txid = t["txid"]
            if txid != latest_txid:
                timestamp = int(t["blocktime"])
                amount = int(float(t["amount"]) / 1e6)
                timestamp_human = datetime.datetime.fromtimestamp(
                    timestamp
                    ).strftime('%Y-%m-%d %H:%M:%S')
                transaction_link = "http://omniexplorer.info/lookuptx.aspx?txid={}"
                address_link = "http://omniexplorer.info/lookupadd.aspx?address={}"
                telegram_message = """
                {} MUSDT created at {}
                transaction: {}
                sent to address: {}""".format(
                    amount,
                    timestamp_human,
                    transaction_link.format(t["txid"]),
                    address_link.format(t["referenceaddress"]),
                )
                bot.send_message(chat_id=chat_id, text=telegram_message)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
        time.sleep(n)


if __name__ == "__main__":
    main()
