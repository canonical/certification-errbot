from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.certified_vendor import CertifiedVendor
from ...types import Response


def _get_kwargs(
    vendor: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/certified-vendors/{vendor}/".format(
            vendor=vendor,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CertifiedVendor]:
    if response.status_code == 200:
        response_200 = CertifiedVendor.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CertifiedVendor]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vendor: str,
    *,
    client: AuthenticatedClient,
) -> Response[CertifiedVendor]:
    """
    Args:
        vendor (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CertifiedVendor]
    """

    kwargs = _get_kwargs(
        vendor=vendor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vendor: str,
    *,
    client: AuthenticatedClient,
) -> Optional[CertifiedVendor]:
    """
    Args:
        vendor (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CertifiedVendor
    """

    return sync_detailed(
        vendor=vendor,
        client=client,
    ).parsed


async def asyncio_detailed(
    vendor: str,
    *,
    client: AuthenticatedClient,
) -> Response[CertifiedVendor]:
    """
    Args:
        vendor (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CertifiedVendor]
    """

    kwargs = _get_kwargs(
        vendor=vendor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vendor: str,
    *,
    client: AuthenticatedClient,
) -> Optional[CertifiedVendor]:
    """
    Args:
        vendor (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CertifiedVendor
    """

    return (
        await asyncio_detailed(
            vendor=vendor,
            client=client,
        )
    ).parsed
