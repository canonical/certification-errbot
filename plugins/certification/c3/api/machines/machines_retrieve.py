from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.read_physical_machine import ReadPhysicalMachine
from ...types import Response


def _get_kwargs(
    canonical_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/machines/{canonical_id}/".format(
            canonical_id=canonical_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ReadPhysicalMachine]:
    if response.status_code == 200:
        response_200 = ReadPhysicalMachine.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReadPhysicalMachine]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    canonical_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ReadPhysicalMachine]:
    """View to detail and modify a given PhysicalMachine.

    Args:
        canonical_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReadPhysicalMachine]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    canonical_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ReadPhysicalMachine]:
    """View to detail and modify a given PhysicalMachine.

    Args:
        canonical_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReadPhysicalMachine
    """

    return sync_detailed(
        canonical_id=canonical_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    canonical_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ReadPhysicalMachine]:
    """View to detail and modify a given PhysicalMachine.

    Args:
        canonical_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReadPhysicalMachine]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    canonical_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[ReadPhysicalMachine]:
    """View to detail and modify a given PhysicalMachine.

    Args:
        canonical_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReadPhysicalMachine
    """

    return (
        await asyncio_detailed(
            canonical_id=canonical_id,
            client=client,
        )
    ).parsed
