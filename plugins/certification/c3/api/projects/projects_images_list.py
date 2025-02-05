from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.image import Image
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    buildstamp_name: Union[Unset, str] = UNSET,
    buildstamp_name_contains: Union[Unset, str] = UNSET,
    buildstamp_name_icontains: Union[Unset, str] = UNSET,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_isnull: Union[Unset, bool] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_contains: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, int] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_name_contains: Union[Unset, str] = UNSET,
    project_name_icontains: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["buildstamp__name"] = buildstamp_name

    params["buildstamp__name__contains"] = buildstamp_name_contains

    params["buildstamp__name__icontains"] = buildstamp_name_icontains

    params["created_at__day"] = created_at_day

    params["created_at__isnull"] = created_at_isnull

    params["created_at__month"] = created_at_month

    params["created_at__year"] = created_at_year

    params["name"] = name

    params["name__contains"] = name_contains

    params["name__icontains"] = name_icontains

    params["ordering"] = ordering

    params["project"] = project

    params["project__name"] = project_name

    params["project__name__contains"] = project_name_contains

    params["project__name__icontains"] = project_name_icontains

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/projects/images/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["Image"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_paginated_image_list_item_data in _response_200:
            componentsschemas_paginated_image_list_item = Image.from_dict(
                componentsschemas_paginated_image_list_item_data
            )

            response_200.append(componentsschemas_paginated_image_list_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Image"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    buildstamp_name: Union[Unset, str] = UNSET,
    buildstamp_name_contains: Union[Unset, str] = UNSET,
    buildstamp_name_icontains: Union[Unset, str] = UNSET,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_isnull: Union[Unset, bool] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_contains: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, int] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_name_contains: Union[Unset, str] = UNSET,
    project_name_icontains: Union[Unset, str] = UNSET,
) -> Response[list["Image"]]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        buildstamp_name (Union[Unset, str]):
        buildstamp_name_contains (Union[Unset, str]):
        buildstamp_name_icontains (Union[Unset, str]):
        created_at_day (Union[Unset, float]):
        created_at_isnull (Union[Unset, bool]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        name (Union[Unset, str]):
        name_contains (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, int]):
        project_name (Union[Unset, str]):
        project_name_contains (Union[Unset, str]):
        project_name_icontains (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Image']]
    """

    kwargs = _get_kwargs(
        buildstamp_name=buildstamp_name,
        buildstamp_name_contains=buildstamp_name_contains,
        buildstamp_name_icontains=buildstamp_name_icontains,
        created_at_day=created_at_day,
        created_at_isnull=created_at_isnull,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        name=name,
        name_contains=name_contains,
        name_icontains=name_icontains,
        ordering=ordering,
        project=project,
        project_name=project_name,
        project_name_contains=project_name_contains,
        project_name_icontains=project_name_icontains,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    buildstamp_name: Union[Unset, str] = UNSET,
    buildstamp_name_contains: Union[Unset, str] = UNSET,
    buildstamp_name_icontains: Union[Unset, str] = UNSET,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_isnull: Union[Unset, bool] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_contains: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, int] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_name_contains: Union[Unset, str] = UNSET,
    project_name_icontains: Union[Unset, str] = UNSET,
) -> Optional[list["Image"]]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        buildstamp_name (Union[Unset, str]):
        buildstamp_name_contains (Union[Unset, str]):
        buildstamp_name_icontains (Union[Unset, str]):
        created_at_day (Union[Unset, float]):
        created_at_isnull (Union[Unset, bool]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        name (Union[Unset, str]):
        name_contains (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, int]):
        project_name (Union[Unset, str]):
        project_name_contains (Union[Unset, str]):
        project_name_icontains (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Image']
    """

    return sync_detailed(
        client=client,
        buildstamp_name=buildstamp_name,
        buildstamp_name_contains=buildstamp_name_contains,
        buildstamp_name_icontains=buildstamp_name_icontains,
        created_at_day=created_at_day,
        created_at_isnull=created_at_isnull,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        name=name,
        name_contains=name_contains,
        name_icontains=name_icontains,
        ordering=ordering,
        project=project,
        project_name=project_name,
        project_name_contains=project_name_contains,
        project_name_icontains=project_name_icontains,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    buildstamp_name: Union[Unset, str] = UNSET,
    buildstamp_name_contains: Union[Unset, str] = UNSET,
    buildstamp_name_icontains: Union[Unset, str] = UNSET,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_isnull: Union[Unset, bool] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_contains: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, int] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_name_contains: Union[Unset, str] = UNSET,
    project_name_icontains: Union[Unset, str] = UNSET,
) -> Response[list["Image"]]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        buildstamp_name (Union[Unset, str]):
        buildstamp_name_contains (Union[Unset, str]):
        buildstamp_name_icontains (Union[Unset, str]):
        created_at_day (Union[Unset, float]):
        created_at_isnull (Union[Unset, bool]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        name (Union[Unset, str]):
        name_contains (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, int]):
        project_name (Union[Unset, str]):
        project_name_contains (Union[Unset, str]):
        project_name_icontains (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Image']]
    """

    kwargs = _get_kwargs(
        buildstamp_name=buildstamp_name,
        buildstamp_name_contains=buildstamp_name_contains,
        buildstamp_name_icontains=buildstamp_name_icontains,
        created_at_day=created_at_day,
        created_at_isnull=created_at_isnull,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        name=name,
        name_contains=name_contains,
        name_icontains=name_icontains,
        ordering=ordering,
        project=project,
        project_name=project_name,
        project_name_contains=project_name_contains,
        project_name_icontains=project_name_icontains,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    buildstamp_name: Union[Unset, str] = UNSET,
    buildstamp_name_contains: Union[Unset, str] = UNSET,
    buildstamp_name_icontains: Union[Unset, str] = UNSET,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_isnull: Union[Unset, bool] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_contains: Union[Unset, str] = UNSET,
    name_icontains: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, int] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_name_contains: Union[Unset, str] = UNSET,
    project_name_icontains: Union[Unset, str] = UNSET,
) -> Optional[list["Image"]]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        buildstamp_name (Union[Unset, str]):
        buildstamp_name_contains (Union[Unset, str]):
        buildstamp_name_icontains (Union[Unset, str]):
        created_at_day (Union[Unset, float]):
        created_at_isnull (Union[Unset, bool]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        name (Union[Unset, str]):
        name_contains (Union[Unset, str]):
        name_icontains (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, int]):
        project_name (Union[Unset, str]):
        project_name_contains (Union[Unset, str]):
        project_name_icontains (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Image']
    """

    return (
        await asyncio_detailed(
            client=client,
            buildstamp_name=buildstamp_name,
            buildstamp_name_contains=buildstamp_name_contains,
            buildstamp_name_icontains=buildstamp_name_icontains,
            created_at_day=created_at_day,
            created_at_isnull=created_at_isnull,
            created_at_month=created_at_month,
            created_at_year=created_at_year,
            name=name,
            name_contains=name_contains,
            name_icontains=name_icontains,
            ordering=ordering,
            project=project,
            project_name=project_name,
            project_name_contains=project_name_contains,
            project_name_icontains=project_name_icontains,
        )
    ).parsed
