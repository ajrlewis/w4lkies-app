from urllib.parse import urlparse

from flask import request, Response
from loguru import logger


def htmx_middleware(response: Response) -> Response:
    hx_request = request.headers.get("HX-Request")
    status_code = response.status_code
    if hx_request == "true" and status_code == 302:
        logger.debug(f"{hx_request = } {status_code = }")
        ref_header = request.headers.get("Referer", "")
        logger.debug(f"{ref_header = }")
        if ref_header:
            referer = urlparse(ref_header)
            logger.debug(f"{referer = }")
            querystring = f"?next={referer.path}"
            logger.debug(f"{querystring = }")
        else:
            querystring = ""
        redirect = urlparse(response.location)
        response.status_code = 204
        response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"
    return response
