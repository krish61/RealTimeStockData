import json
import time
from urllib.parse import parse_qs
from channels.consumer import AsyncConsumer
from yahoo_fin.stock_info import tickers_nifty50, get_quote_table
import asyncio
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
)


class StockConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        query_params = parse_qs(self.scope["query_string"], encoding="utf-8")
        # print(query_params)
        stocks_list = query_params[b"stockpicker"]
        stocks_list = list(map(lambda x: x.decode("utf-8"), stocks_list))
        while True:
            stock_data = {}
            for stock in stocks_list:
                data = get_quote_table(stock)
                stock_data.update({stock: data})
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps(stock_data),
                }
            )
            await asyncio.sleep(2)

        # stock_list = {
        #     "message": "Hello, welcome to Stock Live Data. Send Any name in this list to get real timedata",
        #     "stocks": tickers_nifty50(),
        # }
        # await self.send(
        #     {"type": "websocket.send", "text": json.dumps(stock_list)}
        # )

    async def websocket_receive(self, event):
        while True:
            await asyncio.sleep(2)
            stock_data = {}
            # print(event.get("stocks"))
            stocks = json.loads(event.get("text")).get("stocks")
            for stock in stocks:
                data = get_quote_table(stock)
                stock_data.update({stock: data})
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps(stock_data),
                }
            )

    async def websocket_disconnect(self, event):
        print("disconnected", event)
