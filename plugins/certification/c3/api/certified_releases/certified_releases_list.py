from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.certified_configuration_release import CertifiedConfigurationRelease
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    desktops: Union[Unset, int] = UNSET,
    desktops_gte: Union[Unset, int] = UNSET,
    desktops_in: Union[Unset, list[int]] = UNSET,
    laptops: Union[Unset, int] = UNSET,
    laptops_gte: Union[Unset, int] = UNSET,
    laptops_in: Union[Unset, list[int]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    release_icontains: Union[Unset, str] = UNSET,
    release_iexact: Union[Unset, str] = UNSET,
    release_in: Union[Unset, list[str]] = UNSET,
    servers: Union[Unset, int] = UNSET,
    servers_gte: Union[Unset, int] = UNSET,
    servers_in: Union[Unset, list[int]] = UNSET,
    smart_core: Union[Unset, int] = UNSET,
    smart_core_gte: Union[Unset, int] = UNSET,
    smart_core_in: Union[Unset, list[int]] = UNSET,
    soc: Union[Unset, int] = UNSET,
    soc_gte: Union[Unset, int] = UNSET,
    soc_in: Union[Unset, list[int]] = UNSET,
    total: Union[Unset, int] = UNSET,
    total_gte: Union[Unset, int] = UNSET,
    total_in: Union[Unset, list[int]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["desktops"] = desktops

    params["desktops__gte"] = desktops_gte

    json_desktops_in: Union[Unset, list[int]] = UNSET
    if not isinstance(desktops_in, Unset):
        json_desktops_in = desktops_in

    params["desktops__in"] = json_desktops_in

    params["laptops"] = laptops

    params["laptops__gte"] = laptops_gte

    json_laptops_in: Union[Unset, list[int]] = UNSET
    if not isinstance(laptops_in, Unset):
        json_laptops_in = laptops_in

    params["laptops__in"] = json_laptops_in

    params["ordering"] = ordering

    params["release"] = release

    params["release__icontains"] = release_icontains

    params["release__iexact"] = release_iexact

    json_release_in: Union[Unset, list[str]] = UNSET
    if not isinstance(release_in, Unset):
        json_release_in = release_in

    params["release__in"] = json_release_in

    params["servers"] = servers

    params["servers__gte"] = servers_gte

    json_servers_in: Union[Unset, list[int]] = UNSET
    if not isinstance(servers_in, Unset):
        json_servers_in = servers_in

    params["servers__in"] = json_servers_in

    params["smart_core"] = smart_core

    params["smart_core__gte"] = smart_core_gte

    json_smart_core_in: Union[Unset, list[int]] = UNSET
    if not isinstance(smart_core_in, Unset):
        json_smart_core_in = smart_core_in

    params["smart_core__in"] = json_smart_core_in

    params["soc"] = soc

    params["soc__gte"] = soc_gte

    json_soc_in: Union[Unset, list[int]] = UNSET
    if not isinstance(soc_in, Unset):
        json_soc_in = soc_in

    params["soc__in"] = json_soc_in

    params["total"] = total

    params["total__gte"] = total_gte

    json_total_in: Union[Unset, list[int]] = UNSET
    if not isinstance(total_in, Unset):
        json_total_in = total_in

    params["total__in"] = json_total_in

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/certified-releases/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["CertifiedConfigurationRelease"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_certified_configuration_release_list_item_data
        ) in _response_200:
            componentsschemas_paginated_certified_configuration_release_list_item = CertifiedConfigurationRelease.from_dict(
                componentsschemas_paginated_certified_configuration_release_list_item_data
            )

            response_200.append(
                componentsschemas_paginated_certified_configuration_release_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CertifiedConfigurationRelease"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    desktops: Union[Unset, int] = UNSET,
    desktops_gte: Union[Unset, int] = UNSET,
    desktops_in: Union[Unset, list[int]] = UNSET,
    laptops: Union[Unset, int] = UNSET,
    laptops_gte: Union[Unset, int] = UNSET,
    laptops_in: Union[Unset, list[int]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    release_icontains: Union[Unset, str] = UNSET,
    release_iexact: Union[Unset, str] = UNSET,
    release_in: Union[Unset, list[str]] = UNSET,
    servers: Union[Unset, int] = UNSET,
    servers_gte: Union[Unset, int] = UNSET,
    servers_in: Union[Unset, list[int]] = UNSET,
    smart_core: Union[Unset, int] = UNSET,
    smart_core_gte: Union[Unset, int] = UNSET,
    smart_core_in: Union[Unset, list[int]] = UNSET,
    soc: Union[Unset, int] = UNSET,
    soc_gte: Union[Unset, int] = UNSET,
    soc_in: Union[Unset, list[int]] = UNSET,
    total: Union[Unset, int] = UNSET,
    total_gte: Union[Unset, int] = UNSET,
    total_in: Union[Unset, list[int]] = UNSET,
) -> Response[list["CertifiedConfigurationRelease"]]:
    """
    Args:
        desktops (Union[Unset, int]):
        desktops_gte (Union[Unset, int]):
        desktops_in (Union[Unset, list[int]]):
        laptops (Union[Unset, int]):
        laptops_gte (Union[Unset, int]):
        laptops_in (Union[Unset, list[int]]):
        ordering (Union[Unset, str]):
        release (Union[Unset, str]):
        release_icontains (Union[Unset, str]):
        release_iexact (Union[Unset, str]):
        release_in (Union[Unset, list[str]]):
        servers (Union[Unset, int]):
        servers_gte (Union[Unset, int]):
        servers_in (Union[Unset, list[int]]):
        smart_core (Union[Unset, int]):
        smart_core_gte (Union[Unset, int]):
        smart_core_in (Union[Unset, list[int]]):
        soc (Union[Unset, int]):
        soc_gte (Union[Unset, int]):
        soc_in (Union[Unset, list[int]]):
        total (Union[Unset, int]):
        total_gte (Union[Unset, int]):
        total_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationRelease']]
    """

    kwargs = _get_kwargs(
        desktops=desktops,
        desktops_gte=desktops_gte,
        desktops_in=desktops_in,
        laptops=laptops,
        laptops_gte=laptops_gte,
        laptops_in=laptops_in,
        ordering=ordering,
        release=release,
        release_icontains=release_icontains,
        release_iexact=release_iexact,
        release_in=release_in,
        servers=servers,
        servers_gte=servers_gte,
        servers_in=servers_in,
        smart_core=smart_core,
        smart_core_gte=smart_core_gte,
        smart_core_in=smart_core_in,
        soc=soc,
        soc_gte=soc_gte,
        soc_in=soc_in,
        total=total,
        total_gte=total_gte,
        total_in=total_in,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    desktops: Union[Unset, int] = UNSET,
    desktops_gte: Union[Unset, int] = UNSET,
    desktops_in: Union[Unset, list[int]] = UNSET,
    laptops: Union[Unset, int] = UNSET,
    laptops_gte: Union[Unset, int] = UNSET,
    laptops_in: Union[Unset, list[int]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    release_icontains: Union[Unset, str] = UNSET,
    release_iexact: Union[Unset, str] = UNSET,
    release_in: Union[Unset, list[str]] = UNSET,
    servers: Union[Unset, int] = UNSET,
    servers_gte: Union[Unset, int] = UNSET,
    servers_in: Union[Unset, list[int]] = UNSET,
    smart_core: Union[Unset, int] = UNSET,
    smart_core_gte: Union[Unset, int] = UNSET,
    smart_core_in: Union[Unset, list[int]] = UNSET,
    soc: Union[Unset, int] = UNSET,
    soc_gte: Union[Unset, int] = UNSET,
    soc_in: Union[Unset, list[int]] = UNSET,
    total: Union[Unset, int] = UNSET,
    total_gte: Union[Unset, int] = UNSET,
    total_in: Union[Unset, list[int]] = UNSET,
) -> Optional[list["CertifiedConfigurationRelease"]]:
    """
    Args:
        desktops (Union[Unset, int]):
        desktops_gte (Union[Unset, int]):
        desktops_in (Union[Unset, list[int]]):
        laptops (Union[Unset, int]):
        laptops_gte (Union[Unset, int]):
        laptops_in (Union[Unset, list[int]]):
        ordering (Union[Unset, str]):
        release (Union[Unset, str]):
        release_icontains (Union[Unset, str]):
        release_iexact (Union[Unset, str]):
        release_in (Union[Unset, list[str]]):
        servers (Union[Unset, int]):
        servers_gte (Union[Unset, int]):
        servers_in (Union[Unset, list[int]]):
        smart_core (Union[Unset, int]):
        smart_core_gte (Union[Unset, int]):
        smart_core_in (Union[Unset, list[int]]):
        soc (Union[Unset, int]):
        soc_gte (Union[Unset, int]):
        soc_in (Union[Unset, list[int]]):
        total (Union[Unset, int]):
        total_gte (Union[Unset, int]):
        total_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationRelease']
    """

    return sync_detailed(
        client=client,
        desktops=desktops,
        desktops_gte=desktops_gte,
        desktops_in=desktops_in,
        laptops=laptops,
        laptops_gte=laptops_gte,
        laptops_in=laptops_in,
        ordering=ordering,
        release=release,
        release_icontains=release_icontains,
        release_iexact=release_iexact,
        release_in=release_in,
        servers=servers,
        servers_gte=servers_gte,
        servers_in=servers_in,
        smart_core=smart_core,
        smart_core_gte=smart_core_gte,
        smart_core_in=smart_core_in,
        soc=soc,
        soc_gte=soc_gte,
        soc_in=soc_in,
        total=total,
        total_gte=total_gte,
        total_in=total_in,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    desktops: Union[Unset, int] = UNSET,
    desktops_gte: Union[Unset, int] = UNSET,
    desktops_in: Union[Unset, list[int]] = UNSET,
    laptops: Union[Unset, int] = UNSET,
    laptops_gte: Union[Unset, int] = UNSET,
    laptops_in: Union[Unset, list[int]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    release_icontains: Union[Unset, str] = UNSET,
    release_iexact: Union[Unset, str] = UNSET,
    release_in: Union[Unset, list[str]] = UNSET,
    servers: Union[Unset, int] = UNSET,
    servers_gte: Union[Unset, int] = UNSET,
    servers_in: Union[Unset, list[int]] = UNSET,
    smart_core: Union[Unset, int] = UNSET,
    smart_core_gte: Union[Unset, int] = UNSET,
    smart_core_in: Union[Unset, list[int]] = UNSET,
    soc: Union[Unset, int] = UNSET,
    soc_gte: Union[Unset, int] = UNSET,
    soc_in: Union[Unset, list[int]] = UNSET,
    total: Union[Unset, int] = UNSET,
    total_gte: Union[Unset, int] = UNSET,
    total_in: Union[Unset, list[int]] = UNSET,
) -> Response[list["CertifiedConfigurationRelease"]]:
    """
    Args:
        desktops (Union[Unset, int]):
        desktops_gte (Union[Unset, int]):
        desktops_in (Union[Unset, list[int]]):
        laptops (Union[Unset, int]):
        laptops_gte (Union[Unset, int]):
        laptops_in (Union[Unset, list[int]]):
        ordering (Union[Unset, str]):
        release (Union[Unset, str]):
        release_icontains (Union[Unset, str]):
        release_iexact (Union[Unset, str]):
        release_in (Union[Unset, list[str]]):
        servers (Union[Unset, int]):
        servers_gte (Union[Unset, int]):
        servers_in (Union[Unset, list[int]]):
        smart_core (Union[Unset, int]):
        smart_core_gte (Union[Unset, int]):
        smart_core_in (Union[Unset, list[int]]):
        soc (Union[Unset, int]):
        soc_gte (Union[Unset, int]):
        soc_in (Union[Unset, list[int]]):
        total (Union[Unset, int]):
        total_gte (Union[Unset, int]):
        total_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationRelease']]
    """

    kwargs = _get_kwargs(
        desktops=desktops,
        desktops_gte=desktops_gte,
        desktops_in=desktops_in,
        laptops=laptops,
        laptops_gte=laptops_gte,
        laptops_in=laptops_in,
        ordering=ordering,
        release=release,
        release_icontains=release_icontains,
        release_iexact=release_iexact,
        release_in=release_in,
        servers=servers,
        servers_gte=servers_gte,
        servers_in=servers_in,
        smart_core=smart_core,
        smart_core_gte=smart_core_gte,
        smart_core_in=smart_core_in,
        soc=soc,
        soc_gte=soc_gte,
        soc_in=soc_in,
        total=total,
        total_gte=total_gte,
        total_in=total_in,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    desktops: Union[Unset, int] = UNSET,
    desktops_gte: Union[Unset, int] = UNSET,
    desktops_in: Union[Unset, list[int]] = UNSET,
    laptops: Union[Unset, int] = UNSET,
    laptops_gte: Union[Unset, int] = UNSET,
    laptops_in: Union[Unset, list[int]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    release_icontains: Union[Unset, str] = UNSET,
    release_iexact: Union[Unset, str] = UNSET,
    release_in: Union[Unset, list[str]] = UNSET,
    servers: Union[Unset, int] = UNSET,
    servers_gte: Union[Unset, int] = UNSET,
    servers_in: Union[Unset, list[int]] = UNSET,
    smart_core: Union[Unset, int] = UNSET,
    smart_core_gte: Union[Unset, int] = UNSET,
    smart_core_in: Union[Unset, list[int]] = UNSET,
    soc: Union[Unset, int] = UNSET,
    soc_gte: Union[Unset, int] = UNSET,
    soc_in: Union[Unset, list[int]] = UNSET,
    total: Union[Unset, int] = UNSET,
    total_gte: Union[Unset, int] = UNSET,
    total_in: Union[Unset, list[int]] = UNSET,
) -> Optional[list["CertifiedConfigurationRelease"]]:
    """
    Args:
        desktops (Union[Unset, int]):
        desktops_gte (Union[Unset, int]):
        desktops_in (Union[Unset, list[int]]):
        laptops (Union[Unset, int]):
        laptops_gte (Union[Unset, int]):
        laptops_in (Union[Unset, list[int]]):
        ordering (Union[Unset, str]):
        release (Union[Unset, str]):
        release_icontains (Union[Unset, str]):
        release_iexact (Union[Unset, str]):
        release_in (Union[Unset, list[str]]):
        servers (Union[Unset, int]):
        servers_gte (Union[Unset, int]):
        servers_in (Union[Unset, list[int]]):
        smart_core (Union[Unset, int]):
        smart_core_gte (Union[Unset, int]):
        smart_core_in (Union[Unset, list[int]]):
        soc (Union[Unset, int]):
        soc_gte (Union[Unset, int]):
        soc_in (Union[Unset, list[int]]):
        total (Union[Unset, int]):
        total_gte (Union[Unset, int]):
        total_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationRelease']
    """

    return (
        await asyncio_detailed(
            client=client,
            desktops=desktops,
            desktops_gte=desktops_gte,
            desktops_in=desktops_in,
            laptops=laptops,
            laptops_gte=laptops_gte,
            laptops_in=laptops_in,
            ordering=ordering,
            release=release,
            release_icontains=release_icontains,
            release_iexact=release_iexact,
            release_in=release_in,
            servers=servers,
            servers_gte=servers_gte,
            servers_in=servers_in,
            smart_core=smart_core,
            smart_core_gte=smart_core_gte,
            smart_core_in=smart_core_in,
            soc=soc,
            soc_gte=soc_gte,
            soc_in=soc_in,
            total=total,
            total_gte=total_gte,
            total_in=total_in,
        )
    ).parsed
