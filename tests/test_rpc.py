from jsonrpcserver import method, serve

@method
def ping() -> str:
    return "pong"

serve(methods=[ping])