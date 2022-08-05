import qrcode
from PIL import Image
from io import BytesIO


def qr_gen_io(text: str) -> BytesIO:
    """
    function generate QR Code from text
    :param text:
    :return: BytesIO
    """

    # create qrcode object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # create image object
    img: Image = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # create binary/iterable object from edited image
    with BytesIO() as output:
        img.save(output, format='png')
        img_byte_arr = output.getvalue()

    return BytesIO(img_byte_arr)


def qr_gen_bytes(text: str) -> bytes:
    """
    function generate QR Code from text
    :param text:
    :return: bytes
    """

    # create qrcode object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # create image object
    img: Image = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # create binary/iterable object from edited image
    with BytesIO() as output:
        img.save(output, format='png')
        img_byte_arr = output.getvalue()

    return img_byte_arr
