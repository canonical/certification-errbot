from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.certified_configuration_details import CertifiedConfigurationDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["canonical_id"] = canonical_id

    params["canonical_id__in"] = canonical_id_in

    params["model"] = model

    params["ordering"] = ordering

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/certified-configuration-details/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["CertifiedConfigurationDetails"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_certified_configuration_details_list_item_data
        ) in _response_200:
            componentsschemas_paginated_certified_configuration_details_list_item = CertifiedConfigurationDetails.from_dict(
                componentsschemas_paginated_certified_configuration_details_list_item_data
            )

            response_200.append(
                componentsschemas_paginated_certified_configuration_details_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CertifiedConfigurationDetails"]]:
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
    canonical_id_in: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Response[list["CertifiedConfigurationDetails"]]:
    """
    Args:
        canonical_id (Union[Unset, str]):
        canonical_id_in (Union[Unset, str]):
        model (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationDetails']]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
        canonical_id_in=canonical_id_in,
        model=model,
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
    canonical_id_in: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Optional[list["CertifiedConfigurationDetails"]]:
    """
    Args:
        canonical_id (Union[Unset, str]):
        canonical_id_in (Union[Unset, str]):
        model (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationDetails']
    """

    return sync_detailed(
        client=client,
        canonical_id=canonical_id,
        canonical_id_in=canonical_id_in,
        model=model,
        ordering=ordering,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Response[list["CertifiedConfigurationDetails"]]:
    """
    Args:
        canonical_id (Union[Unset, str]):
        canonical_id_in (Union[Unset, str]):
        model (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationDetails']]
    """

    kwargs = _get_kwargs(
        canonical_id=canonical_id,
        canonical_id_in=canonical_id_in,
        model=model,
        ordering=ordering,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
) -> Optional[list["CertifiedConfigurationDetails"]]:
    """
    Args:
        canonical_id (Union[Unset, str]):
        canonical_id_in (Union[Unset, str]):
        model (Union[Unset, str]):
        ordering (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationDetails']
    """

    return (
        await asyncio_detailed(
            client=client,
            canonical_id=canonical_id,
            canonical_id_in=canonical_id_in,
            model=model,
            ordering=ordering,
        )
    ).parsed
