from urllib.parse import urlparse

from flask import request, Response
from loguru import logger


def handle_htmx_redirect(response: Response) -> Response:
    """
    Handles redirects for HTMX requests.

    If the request is an HTMX request and the response status code is 302,
    this method modifies the response to include an HX-Redirect header with the redirect URL.

    Args:
        response (Response): The response object to be modified.

    Returns:
        Response: The modified response object.
    """

    # Check if the request is an HTMX request
    hx_request = request.headers.get("HX-Request")
    if hx_request != "true":
        return response  # Not an HTMX request, return the original response

    # Check if the response status code is 302
    status_code = response.status_code
    if status_code != 302:
        return response  # Not a redirect, return the original response

    # Get the referer URL from the request headers
    ref_header = request.headers.get("Referer", "")
    if ref_header:
        # Parse the referer URL to extract the path
        referer = urlparse(ref_header)
        querystring = f"?next={referer.path}"
    else:
        querystring = ""

    # Parse the redirect URL from the response location
    redirect = urlparse(response.location)

    # Modify the response to include an HX-Redirect header
    response.status_code = 204
    response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"

    return response
