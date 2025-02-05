from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.lab_resource import LabResource
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/linked-labresource/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["LabResource"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_paginated_lab_resource_list_item_data in _response_200:
            componentsschemas_paginated_lab_resource_list_item = LabResource.from_dict(
                componentsschemas_paginated_lab_resource_list_item_data
            )

            response_200.append(componentsschemas_paginated_lab_resource_list_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["LabResource"]]:
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
    page: Union[Unset, int] = UNSET,
) -> Response[list["LabResource"]]:
    """View to list LabResource that are linked with the machine

    Args:
        limit (Union[Unset, int]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LabResource']]
    """

    kwargs = _get_kwargs(
        limit=limit,
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
    page: Union[Unset, int] = UNSET,
) -> Optional[list["LabResource"]]:
    """View to list LabResource that are linked with the machine

    Args:
        limit (Union[Unset, int]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LabResource']
    """

    return sync_detailed(
        client=client,
        limit=limit,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[list["LabResource"]]:
    """View to list LabResource that are linked with the machine

    Args:
        limit (Union[Unset, int]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LabResource']]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[list["LabResource"]]:
    """View to list LabResource that are linked with the machine

    Args:
        limit (Union[Unset, int]):
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LabResource']
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            page=page,
        )
    ).parsed
