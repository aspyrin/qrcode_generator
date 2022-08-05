from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, AnyHttpUrl, ValidationError, validator
from io import BytesIO
from utils import qr_gen_bytes
from pymemcache.client import base

app = FastAPI()


class Message(BaseModel):
    url: AnyHttpUrl

    @validator('url')
    def url_domain_and_port(cls, value=str):
        if 'http://localhost:8000/' not in value.lower():
            raise ValueError('Domain and port must be http://localhost:8000/')
        return value


@app.get("/")
async def root():
    return {"message": "QR Code Generator"}


@app.get("/clear_cache")
async def clear_cache():
    """
    GET, function clear all caches in memory
    :return:
    """

    client = base.Client(('localhost', 11211))
    client.flush_all()
    return {"message": "Cache is cleared!"}


@app.post("/qr-code")
async def qr_code(parameters: Message):
    """
    POST, function receives JSON, pars and validate it,
    generate QR Code and return it as image/png
    :param parameters: url in JSON
    :return: QR Code as image/png
    """

    # get text from parameters
    try:
        text = parameters.url
    except ValidationError as e:
        return {"Exception": e.json()}

    # pymemcache
    client = base.Client(('localhost', 11211))
    cash_value = client.get(text)

    if cash_value is None:
        cash_value = qr_gen_bytes(text)
        client.set(text, cash_value)

    # create qr code object as BytesIO
    qr_io_object = BytesIO(cash_value)

    # get bytes_count
    bytes_count = 0
    if qr_io_object.getbuffer().nbytes > 0:
        bytes_count = qr_io_object.getbuffer().nbytes

    # create response
    response: StreamingResponse = StreamingResponse(qr_io_object, media_type="image/png")
    response.headers['content-type'] = 'image/png'
    response.headers['content-length'] = str(bytes_count)
    # send qr-code as attachment for download
    # response.headers["Content-Disposition"] = f"attachment; filename=qr_code.png"

    return response
