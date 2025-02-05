from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.public_device_instance import PublicDeviceInstance
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    device_category_name: Union[Unset, str] = UNSET,
    device_category_name_icontains: Union[Unset, str] = UNSET,
    device_category_name_iexact: Union[Unset, str] = UNSET,
    device_category_name_in: Union[Unset, list[str]] = UNSET,
    device_identifier: Union[Unset, str] = UNSET,
    device_identifier_icontains: Union[Unset, str] = UNSET,
    device_identifier_iexact: Union[Unset, str] = UNSET,
    device_identifier_in: Union[Unset, list[str]] = UNSET,
    device_name: Union[Unset, str] = UNSET,
    device_name_icontains: Union[Unset, str] = UNSET,
    device_name_iexact: Union[Unset, str] = UNSET,
    device_name_in: Union[Unset, list[str]] = UNSET,
    device_vendor_name: Union[Unset, str] = UNSET,
    device_vendor_name_icontains: Union[Unset, str] = UNSET,
    device_vendor_name_iexact: Union[Unset, str] = UNSET,
    device_vendor_name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_icontains: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_iexact: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["device__category__name"] = device_category_name

    params["device__category__name__icontains"] = device_category_name_icontains

    params["device__category__name__iexact"] = device_category_name_iexact

    json_device_category_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(device_category_name_in, Unset):
        json_device_category_name_in = device_category_name_in

    params["device__category__name__in"] = json_device_category_name_in

    params["device__identifier"] = device_identifier

    params["device__identifier__icontains"] = device_identifier_icontains

    params["device__identifier__iexact"] = device_identifier_iexact

    json_device_identifier_in: Union[Unset, list[str]] = UNSET
    if not isinstance(device_identifier_in, Unset):
        json_device_identifier_in = device_identifier_in

    params["device__identifier__in"] = json_device_identifier_in

    params["device__name"] = device_name

    params["device__name__icontains"] = device_name_icontains

    params["device__name__iexact"] = device_name_iexact

    json_device_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(device_name_in, Unset):
        json_device_name_in = device_name_in

    params["device__name__in"] = json_device_name_in

    params["device__vendor__name"] = device_vendor_name

    params["device__vendor__name__icontains"] = device_vendor_name_icontains

    params["device__vendor__name__iexact"] = device_vendor_name_iexact

    json_device_vendor_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(device_vendor_name_in, Unset):
        json_device_vendor_name_in = device_vendor_name_in

    params["device__vendor__name__in"] = json_device_vendor_name_in

    params["ordering"] = ordering

    params["report__physical_machine__canonical_id"] = (
        report_physical_machine_canonical_id
    )

    params["report__physical_machine__canonical_id__icontains"] = (
        report_physical_machine_canonical_id_icontains
    )

    params["report__physical_machine__canonical_id__iexact"] = (
        report_physical_machine_canonical_id_iexact
    )

    json_report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET
    if not isinstance(report_physical_machine_canonical_id_in, Unset):
        json_report_physical_machine_canonical_id_in = (
            report_physical_machine_canonical_id_in
        )

    params["report__physical_machine__canonical_id__in"] = (
        json_report_physical_machine_canonical_id_in
    )

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/public-devices/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["PublicDeviceInstance"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_public_device_instance_list_item_data
        ) in _response_200:
            componentsschemas_paginated_public_device_instance_list_item = (
                PublicDeviceInstance.from_dict(
                    componentsschemas_paginated_public_device_instance_list_item_data
                )
            )

            response_200.append(
                componentsschemas_paginated_public_device_instance_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PublicDeviceInstance"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    device_category_name: Union[Unset, str] = UNSET,
    device_category_name_icontains: Union[Unset, str] = UNSET,
    device_category_name_iexact: Union[Unset, str] = UNSET,
    device_category_name_in: Union[Unset, list[str]] = UNSET,
    device_identifier: Union[Unset, str] = UNSET,
    device_identifier_icontains: Union[Unset, str] = UNSET,
    device_identifier_iexact: Union[Unset, str] = UNSET,
    device_identifier_in: Union[Unset, list[str]] = UNSET,
    device_name: Union[Unset, str] = UNSET,
    device_name_icontains: Union[Unset, str] = UNSET,
    device_name_iexact: Union[Unset, str] = UNSET,
    device_name_in: Union[Unset, list[str]] = UNSET,
    device_vendor_name: Union[Unset, str] = UNSET,
    device_vendor_name_icontains: Union[Unset, str] = UNSET,
    device_vendor_name_iexact: Union[Unset, str] = UNSET,
    device_vendor_name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_icontains: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_iexact: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET,
) -> Response[list["PublicDeviceInstance"]]:
    """Public API for showing devices from the reports attached to certificates

    Args:
        device_category_name (Union[Unset, str]):
        device_category_name_icontains (Union[Unset, str]):
        device_category_name_iexact (Union[Unset, str]):
        device_category_name_in (Union[Unset, list[str]]):
        device_identifier (Union[Unset, str]):
        device_identifier_icontains (Union[Unset, str]):
        device_identifier_iexact (Union[Unset, str]):
        device_identifier_in (Union[Unset, list[str]]):
        device_name (Union[Unset, str]):
        device_name_icontains (Union[Unset, str]):
        device_name_iexact (Union[Unset, str]):
        device_name_in (Union[Unset, list[str]]):
        device_vendor_name (Union[Unset, str]):
        device_vendor_name_icontains (Union[Unset, str]):
        device_vendor_name_iexact (Union[Unset, str]):
        device_vendor_name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_physical_machine_canonical_id (Union[Unset, str]):
        report_physical_machine_canonical_id_icontains (Union[Unset, str]):
        report_physical_machine_canonical_id_iexact (Union[Unset, str]):
        report_physical_machine_canonical_id_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PublicDeviceInstance']]
    """

    kwargs = _get_kwargs(
        device_category_name=device_category_name,
        device_category_name_icontains=device_category_name_icontains,
        device_category_name_iexact=device_category_name_iexact,
        device_category_name_in=device_category_name_in,
        device_identifier=device_identifier,
        device_identifier_icontains=device_identifier_icontains,
        device_identifier_iexact=device_identifier_iexact,
        device_identifier_in=device_identifier_in,
        device_name=device_name,
        device_name_icontains=device_name_icontains,
        device_name_iexact=device_name_iexact,
        device_name_in=device_name_in,
        device_vendor_name=device_vendor_name,
        device_vendor_name_icontains=device_vendor_name_icontains,
        device_vendor_name_iexact=device_vendor_name_iexact,
        device_vendor_name_in=device_vendor_name_in,
        ordering=ordering,
        report_physical_machine_canonical_id=report_physical_machine_canonical_id,
        report_physical_machine_canonical_id_icontains=report_physical_machine_canonical_id_icontains,
        report_physical_machine_canonical_id_iexact=report_physical_machine_canonical_id_iexact,
        report_physical_machine_canonical_id_in=report_physical_machine_canonical_id_in,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    device_category_name: Union[Unset, str] = UNSET,
    device_category_name_icontains: Union[Unset, str] = UNSET,
    device_category_name_iexact: Union[Unset, str] = UNSET,
    device_category_name_in: Union[Unset, list[str]] = UNSET,
    device_identifier: Union[Unset, str] = UNSET,
    device_identifier_icontains: Union[Unset, str] = UNSET,
    device_identifier_iexact: Union[Unset, str] = UNSET,
    device_identifier_in: Union[Unset, list[str]] = UNSET,
    device_name: Union[Unset, str] = UNSET,
    device_name_icontains: Union[Unset, str] = UNSET,
    device_name_iexact: Union[Unset, str] = UNSET,
    device_name_in: Union[Unset, list[str]] = UNSET,
    device_vendor_name: Union[Unset, str] = UNSET,
    device_vendor_name_icontains: Union[Unset, str] = UNSET,
    device_vendor_name_iexact: Union[Unset, str] = UNSET,
    device_vendor_name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_icontains: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_iexact: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET,
) -> Optional[list["PublicDeviceInstance"]]:
    """Public API for showing devices from the reports attached to certificates

    Args:
        device_category_name (Union[Unset, str]):
        device_category_name_icontains (Union[Unset, str]):
        device_category_name_iexact (Union[Unset, str]):
        device_category_name_in (Union[Unset, list[str]]):
        device_identifier (Union[Unset, str]):
        device_identifier_icontains (Union[Unset, str]):
        device_identifier_iexact (Union[Unset, str]):
        device_identifier_in (Union[Unset, list[str]]):
        device_name (Union[Unset, str]):
        device_name_icontains (Union[Unset, str]):
        device_name_iexact (Union[Unset, str]):
        device_name_in (Union[Unset, list[str]]):
        device_vendor_name (Union[Unset, str]):
        device_vendor_name_icontains (Union[Unset, str]):
        device_vendor_name_iexact (Union[Unset, str]):
        device_vendor_name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_physical_machine_canonical_id (Union[Unset, str]):
        report_physical_machine_canonical_id_icontains (Union[Unset, str]):
        report_physical_machine_canonical_id_iexact (Union[Unset, str]):
        report_physical_machine_canonical_id_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PublicDeviceInstance']
    """

    return sync_detailed(
        client=client,
        device_category_name=device_category_name,
        device_category_name_icontains=device_category_name_icontains,
        device_category_name_iexact=device_category_name_iexact,
        device_category_name_in=device_category_name_in,
        device_identifier=device_identifier,
        device_identifier_icontains=device_identifier_icontains,
        device_identifier_iexact=device_identifier_iexact,
        device_identifier_in=device_identifier_in,
        device_name=device_name,
        device_name_icontains=device_name_icontains,
        device_name_iexact=device_name_iexact,
        device_name_in=device_name_in,
        device_vendor_name=device_vendor_name,
        device_vendor_name_icontains=device_vendor_name_icontains,
        device_vendor_name_iexact=device_vendor_name_iexact,
        device_vendor_name_in=device_vendor_name_in,
        ordering=ordering,
        report_physical_machine_canonical_id=report_physical_machine_canonical_id,
        report_physical_machine_canonical_id_icontains=report_physical_machine_canonical_id_icontains,
        report_physical_machine_canonical_id_iexact=report_physical_machine_canonical_id_iexact,
        report_physical_machine_canonical_id_in=report_physical_machine_canonical_id_in,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    device_category_name: Union[Unset, str] = UNSET,
    device_category_name_icontains: Union[Unset, str] = UNSET,
    device_category_name_iexact: Union[Unset, str] = UNSET,
    device_category_name_in: Union[Unset, list[str]] = UNSET,
    device_identifier: Union[Unset, str] = UNSET,
    device_identifier_icontains: Union[Unset, str] = UNSET,
    device_identifier_iexact: Union[Unset, str] = UNSET,
    device_identifier_in: Union[Unset, list[str]] = UNSET,
    device_name: Union[Unset, str] = UNSET,
    device_name_icontains: Union[Unset, str] = UNSET,
    device_name_iexact: Union[Unset, str] = UNSET,
    device_name_in: Union[Unset, list[str]] = UNSET,
    device_vendor_name: Union[Unset, str] = UNSET,
    device_vendor_name_icontains: Union[Unset, str] = UNSET,
    device_vendor_name_iexact: Union[Unset, str] = UNSET,
    device_vendor_name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_icontains: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_iexact: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET,
) -> Response[list["PublicDeviceInstance"]]:
    """Public API for showing devices from the reports attached to certificates

    Args:
        device_category_name (Union[Unset, str]):
        device_category_name_icontains (Union[Unset, str]):
        device_category_name_iexact (Union[Unset, str]):
        device_category_name_in (Union[Unset, list[str]]):
        device_identifier (Union[Unset, str]):
        device_identifier_icontains (Union[Unset, str]):
        device_identifier_iexact (Union[Unset, str]):
        device_identifier_in (Union[Unset, list[str]]):
        device_name (Union[Unset, str]):
        device_name_icontains (Union[Unset, str]):
        device_name_iexact (Union[Unset, str]):
        device_name_in (Union[Unset, list[str]]):
        device_vendor_name (Union[Unset, str]):
        device_vendor_name_icontains (Union[Unset, str]):
        device_vendor_name_iexact (Union[Unset, str]):
        device_vendor_name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_physical_machine_canonical_id (Union[Unset, str]):
        report_physical_machine_canonical_id_icontains (Union[Unset, str]):
        report_physical_machine_canonical_id_iexact (Union[Unset, str]):
        report_physical_machine_canonical_id_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PublicDeviceInstance']]
    """

    kwargs = _get_kwargs(
        device_category_name=device_category_name,
        device_category_name_icontains=device_category_name_icontains,
        device_category_name_iexact=device_category_name_iexact,
        device_category_name_in=device_category_name_in,
        device_identifier=device_identifier,
        device_identifier_icontains=device_identifier_icontains,
        device_identifier_iexact=device_identifier_iexact,
        device_identifier_in=device_identifier_in,
        device_name=device_name,
        device_name_icontains=device_name_icontains,
        device_name_iexact=device_name_iexact,
        device_name_in=device_name_in,
        device_vendor_name=device_vendor_name,
        device_vendor_name_icontains=device_vendor_name_icontains,
        device_vendor_name_iexact=device_vendor_name_iexact,
        device_vendor_name_in=device_vendor_name_in,
        ordering=ordering,
        report_physical_machine_canonical_id=report_physical_machine_canonical_id,
        report_physical_machine_canonical_id_icontains=report_physical_machine_canonical_id_icontains,
        report_physical_machine_canonical_id_iexact=report_physical_machine_canonical_id_iexact,
        report_physical_machine_canonical_id_in=report_physical_machine_canonical_id_in,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    device_category_name: Union[Unset, str] = UNSET,
    device_category_name_icontains: Union[Unset, str] = UNSET,
    device_category_name_iexact: Union[Unset, str] = UNSET,
    device_category_name_in: Union[Unset, list[str]] = UNSET,
    device_identifier: Union[Unset, str] = UNSET,
    device_identifier_icontains: Union[Unset, str] = UNSET,
    device_identifier_iexact: Union[Unset, str] = UNSET,
    device_identifier_in: Union[Unset, list[str]] = UNSET,
    device_name: Union[Unset, str] = UNSET,
    device_name_icontains: Union[Unset, str] = UNSET,
    device_name_iexact: Union[Unset, str] = UNSET,
    device_name_in: Union[Unset, list[str]] = UNSET,
    device_vendor_name: Union[Unset, str] = UNSET,
    device_vendor_name_icontains: Union[Unset, str] = UNSET,
    device_vendor_name_iexact: Union[Unset, str] = UNSET,
    device_vendor_name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_icontains: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_iexact: Union[Unset, str] = UNSET,
    report_physical_machine_canonical_id_in: Union[Unset, list[str]] = UNSET,
) -> Optional[list["PublicDeviceInstance"]]:
    """Public API for showing devices from the reports attached to certificates

    Args:
        device_category_name (Union[Unset, str]):
        device_category_name_icontains (Union[Unset, str]):
        device_category_name_iexact (Union[Unset, str]):
        device_category_name_in (Union[Unset, list[str]]):
        device_identifier (Union[Unset, str]):
        device_identifier_icontains (Union[Unset, str]):
        device_identifier_iexact (Union[Unset, str]):
        device_identifier_in (Union[Unset, list[str]]):
        device_name (Union[Unset, str]):
        device_name_icontains (Union[Unset, str]):
        device_name_iexact (Union[Unset, str]):
        device_name_in (Union[Unset, list[str]]):
        device_vendor_name (Union[Unset, str]):
        device_vendor_name_icontains (Union[Unset, str]):
        device_vendor_name_iexact (Union[Unset, str]):
        device_vendor_name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_physical_machine_canonical_id (Union[Unset, str]):
        report_physical_machine_canonical_id_icontains (Union[Unset, str]):
        report_physical_machine_canonical_id_iexact (Union[Unset, str]):
        report_physical_machine_canonical_id_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PublicDeviceInstance']
    """

    return (
        await asyncio_detailed(
            client=client,
            device_category_name=device_category_name,
            device_category_name_icontains=device_category_name_icontains,
            device_category_name_iexact=device_category_name_iexact,
            device_category_name_in=device_category_name_in,
            device_identifier=device_identifier,
            device_identifier_icontains=device_identifier_icontains,
            device_identifier_iexact=device_identifier_iexact,
            device_identifier_in=device_identifier_in,
            device_name=device_name,
            device_name_icontains=device_name_icontains,
            device_name_iexact=device_name_iexact,
            device_name_in=device_name_in,
            device_vendor_name=device_vendor_name,
            device_vendor_name_icontains=device_vendor_name_icontains,
            device_vendor_name_iexact=device_vendor_name_iexact,
            device_vendor_name_in=device_vendor_name_in,
            ordering=ordering,
            report_physical_machine_canonical_id=report_physical_machine_canonical_id,
            report_physical_machine_canonical_id_icontains=report_physical_machine_canonical_id_icontains,
            report_physical_machine_canonical_id_iexact=report_physical_machine_canonical_id_iexact,
            report_physical_machine_canonical_id_in=report_physical_machine_canonical_id_in,
        )
    ).parsed
