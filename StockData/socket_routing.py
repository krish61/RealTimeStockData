from WebSocket.stock_consumers import StockConsumer
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
                URLRouter(
                    [
                        path(
                            "stockdata/",
                            StockConsumer.as_asgi(),
                        ),

                    ]
                )
        )
    }
)
