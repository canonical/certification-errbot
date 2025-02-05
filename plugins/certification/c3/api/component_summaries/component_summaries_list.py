from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_summaries import ComponentSummaries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    canonical_id: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["canonical_id"] = canonical_id

    params["ordering"] = ordering

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/component-summaries/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["ComponentSummaries"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_component_summaries_list_item_data
        ) in _response_200:
            componentsschemas_paginated_component_summaries_list_item = (
                ComponentSummaries.from_dict(
                    componentsschemas_paginated_component_summaries_list_item_data
                )
            )

            response_200.append(
                componentsschemas_paginated_component_summaries_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ComponentSummaries"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Response[list["ComponentSummaries"]]:
    """Public API view to access the summary details for components

    Args:
        canonical_id (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ComponentSummaries']]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
        ordering=ordering,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Optional[list["ComponentSummaries"]]:
    """Public API view to access the summary details for components

    Args:
        canonical_id (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ComponentSummaries']
    """

    return sync_detailed(
        client=client,
        canonical_id=canonical_id,
        ordering=ordering,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Response[list["ComponentSummaries"]]:
    """Public API view to access the summary details for components

    Args:
        canonical_id (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ComponentSummaries']]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
        ordering=ordering,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Optional[list["ComponentSummaries"]]:
    """Public API view to access the summary details for components

    Args:
        canonical_id (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ComponentSummaries']
    """

    return (
        await asyncio_detailed(
            client=client,
            canonical_id=canonical_id,
            ordering=ordering,
        )
    ).parsed
