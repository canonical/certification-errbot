from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_switch_list import PaginatedSwitchList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["ordering"] = ordering

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/switches/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PaginatedSwitchList]:
    if response.status_code == 200:
        response_200 = PaginatedSwitchList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PaginatedSwitchList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[PaginatedSwitchList]:
    """API endpoint to get the list of network switches and create new
    instances of network switches

    Args:
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedSwitchList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        ordering=ordering,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[PaginatedSwitchList]:
    """API endpoint to get the list of network switches and create new
    instances of network switches

    Args:
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedSwitchList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        ordering=ordering,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[PaginatedSwitchList]:
    """API endpoint to get the list of network switches and create new
    instances of network switches

    Args:
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedSwitchList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        ordering=ordering,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[PaginatedSwitchList]:
    """API endpoint to get the list of network switches and create new
    instances of network switches

    Args:
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedSwitchList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            ordering=ordering,
            page=page,
        )
    ).parsed
