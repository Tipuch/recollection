import asyncio

from whitenoise.middleware import WhiteNoiseMiddleware


class AsyncWhitenoiseMiddleware(WhiteNoiseMiddleware):
    sync_capable = True
    async_capable = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._async_check()

    def _async_check(self):
        if asyncio.iscoroutinefunction(self.get_response):
            self._is_coroutine = asyncio.coroutines._is_coroutine

    def __call__(self, request):
        if asyncio.iscoroutinefunction(self.get_response):
            return self.__acall__(request)
        else:
            return super().__call__(request)

    async def __acall__(self, request):
        response = self.process_request(request)
        if response is None:
            response = await self.get_response(request)
        return response