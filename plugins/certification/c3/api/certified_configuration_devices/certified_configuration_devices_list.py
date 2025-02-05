from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.certified_configuration_device import CertifiedConfigurationDevice
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    bus: Union[Unset, str] = UNSET,
    bus_icontains: Union[Unset, str] = UNSET,
    bus_iexact: Union[Unset, str] = UNSET,
    bus_in: Union[Unset, list[str]] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_icontains: Union[Unset, str] = UNSET,
    canonical_id_iexact: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, list[str]] = UNSET,
    category: Union[Unset, str] = UNSET,
    category_icontains: Union[Unset, str] = UNSET,
    category_iexact: Union[Unset, str] = UNSET,
    category_in: Union[Unset, list[str]] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    identifier_icontains: Union[Unset, str] = UNSET,
    identifier_iexact: Union[Unset, str] = UNSET,
    identifier_in: Union[Unset, list[str]] = UNSET,
    make: Union[Unset, str] = UNSET,
    make_icontains: Union[Unset, str] = UNSET,
    make_iexact: Union[Unset, str] = UNSET,
    make_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    subproduct_name: Union[Unset, str] = UNSET,
    subproduct_name_icontains: Union[Unset, str] = UNSET,
    subproduct_name_iexact: Union[Unset, str] = UNSET,
    subproduct_name_in: Union[Unset, list[str]] = UNSET,
    subsystem: Union[Unset, str] = UNSET,
    subsystem_icontains: Union[Unset, str] = UNSET,
    subsystem_iexact: Union[Unset, str] = UNSET,
    subsystem_in: Union[Unset, list[str]] = UNSET,
    subvendor_id: Union[Unset, int] = UNSET,
    subvendor_id_icontains: Union[Unset, int] = UNSET,
    subvendor_id_iexact: Union[Unset, int] = UNSET,
    subvendor_id_in: Union[Unset, list[int]] = UNSET,
    vendor_id: Union[Unset, int] = UNSET,
    vendor_id_icontains: Union[Unset, int] = UNSET,
    vendor_id_iexact: Union[Unset, int] = UNSET,
    vendor_id_in: Union[Unset, list[int]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["bus"] = bus

    params["bus__icontains"] = bus_icontains

    params["bus__iexact"] = bus_iexact

    json_bus_in: Union[Unset, list[str]] = UNSET
    if not isinstance(bus_in, Unset):
        json_bus_in = bus_in

    params["bus__in"] = json_bus_in

    params["canonical_id"] = canonical_id

    params["canonical_id__icontains"] = canonical_id_icontains

    params["canonical_id__iexact"] = canonical_id_iexact

    json_canonical_id_in: Union[Unset, list[str]] = UNSET
    if not isinstance(canonical_id_in, Unset):
        json_canonical_id_in = canonical_id_in

    params["canonical_id__in"] = json_canonical_id_in

    params["category"] = category

    params["category__icontains"] = category_icontains

    params["category__iexact"] = category_iexact

    json_category_in: Union[Unset, list[str]] = UNSET
    if not isinstance(category_in, Unset):
        json_category_in = category_in

    params["category__in"] = json_category_in

    params["identifier"] = identifier

    params["identifier__icontains"] = identifier_icontains

    params["identifier__iexact"] = identifier_iexact

    json_identifier_in: Union[Unset, list[str]] = UNSET
    if not isinstance(identifier_in, Unset):
        json_identifier_in = identifier_in

    params["identifier__in"] = json_identifier_in

    params["make"] = make

    params["make__icontains"] = make_icontains

    params["make__iexact"] = make_iexact

    json_make_in: Union[Unset, list[str]] = UNSET
    if not isinstance(make_in, Unset):
        json_make_in = make_in

    params["make__in"] = json_make_in

    params["name"] = name

    params["name__icontains"] = name_icontains

    params["name__iexact"] = name_iexact

    json_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(name_in, Unset):
        json_name_in = name_in

    params["name__in"] = json_name_in

    params["ordering"] = ordering

    params["subproduct_name"] = subproduct_name

    params["subproduct_name__icontains"] = subproduct_name_icontains

    params["subproduct_name__iexact"] = subproduct_name_iexact

    json_subproduct_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(subproduct_name_in, Unset):
        json_subproduct_name_in = subproduct_name_in

    params["subproduct_name__in"] = json_subproduct_name_in

    params["subsystem"] = subsystem

    params["subsystem__icontains"] = subsystem_icontains

    params["subsystem__iexact"] = subsystem_iexact

    json_subsystem_in: Union[Unset, list[str]] = UNSET
    if not isinstance(subsystem_in, Unset):
        json_subsystem_in = subsystem_in

    params["subsystem__in"] = json_subsystem_in

    params["subvendor_id"] = subvendor_id

    params["subvendor_id__icontains"] = subvendor_id_icontains

    params["subvendor_id__iexact"] = subvendor_id_iexact

    json_subvendor_id_in: Union[Unset, list[int]] = UNSET
    if not isinstance(subvendor_id_in, Unset):
        json_subvendor_id_in = subvendor_id_in

    params["subvendor_id__in"] = json_subvendor_id_in

    params["vendor_id"] = vendor_id

    params["vendor_id__icontains"] = vendor_id_icontains

    params["vendor_id__iexact"] = vendor_id_iexact

    json_vendor_id_in: Union[Unset, list[int]] = UNSET
    if not isinstance(vendor_id_in, Unset):
        json_vendor_id_in = vendor_id_in

    params["vendor_id__in"] = json_vendor_id_in

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/certified-configuration-devices/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["CertifiedConfigurationDevice"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_certified_configuration_device_list_item_data
        ) in _response_200:
            componentsschemas_paginated_certified_configuration_device_list_item = CertifiedConfigurationDevice.from_dict(
                componentsschemas_paginated_certified_configuration_device_list_item_data
            )

            response_200.append(
                componentsschemas_paginated_certified_configuration_device_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CertifiedConfigurationDevice"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    bus: Union[Unset, str] = UNSET,
    bus_icontains: Union[Unset, str] = UNSET,
    bus_iexact: Union[Unset, str] = UNSET,
    bus_in: Union[Unset, list[str]] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_icontains: Union[Unset, str] = UNSET,
    canonical_id_iexact: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, list[str]] = UNSET,
    category: Union[Unset, str] = UNSET,
    category_icontains: Union[Unset, str] = UNSET,
    category_iexact: Union[Unset, str] = UNSET,
    category_in: Union[Unset, list[str]] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    identifier_icontains: Union[Unset, str] = UNSET,
    identifier_iexact: Union[Unset, str] = UNSET,
    identifier_in: Union[Unset, list[str]] = UNSET,
    make: Union[Unset, str] = UNSET,
    make_icontains: Union[Unset, str] = UNSET,
    make_iexact: Union[Unset, str] = UNSET,
    make_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    subproduct_name: Union[Unset, str] = UNSET,
    subproduct_name_icontains: Union[Unset, str] = UNSET,
    subproduct_name_iexact: Union[Unset, str] = UNSET,
    subproduct_name_in: Union[Unset, list[str]] = UNSET,
    subsystem: Union[Unset, str] = UNSET,
    subsystem_icontains: Union[Unset, str] = UNSET,
    subsystem_iexact: Union[Unset, str] = UNSET,
    subsystem_in: Union[Unset, list[str]] = UNSET,
    subvendor_id: Union[Unset, int] = UNSET,
    subvendor_id_icontains: Union[Unset, int] = UNSET,
    subvendor_id_iexact: Union[Unset, int] = UNSET,
    subvendor_id_in: Union[Unset, list[int]] = UNSET,
    vendor_id: Union[Unset, int] = UNSET,
    vendor_id_icontains: Union[Unset, int] = UNSET,
    vendor_id_iexact: Union[Unset, int] = UNSET,
    vendor_id_in: Union[Unset, list[int]] = UNSET,
) -> Response[list["CertifiedConfigurationDevice"]]:
    """
    Args:
        bus (Union[Unset, str]):
        bus_icontains (Union[Unset, str]):
        bus_iexact (Union[Unset, str]):
        bus_in (Union[Unset, list[str]]):
        canonical_id (Union[Unset, str]):
        canonical_id_icontains (Union[Unset, str]):
        canonical_id_iexact (Union[Unset, str]):
        canonical_id_in (Union[Unset, list[str]]):
        category (Union[Unset, str]):
        category_icontains (Union[Unset, str]):
        category_iexact (Union[Unset, str]):
        category_in (Union[Unset, list[str]]):
        identifier (Union[Unset, str]):
        identifier_icontains (Union[Unset, str]):
        identifier_iexact (Union[Unset, str]):
        identifier_in (Union[Unset, list[str]]):
        make (Union[Unset, str]):
        make_icontains (Union[Unset, str]):
        make_iexact (Union[Unset, str]):
        make_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        subproduct_name (Union[Unset, str]):
        subproduct_name_icontains (Union[Unset, str]):
        subproduct_name_iexact (Union[Unset, str]):
        subproduct_name_in (Union[Unset, list[str]]):
        subsystem (Union[Unset, str]):
        subsystem_icontains (Union[Unset, str]):
        subsystem_iexact (Union[Unset, str]):
        subsystem_in (Union[Unset, list[str]]):
        subvendor_id (Union[Unset, int]):
        subvendor_id_icontains (Union[Unset, int]):
        subvendor_id_iexact (Union[Unset, int]):
        subvendor_id_in (Union[Unset, list[int]]):
        vendor_id (Union[Unset, int]):
        vendor_id_icontains (Union[Unset, int]):
        vendor_id_iexact (Union[Unset, int]):
        vendor_id_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationDevice']]
    """

    kwargs = _get_kwargs(
        bus=bus,
        bus_icontains=bus_icontains,
        bus_iexact=bus_iexact,
        bus_in=bus_in,
        canonical_id=canonical_id,
        canonical_id_icontains=canonical_id_icontains,
        canonical_id_iexact=canonical_id_iexact,
        canonical_id_in=canonical_id_in,
        category=category,
        category_icontains=category_icontains,
        category_iexact=category_iexact,
        category_in=category_in,
        identifier=identifier,
        identifier_icontains=identifier_icontains,
        identifier_iexact=identifier_iexact,
        identifier_in=identifier_in,
        make=make,
        make_icontains=make_icontains,
        make_iexact=make_iexact,
        make_in=make_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        subproduct_name=subproduct_name,
        subproduct_name_icontains=subproduct_name_icontains,
        subproduct_name_iexact=subproduct_name_iexact,
        subproduct_name_in=subproduct_name_in,
        subsystem=subsystem,
        subsystem_icontains=subsystem_icontains,
        subsystem_iexact=subsystem_iexact,
        subsystem_in=subsystem_in,
        subvendor_id=subvendor_id,
        subvendor_id_icontains=subvendor_id_icontains,
        subvendor_id_iexact=subvendor_id_iexact,
        subvendor_id_in=subvendor_id_in,
        vendor_id=vendor_id,
        vendor_id_icontains=vendor_id_icontains,
        vendor_id_iexact=vendor_id_iexact,
        vendor_id_in=vendor_id_in,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    bus: Union[Unset, str] = UNSET,
    bus_icontains: Union[Unset, str] = UNSET,
    bus_iexact: Union[Unset, str] = UNSET,
    bus_in: Union[Unset, list[str]] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_icontains: Union[Unset, str] = UNSET,
    canonical_id_iexact: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, list[str]] = UNSET,
    category: Union[Unset, str] = UNSET,
    category_icontains: Union[Unset, str] = UNSET,
    category_iexact: Union[Unset, str] = UNSET,
    category_in: Union[Unset, list[str]] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    identifier_icontains: Union[Unset, str] = UNSET,
    identifier_iexact: Union[Unset, str] = UNSET,
    identifier_in: Union[Unset, list[str]] = UNSET,
    make: Union[Unset, str] = UNSET,
    make_icontains: Union[Unset, str] = UNSET,
    make_iexact: Union[Unset, str] = UNSET,
    make_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    subproduct_name: Union[Unset, str] = UNSET,
    subproduct_name_icontains: Union[Unset, str] = UNSET,
    subproduct_name_iexact: Union[Unset, str] = UNSET,
    subproduct_name_in: Union[Unset, list[str]] = UNSET,
    subsystem: Union[Unset, str] = UNSET,
    subsystem_icontains: Union[Unset, str] = UNSET,
    subsystem_iexact: Union[Unset, str] = UNSET,
    subsystem_in: Union[Unset, list[str]] = UNSET,
    subvendor_id: Union[Unset, int] = UNSET,
    subvendor_id_icontains: Union[Unset, int] = UNSET,
    subvendor_id_iexact: Union[Unset, int] = UNSET,
    subvendor_id_in: Union[Unset, list[int]] = UNSET,
    vendor_id: Union[Unset, int] = UNSET,
    vendor_id_icontains: Union[Unset, int] = UNSET,
    vendor_id_iexact: Union[Unset, int] = UNSET,
    vendor_id_in: Union[Unset, list[int]] = UNSET,
) -> Optional[list["CertifiedConfigurationDevice"]]:
    """
    Args:
        bus (Union[Unset, str]):
        bus_icontains (Union[Unset, str]):
        bus_iexact (Union[Unset, str]):
        bus_in (Union[Unset, list[str]]):
        canonical_id (Union[Unset, str]):
        canonical_id_icontains (Union[Unset, str]):
        canonical_id_iexact (Union[Unset, str]):
        canonical_id_in (Union[Unset, list[str]]):
        category (Union[Unset, str]):
        category_icontains (Union[Unset, str]):
        category_iexact (Union[Unset, str]):
        category_in (Union[Unset, list[str]]):
        identifier (Union[Unset, str]):
        identifier_icontains (Union[Unset, str]):
        identifier_iexact (Union[Unset, str]):
        identifier_in (Union[Unset, list[str]]):
        make (Union[Unset, str]):
        make_icontains (Union[Unset, str]):
        make_iexact (Union[Unset, str]):
        make_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        subproduct_name (Union[Unset, str]):
        subproduct_name_icontains (Union[Unset, str]):
        subproduct_name_iexact (Union[Unset, str]):
        subproduct_name_in (Union[Unset, list[str]]):
        subsystem (Union[Unset, str]):
        subsystem_icontains (Union[Unset, str]):
        subsystem_iexact (Union[Unset, str]):
        subsystem_in (Union[Unset, list[str]]):
        subvendor_id (Union[Unset, int]):
        subvendor_id_icontains (Union[Unset, int]):
        subvendor_id_iexact (Union[Unset, int]):
        subvendor_id_in (Union[Unset, list[int]]):
        vendor_id (Union[Unset, int]):
        vendor_id_icontains (Union[Unset, int]):
        vendor_id_iexact (Union[Unset, int]):
        vendor_id_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationDevice']
    """

    return sync_detailed(
        client=client,
        bus=bus,
        bus_icontains=bus_icontains,
        bus_iexact=bus_iexact,
        bus_in=bus_in,
        canonical_id=canonical_id,
        canonical_id_icontains=canonical_id_icontains,
        canonical_id_iexact=canonical_id_iexact,
        canonical_id_in=canonical_id_in,
        category=category,
        category_icontains=category_icontains,
        category_iexact=category_iexact,
        category_in=category_in,
        identifier=identifier,
        identifier_icontains=identifier_icontains,
        identifier_iexact=identifier_iexact,
        identifier_in=identifier_in,
        make=make,
        make_icontains=make_icontains,
        make_iexact=make_iexact,
        make_in=make_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        subproduct_name=subproduct_name,
        subproduct_name_icontains=subproduct_name_icontains,
        subproduct_name_iexact=subproduct_name_iexact,
        subproduct_name_in=subproduct_name_in,
        subsystem=subsystem,
        subsystem_icontains=subsystem_icontains,
        subsystem_iexact=subsystem_iexact,
        subsystem_in=subsystem_in,
        subvendor_id=subvendor_id,
        subvendor_id_icontains=subvendor_id_icontains,
        subvendor_id_iexact=subvendor_id_iexact,
        subvendor_id_in=subvendor_id_in,
        vendor_id=vendor_id,
        vendor_id_icontains=vendor_id_icontains,
        vendor_id_iexact=vendor_id_iexact,
        vendor_id_in=vendor_id_in,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    bus: Union[Unset, str] = UNSET,
    bus_icontains: Union[Unset, str] = UNSET,
    bus_iexact: Union[Unset, str] = UNSET,
    bus_in: Union[Unset, list[str]] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_icontains: Union[Unset, str] = UNSET,
    canonical_id_iexact: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, list[str]] = UNSET,
    category: Union[Unset, str] = UNSET,
    category_icontains: Union[Unset, str] = UNSET,
    category_iexact: Union[Unset, str] = UNSET,
    category_in: Union[Unset, list[str]] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    identifier_icontains: Union[Unset, str] = UNSET,
    identifier_iexact: Union[Unset, str] = UNSET,
    identifier_in: Union[Unset, list[str]] = UNSET,
    make: Union[Unset, str] = UNSET,
    make_icontains: Union[Unset, str] = UNSET,
    make_iexact: Union[Unset, str] = UNSET,
    make_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    subproduct_name: Union[Unset, str] = UNSET,
    subproduct_name_icontains: Union[Unset, str] = UNSET,
    subproduct_name_iexact: Union[Unset, str] = UNSET,
    subproduct_name_in: Union[Unset, list[str]] = UNSET,
    subsystem: Union[Unset, str] = UNSET,
    subsystem_icontains: Union[Unset, str] = UNSET,
    subsystem_iexact: Union[Unset, str] = UNSET,
    subsystem_in: Union[Unset, list[str]] = UNSET,
    subvendor_id: Union[Unset, int] = UNSET,
    subvendor_id_icontains: Union[Unset, int] = UNSET,
    subvendor_id_iexact: Union[Unset, int] = UNSET,
    subvendor_id_in: Union[Unset, list[int]] = UNSET,
    vendor_id: Union[Unset, int] = UNSET,
    vendor_id_icontains: Union[Unset, int] = UNSET,
    vendor_id_iexact: Union[Unset, int] = UNSET,
    vendor_id_in: Union[Unset, list[int]] = UNSET,
) -> Response[list["CertifiedConfigurationDevice"]]:
    """
    Args:
        bus (Union[Unset, str]):
        bus_icontains (Union[Unset, str]):
        bus_iexact (Union[Unset, str]):
        bus_in (Union[Unset, list[str]]):
        canonical_id (Union[Unset, str]):
        canonical_id_icontains (Union[Unset, str]):
        canonical_id_iexact (Union[Unset, str]):
        canonical_id_in (Union[Unset, list[str]]):
        category (Union[Unset, str]):
        category_icontains (Union[Unset, str]):
        category_iexact (Union[Unset, str]):
        category_in (Union[Unset, list[str]]):
        identifier (Union[Unset, str]):
        identifier_icontains (Union[Unset, str]):
        identifier_iexact (Union[Unset, str]):
        identifier_in (Union[Unset, list[str]]):
        make (Union[Unset, str]):
        make_icontains (Union[Unset, str]):
        make_iexact (Union[Unset, str]):
        make_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        subproduct_name (Union[Unset, str]):
        subproduct_name_icontains (Union[Unset, str]):
        subproduct_name_iexact (Union[Unset, str]):
        subproduct_name_in (Union[Unset, list[str]]):
        subsystem (Union[Unset, str]):
        subsystem_icontains (Union[Unset, str]):
        subsystem_iexact (Union[Unset, str]):
        subsystem_in (Union[Unset, list[str]]):
        subvendor_id (Union[Unset, int]):
        subvendor_id_icontains (Union[Unset, int]):
        subvendor_id_iexact (Union[Unset, int]):
        subvendor_id_in (Union[Unset, list[int]]):
        vendor_id (Union[Unset, int]):
        vendor_id_icontains (Union[Unset, int]):
        vendor_id_iexact (Union[Unset, int]):
        vendor_id_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CertifiedConfigurationDevice']]
    """

    kwargs = _get_kwargs(
        bus=bus,
        bus_icontains=bus_icontains,
        bus_iexact=bus_iexact,
        bus_in=bus_in,
        canonical_id=canonical_id,
        canonical_id_icontains=canonical_id_icontains,
        canonical_id_iexact=canonical_id_iexact,
        canonical_id_in=canonical_id_in,
        category=category,
        category_icontains=category_icontains,
        category_iexact=category_iexact,
        category_in=category_in,
        identifier=identifier,
        identifier_icontains=identifier_icontains,
        identifier_iexact=identifier_iexact,
        identifier_in=identifier_in,
        make=make,
        make_icontains=make_icontains,
        make_iexact=make_iexact,
        make_in=make_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        subproduct_name=subproduct_name,
        subproduct_name_icontains=subproduct_name_icontains,
        subproduct_name_iexact=subproduct_name_iexact,
        subproduct_name_in=subproduct_name_in,
        subsystem=subsystem,
        subsystem_icontains=subsystem_icontains,
        subsystem_iexact=subsystem_iexact,
        subsystem_in=subsystem_in,
        subvendor_id=subvendor_id,
        subvendor_id_icontains=subvendor_id_icontains,
        subvendor_id_iexact=subvendor_id_iexact,
        subvendor_id_in=subvendor_id_in,
        vendor_id=vendor_id,
        vendor_id_icontains=vendor_id_icontains,
        vendor_id_iexact=vendor_id_iexact,
        vendor_id_in=vendor_id_in,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    bus: Union[Unset, str] = UNSET,
    bus_icontains: Union[Unset, str] = UNSET,
    bus_iexact: Union[Unset, str] = UNSET,
    bus_in: Union[Unset, list[str]] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    canonical_id_icontains: Union[Unset, str] = UNSET,
    canonical_id_iexact: Union[Unset, str] = UNSET,
    canonical_id_in: Union[Unset, list[str]] = UNSET,
    category: Union[Unset, str] = UNSET,
    category_icontains: Union[Unset, str] = UNSET,
    category_iexact: Union[Unset, str] = UNSET,
    category_in: Union[Unset, list[str]] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    identifier_icontains: Union[Unset, str] = UNSET,
    identifier_iexact: Union[Unset, str] = UNSET,
    identifier_in: Union[Unset, list[str]] = UNSET,
    make: Union[Unset, str] = UNSET,
    make_icontains: Union[Unset, str] = UNSET,
    make_iexact: Union[Unset, str] = UNSET,
    make_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    subproduct_name: Union[Unset, str] = UNSET,
    subproduct_name_icontains: Union[Unset, str] = UNSET,
    subproduct_name_iexact: Union[Unset, str] = UNSET,
    subproduct_name_in: Union[Unset, list[str]] = UNSET,
    subsystem: Union[Unset, str] = UNSET,
    subsystem_icontains: Union[Unset, str] = UNSET,
    subsystem_iexact: Union[Unset, str] = UNSET,
    subsystem_in: Union[Unset, list[str]] = UNSET,
    subvendor_id: Union[Unset, int] = UNSET,
    subvendor_id_icontains: Union[Unset, int] = UNSET,
    subvendor_id_iexact: Union[Unset, int] = UNSET,
    subvendor_id_in: Union[Unset, list[int]] = UNSET,
    vendor_id: Union[Unset, int] = UNSET,
    vendor_id_icontains: Union[Unset, int] = UNSET,
    vendor_id_iexact: Union[Unset, int] = UNSET,
    vendor_id_in: Union[Unset, list[int]] = UNSET,
) -> Optional[list["CertifiedConfigurationDevice"]]:
    """
    Args:
        bus (Union[Unset, str]):
        bus_icontains (Union[Unset, str]):
        bus_iexact (Union[Unset, str]):
        bus_in (Union[Unset, list[str]]):
        canonical_id (Union[Unset, str]):
        canonical_id_icontains (Union[Unset, str]):
        canonical_id_iexact (Union[Unset, str]):
        canonical_id_in (Union[Unset, list[str]]):
        category (Union[Unset, str]):
        category_icontains (Union[Unset, str]):
        category_iexact (Union[Unset, str]):
        category_in (Union[Unset, list[str]]):
        identifier (Union[Unset, str]):
        identifier_icontains (Union[Unset, str]):
        identifier_iexact (Union[Unset, str]):
        identifier_in (Union[Unset, list[str]]):
        make (Union[Unset, str]):
        make_icontains (Union[Unset, str]):
        make_iexact (Union[Unset, str]):
        make_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        subproduct_name (Union[Unset, str]):
        subproduct_name_icontains (Union[Unset, str]):
        subproduct_name_iexact (Union[Unset, str]):
        subproduct_name_in (Union[Unset, list[str]]):
        subsystem (Union[Unset, str]):
        subsystem_icontains (Union[Unset, str]):
        subsystem_iexact (Union[Unset, str]):
        subsystem_in (Union[Unset, list[str]]):
        subvendor_id (Union[Unset, int]):
        subvendor_id_icontains (Union[Unset, int]):
        subvendor_id_iexact (Union[Unset, int]):
        subvendor_id_in (Union[Unset, list[int]]):
        vendor_id (Union[Unset, int]):
        vendor_id_icontains (Union[Unset, int]):
        vendor_id_iexact (Union[Unset, int]):
        vendor_id_in (Union[Unset, list[int]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CertifiedConfigurationDevice']
    """

    return (
        await asyncio_detailed(
            client=client,
            bus=bus,
            bus_icontains=bus_icontains,
            bus_iexact=bus_iexact,
            bus_in=bus_in,
            canonical_id=canonical_id,
            canonical_id_icontains=canonical_id_icontains,
            canonical_id_iexact=canonical_id_iexact,
            canonical_id_in=canonical_id_in,
            category=category,
            category_icontains=category_icontains,
            category_iexact=category_iexact,
            category_in=category_in,
            identifier=identifier,
            identifier_icontains=identifier_icontains,
            identifier_iexact=identifier_iexact,
            identifier_in=identifier_in,
            make=make,
            make_icontains=make_icontains,
            make_iexact=make_iexact,
            make_in=make_in,
            name=name,
            name_icontains=name_icontains,
            name_iexact=name_iexact,
            name_in=name_in,
            ordering=ordering,
            subproduct_name=subproduct_name,
            subproduct_name_icontains=subproduct_name_icontains,
            subproduct_name_iexact=subproduct_name_iexact,
            subproduct_name_in=subproduct_name_in,
            subsystem=subsystem,
            subsystem_icontains=subsystem_icontains,
            subsystem_iexact=subsystem_iexact,
            subsystem_in=subsystem_in,
            subvendor_id=subvendor_id,
            subvendor_id_icontains=subvendor_id_icontains,
            subvendor_id_iexact=subvendor_id_iexact,
            subvendor_id_in=subvendor_id_in,
            vendor_id=vendor_id,
            vendor_id_icontains=vendor_id_icontains,
            vendor_id_iexact=vendor_id_iexact,
            vendor_id_in=vendor_id_in,
        )
    ).parsed
