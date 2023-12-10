import httpx
import asyncio
import ujson as json

class Bot:
    def __init__(self, userAgent):
        self.userAgent = userAgent