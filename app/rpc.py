from jsonrpcserver import method, async_dispatch as dispatch


@method
async def add(a: int, b: int) -> int:
    return a + b


@method
async def subtract(a: int, b: int) -> int:
    return a - b


@method
async def multiply(a: int, b: int) -> int:
    return a * b


@method
async def divide(a: int, b: int) -> float:
    return a / b


async def handle(request):
    request = await request.read()
    response = await dispatch(request)
    if response.wanted:
        return response.json.encode()
    else:
        return None
