from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.public_certificate import PublicCertificate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    hardware_canonical_id: Union[Unset, str] = UNSET,
    hardware_canonical_id_icontains: Union[Unset, str] = UNSET,
    hardware_canonical_id_iexact: Union[Unset, str] = UNSET,
    hardware_canonical_id_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_arch_name: Union[Unset, str] = UNSET,
    report_arch_name_icontains: Union[Unset, str] = UNSET,
    report_arch_name_iexact: Union[Unset, str] = UNSET,
    report_arch_name_in: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["hardware__canonical_id"] = hardware_canonical_id

    params["hardware__canonical_id__icontains"] = hardware_canonical_id_icontains

    params["hardware__canonical_id__iexact"] = hardware_canonical_id_iexact

    json_hardware_canonical_id_in: Union[Unset, list[str]] = UNSET
    if not isinstance(hardware_canonical_id_in, Unset):
        json_hardware_canonical_id_in = hardware_canonical_id_in

    params["hardware__canonical_id__in"] = json_hardware_canonical_id_in

    params["name"] = name

    params["name__icontains"] = name_icontains

    params["name__iexact"] = name_iexact

    json_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(name_in, Unset):
        json_name_in = name_in

    params["name__in"] = json_name_in

    params["ordering"] = ordering

    params["report__arch__name"] = report_arch_name

    params["report__arch__name__icontains"] = report_arch_name_icontains

    params["report__arch__name__iexact"] = report_arch_name_iexact

    json_report_arch_name_in: Union[Unset, list[str]] = UNSET
    if not isinstance(report_arch_name_in, Unset):
        json_report_arch_name_in = report_arch_name_in

    params["report__arch__name__in"] = json_report_arch_name_in

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/public-certificates/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["PublicCertificate"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for (
            componentsschemas_paginated_public_certificate_list_item_data
        ) in _response_200:
            componentsschemas_paginated_public_certificate_list_item = (
                PublicCertificate.from_dict(
                    componentsschemas_paginated_public_certificate_list_item_data
                )
            )

            response_200.append(
                componentsschemas_paginated_public_certificate_list_item
            )

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PublicCertificate"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    hardware_canonical_id: Union[Unset, str] = UNSET,
    hardware_canonical_id_icontains: Union[Unset, str] = UNSET,
    hardware_canonical_id_iexact: Union[Unset, str] = UNSET,
    hardware_canonical_id_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_arch_name: Union[Unset, str] = UNSET,
    report_arch_name_icontains: Union[Unset, str] = UNSET,
    report_arch_name_iexact: Union[Unset, str] = UNSET,
    report_arch_name_in: Union[Unset, list[str]] = UNSET,
) -> Response[list["PublicCertificate"]]:
    """
    Args:
        hardware_canonical_id (Union[Unset, str]):
        hardware_canonical_id_icontains (Union[Unset, str]):
        hardware_canonical_id_iexact (Union[Unset, str]):
        hardware_canonical_id_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_arch_name (Union[Unset, str]):
        report_arch_name_icontains (Union[Unset, str]):
        report_arch_name_iexact (Union[Unset, str]):
        report_arch_name_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PublicCertificate']]
    """

    kwargs = _get_kwargs(
        hardware_canonical_id=hardware_canonical_id,
        hardware_canonical_id_icontains=hardware_canonical_id_icontains,
        hardware_canonical_id_iexact=hardware_canonical_id_iexact,
        hardware_canonical_id_in=hardware_canonical_id_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        report_arch_name=report_arch_name,
        report_arch_name_icontains=report_arch_name_icontains,
        report_arch_name_iexact=report_arch_name_iexact,
        report_arch_name_in=report_arch_name_in,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    hardware_canonical_id: Union[Unset, str] = UNSET,
    hardware_canonical_id_icontains: Union[Unset, str] = UNSET,
    hardware_canonical_id_iexact: Union[Unset, str] = UNSET,
    hardware_canonical_id_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_arch_name: Union[Unset, str] = UNSET,
    report_arch_name_icontains: Union[Unset, str] = UNSET,
    report_arch_name_iexact: Union[Unset, str] = UNSET,
    report_arch_name_in: Union[Unset, list[str]] = UNSET,
) -> Optional[list["PublicCertificate"]]:
    """
    Args:
        hardware_canonical_id (Union[Unset, str]):
        hardware_canonical_id_icontains (Union[Unset, str]):
        hardware_canonical_id_iexact (Union[Unset, str]):
        hardware_canonical_id_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_arch_name (Union[Unset, str]):
        report_arch_name_icontains (Union[Unset, str]):
        report_arch_name_iexact (Union[Unset, str]):
        report_arch_name_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PublicCertificate']
    """

    return sync_detailed(
        client=client,
        hardware_canonical_id=hardware_canonical_id,
        hardware_canonical_id_icontains=hardware_canonical_id_icontains,
        hardware_canonical_id_iexact=hardware_canonical_id_iexact,
        hardware_canonical_id_in=hardware_canonical_id_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        report_arch_name=report_arch_name,
        report_arch_name_icontains=report_arch_name_icontains,
        report_arch_name_iexact=report_arch_name_iexact,
        report_arch_name_in=report_arch_name_in,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    hardware_canonical_id: Union[Unset, str] = UNSET,
    hardware_canonical_id_icontains: Union[Unset, str] = UNSET,
    hardware_canonical_id_iexact: Union[Unset, str] = UNSET,
    hardware_canonical_id_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_arch_name: Union[Unset, str] = UNSET,
    report_arch_name_icontains: Union[Unset, str] = UNSET,
    report_arch_name_iexact: Union[Unset, str] = UNSET,
    report_arch_name_in: Union[Unset, list[str]] = UNSET,
) -> Response[list["PublicCertificate"]]:
    """
    Args:
        hardware_canonical_id (Union[Unset, str]):
        hardware_canonical_id_icontains (Union[Unset, str]):
        hardware_canonical_id_iexact (Union[Unset, str]):
        hardware_canonical_id_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_arch_name (Union[Unset, str]):
        report_arch_name_icontains (Union[Unset, str]):
        report_arch_name_iexact (Union[Unset, str]):
        report_arch_name_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PublicCertificate']]
    """

    kwargs = _get_kwargs(
        hardware_canonical_id=hardware_canonical_id,
        hardware_canonical_id_icontains=hardware_canonical_id_icontains,
        hardware_canonical_id_iexact=hardware_canonical_id_iexact,
        hardware_canonical_id_in=hardware_canonical_id_in,
        name=name,
        name_icontains=name_icontains,
        name_iexact=name_iexact,
        name_in=name_in,
        ordering=ordering,
        report_arch_name=report_arch_name,
        report_arch_name_icontains=report_arch_name_icontains,
        report_arch_name_iexact=report_arch_name_iexact,
        report_arch_name_in=report_arch_name_in,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    hardware_canonical_id: Union[Unset, str] = UNSET,
    hardware_canonical_id_icontains: Union[Unset, str] = UNSET,
    hardware_canonical_id_iexact: Union[Unset, str] = UNSET,
    hardware_canonical_id_in: Union[Unset, list[str]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    name_iexact: Union[Unset, str] = UNSET,
    name_in: Union[Unset, list[str]] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    report_arch_name: Union[Unset, str] = UNSET,
    report_arch_name_icontains: Union[Unset, str] = UNSET,
    report_arch_name_iexact: Union[Unset, str] = UNSET,
    report_arch_name_in: Union[Unset, list[str]] = UNSET,
) -> Optional[list["PublicCertificate"]]:
    """
    Args:
        hardware_canonical_id (Union[Unset, str]):
        hardware_canonical_id_icontains (Union[Unset, str]):
        hardware_canonical_id_iexact (Union[Unset, str]):
        hardware_canonical_id_in (Union[Unset, list[str]]):
        name (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        name_iexact (Union[Unset, str]):
        name_in (Union[Unset, list[str]]):
        ordering (Union[Unset, str]):
        report_arch_name (Union[Unset, str]):
        report_arch_name_icontains (Union[Unset, str]):
        report_arch_name_iexact (Union[Unset, str]):
        report_arch_name_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PublicCertificate']
    """

    return (
        await asyncio_detailed(
            client=client,
            hardware_canonical_id=hardware_canonical_id,
            hardware_canonical_id_icontains=hardware_canonical_id_icontains,
            hardware_canonical_id_iexact=hardware_canonical_id_iexact,
            hardware_canonical_id_in=hardware_canonical_id_in,
            name=name,
            name_icontains=name_icontains,
            name_iexact=name_iexact,
            name_in=name_in,
            ordering=ordering,
            report_arch_name=report_arch_name,
            report_arch_name_icontains=report_arch_name_icontains,
            report_arch_name_iexact=report_arch_name_iexact,
            report_arch_name_in=report_arch_name_in,
        )
    ).parsed
