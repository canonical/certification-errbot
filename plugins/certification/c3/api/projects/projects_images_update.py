from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.image import Image
from ...types import Response


def _get_kwargs(
    image_id: int,
    *,
    body: Union[
        Image,
        Image,
        Image,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v2/projects/images/{image_id}/".format(
            image_id=image_id,
        ),
    }

    if isinstance(body, Image):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, Image):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, Image):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Image]:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Image]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    image_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        Image,
        Image,
        Image,
    ],
) -> Response[Image]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        image_id (int):
        body (Image):
        body (Image):
        body (Image):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Image]
    """

    kwargs = _get_kwargs(
        image_id=image_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    image_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        Image,
        Image,
        Image,
    ],
) -> Optional[Image]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        image_id (int):
        body (Image):
        body (Image):
        body (Image):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Image
    """

    return sync_detailed(
        image_id=image_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    image_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        Image,
        Image,
        Image,
    ],
) -> Response[Image]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        image_id (int):
        body (Image):
        body (Image):
        body (Image):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Image]
    """

    kwargs = _get_kwargs(
        image_id=image_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    image_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        Image,
        Image,
        Image,
    ],
) -> Optional[Image]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        image_id (int):
        body (Image):
        body (Image):
        body (Image):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Image
    """

    return (
        await asyncio_detailed(
            image_id=image_id,
            client=client,
            body=body,
        )
    ).parsed
