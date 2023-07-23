from fastapi import FastAPI

app = FastAPI()

from . import main, rpc
from .utils import math, strings