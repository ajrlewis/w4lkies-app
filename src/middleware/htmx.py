import json
from urllib.parse import urlparse

from flask import request, Response
from flask_wtf.csrf import generate_csrf
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


def refresh_csrf_token_in_response(response: Response) -> Response:
    """
    Generates a new CSRF token and includes it in the response as an HX-Trigger header.

    This method is used to refresh the CSRF token after an HTMX request, ensuring that the
    client has the most up-to-date token for future requests.

    Args:
        response (Response): The response object to be modified.

    Returns:
        Response: The modified response object with the new CSRF token.

    Raises:
        ValueError: If the input response object is invalid.
    """
    try:
        logger.debug("Generating new CSRF token")
        new_token = generate_csrf()
        hx_trigger = json.dumps({"refreshCSRF": {"token": new_token}})
        response.headers["HX-Trigger"] = hx_trigger
        return response
    except Exception as e:
        logger.error(f"Error generating CSRF token: {e}")
        raise
