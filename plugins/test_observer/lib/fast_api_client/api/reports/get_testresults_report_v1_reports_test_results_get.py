import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_date: Union[Unset, datetime.datetime] = isoparse("0001-01-01T00:00:00"),
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date: Union[None, Unset, str]
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    elif isinstance(end_date, datetime.datetime):
        json_end_date = end_date.isoformat()
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/reports/test-results",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("0001-01-01T00:00:00"),
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Testresults Report

     Returns a csv report detailing all artefacts within a given date range. Together
    with their test executions and test results in csv format.

    Args:
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('0001-01-01T00:00:00').
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("0001-01-01T00:00:00"),
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Testresults Report

     Returns a csv report detailing all artefacts within a given date range. Together
    with their test executions and test results in csv format.

    Args:
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('0001-01-01T00:00:00').
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("0001-01-01T00:00:00"),
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Testresults Report

     Returns a csv report detailing all artefacts within a given date range. Together
    with their test executions and test results in csv format.

    Args:
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('0001-01-01T00:00:00').
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("0001-01-01T00:00:00"),
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Testresults Report

     Returns a csv report detailing all artefacts within a given date range. Together
    with their test executions and test results in csv format.

    Args:
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('0001-01-01T00:00:00').
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
