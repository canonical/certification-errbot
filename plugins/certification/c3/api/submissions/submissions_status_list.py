from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_submission_list import PaginatedSubmissionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    failure_reason: Union[Unset, str] = UNSET,
    failure_reason_icontains: Union[Unset, str] = UNSET,
    failure_reason_iexact: Union[Unset, str] = UNSET,
    failure_reason_in: Union[Unset, list[str]] = UNSET,
    id: Union[Unset, int] = UNSET,
    id_in: Union[Unset, list[int]] = UNSET,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    processed_day: Union[Unset, float] = UNSET,
    processed_month: Union[Unset, float] = UNSET,
    processed_year: Union[Unset, float] = UNSET,
    report_id: Union[Unset, int] = UNSET,
    report_id_in: Union[Unset, list[int]] = UNSET,
    report_id_isnull: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    status_icontains: Union[Unset, str] = UNSET,
    status_iexact: Union[Unset, str] = UNSET,
    status_in: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["created_at__day"] = created_at_day

    params["created_at__month"] = created_at_month

    params["created_at__year"] = created_at_year

    params["failure_reason"] = failure_reason

    params["failure_reason__icontains"] = failure_reason_icontains

    params["failure_reason__iexact"] = failure_reason_iexact

    json_failure_reason_in: Union[Unset, list[str]] = UNSET
    if not isinstance(failure_reason_in, Unset):
        json_failure_reason_in = failure_reason_in

    params["failure_reason__in"] = json_failure_reason_in

    params["id"] = id

    json_id_in: Union[Unset, list[int]] = UNSET
    if not isinstance(id_in, Unset):
        json_id_in = id_in

    params["id__in"] = json_id_in

    params["limit"] = limit

    params["ordering"] = ordering

    params["page"] = page

    params["processed__day"] = processed_day

    params["processed__month"] = processed_month

    params["processed__year"] = processed_year

    params["report__id"] = report_id

    json_report_id_in: Union[Unset, list[int]] = UNSET
    if not isinstance(report_id_in, Unset):
        json_report_id_in = report_id_in

    params["report__id__in"] = json_report_id_in

    params["report__id__isnull"] = report_id_isnull

    params["status"] = status

    params["status__icontains"] = status_icontains

    params["status__iexact"] = status_iexact

    json_status_in: Union[Unset, list[str]] = UNSET
    if not isinstance(status_in, Unset):
        json_status_in = status_in

    params["status__in"] = json_status_in

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/submissions/status/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PaginatedSubmissionList]:
    if response.status_code == 200:
        response_200 = PaginatedSubmissionList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PaginatedSubmissionList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    failure_reason: Union[Unset, str] = UNSET,
    failure_reason_icontains: Union[Unset, str] = UNSET,
    failure_reason_iexact: Union[Unset, str] = UNSET,
    failure_reason_in: Union[Unset, list[str]] = UNSET,
    id: Union[Unset, int] = UNSET,
    id_in: Union[Unset, list[int]] = UNSET,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    processed_day: Union[Unset, float] = UNSET,
    processed_month: Union[Unset, float] = UNSET,
    processed_year: Union[Unset, float] = UNSET,
    report_id: Union[Unset, int] = UNSET,
    report_id_in: Union[Unset, list[int]] = UNSET,
    report_id_isnull: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    status_icontains: Union[Unset, str] = UNSET,
    status_iexact: Union[Unset, str] = UNSET,
    status_in: Union[Unset, list[str]] = UNSET,
) -> Response[PaginatedSubmissionList]:
    """
    Args:
        created_at_day (Union[Unset, float]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        failure_reason (Union[Unset, str]):
        failure_reason_icontains (Union[Unset, str]):
        failure_reason_iexact (Union[Unset, str]):
        failure_reason_in (Union[Unset, list[str]]):
        id (Union[Unset, int]):
        id_in (Union[Unset, list[int]]):
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):
        processed_day (Union[Unset, float]):
        processed_month (Union[Unset, float]):
        processed_year (Union[Unset, float]):
        report_id (Union[Unset, int]):
        report_id_in (Union[Unset, list[int]]):
        report_id_isnull (Union[Unset, bool]):
        status (Union[Unset, str]):
        status_icontains (Union[Unset, str]):
        status_iexact (Union[Unset, str]):
        status_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedSubmissionList]
    """

    kwargs = _get_kwargs(
        created_at_day=created_at_day,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        failure_reason=failure_reason,
        failure_reason_icontains=failure_reason_icontains,
        failure_reason_iexact=failure_reason_iexact,
        failure_reason_in=failure_reason_in,
        id=id,
        id_in=id_in,
        limit=limit,
        ordering=ordering,
        page=page,
        processed_day=processed_day,
        processed_month=processed_month,
        processed_year=processed_year,
        report_id=report_id,
        report_id_in=report_id_in,
        report_id_isnull=report_id_isnull,
        status=status,
        status_icontains=status_icontains,
        status_iexact=status_iexact,
        status_in=status_in,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    failure_reason: Union[Unset, str] = UNSET,
    failure_reason_icontains: Union[Unset, str] = UNSET,
    failure_reason_iexact: Union[Unset, str] = UNSET,
    failure_reason_in: Union[Unset, list[str]] = UNSET,
    id: Union[Unset, int] = UNSET,
    id_in: Union[Unset, list[int]] = UNSET,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    processed_day: Union[Unset, float] = UNSET,
    processed_month: Union[Unset, float] = UNSET,
    processed_year: Union[Unset, float] = UNSET,
    report_id: Union[Unset, int] = UNSET,
    report_id_in: Union[Unset, list[int]] = UNSET,
    report_id_isnull: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    status_icontains: Union[Unset, str] = UNSET,
    status_iexact: Union[Unset, str] = UNSET,
    status_in: Union[Unset, list[str]] = UNSET,
) -> Optional[PaginatedSubmissionList]:
    """
    Args:
        created_at_day (Union[Unset, float]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        failure_reason (Union[Unset, str]):
        failure_reason_icontains (Union[Unset, str]):
        failure_reason_iexact (Union[Unset, str]):
        failure_reason_in (Union[Unset, list[str]]):
        id (Union[Unset, int]):
        id_in (Union[Unset, list[int]]):
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):
        processed_day (Union[Unset, float]):
        processed_month (Union[Unset, float]):
        processed_year (Union[Unset, float]):
        report_id (Union[Unset, int]):
        report_id_in (Union[Unset, list[int]]):
        report_id_isnull (Union[Unset, bool]):
        status (Union[Unset, str]):
        status_icontains (Union[Unset, str]):
        status_iexact (Union[Unset, str]):
        status_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedSubmissionList
    """

    return sync_detailed(
        client=client,
        created_at_day=created_at_day,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        failure_reason=failure_reason,
        failure_reason_icontains=failure_reason_icontains,
        failure_reason_iexact=failure_reason_iexact,
        failure_reason_in=failure_reason_in,
        id=id,
        id_in=id_in,
        limit=limit,
        ordering=ordering,
        page=page,
        processed_day=processed_day,
        processed_month=processed_month,
        processed_year=processed_year,
        report_id=report_id,
        report_id_in=report_id_in,
        report_id_isnull=report_id_isnull,
        status=status,
        status_icontains=status_icontains,
        status_iexact=status_iexact,
        status_in=status_in,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    failure_reason: Union[Unset, str] = UNSET,
    failure_reason_icontains: Union[Unset, str] = UNSET,
    failure_reason_iexact: Union[Unset, str] = UNSET,
    failure_reason_in: Union[Unset, list[str]] = UNSET,
    id: Union[Unset, int] = UNSET,
    id_in: Union[Unset, list[int]] = UNSET,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    processed_day: Union[Unset, float] = UNSET,
    processed_month: Union[Unset, float] = UNSET,
    processed_year: Union[Unset, float] = UNSET,
    report_id: Union[Unset, int] = UNSET,
    report_id_in: Union[Unset, list[int]] = UNSET,
    report_id_isnull: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    status_icontains: Union[Unset, str] = UNSET,
    status_iexact: Union[Unset, str] = UNSET,
    status_in: Union[Unset, list[str]] = UNSET,
) -> Response[PaginatedSubmissionList]:
    """
    Args:
        created_at_day (Union[Unset, float]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        failure_reason (Union[Unset, str]):
        failure_reason_icontains (Union[Unset, str]):
        failure_reason_iexact (Union[Unset, str]):
        failure_reason_in (Union[Unset, list[str]]):
        id (Union[Unset, int]):
        id_in (Union[Unset, list[int]]):
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):
        processed_day (Union[Unset, float]):
        processed_month (Union[Unset, float]):
        processed_year (Union[Unset, float]):
        report_id (Union[Unset, int]):
        report_id_in (Union[Unset, list[int]]):
        report_id_isnull (Union[Unset, bool]):
        status (Union[Unset, str]):
        status_icontains (Union[Unset, str]):
        status_iexact (Union[Unset, str]):
        status_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedSubmissionList]
    """

    kwargs = _get_kwargs(
        created_at_day=created_at_day,
        created_at_month=created_at_month,
        created_at_year=created_at_year,
        failure_reason=failure_reason,
        failure_reason_icontains=failure_reason_icontains,
        failure_reason_iexact=failure_reason_iexact,
        failure_reason_in=failure_reason_in,
        id=id,
        id_in=id_in,
        limit=limit,
        ordering=ordering,
        page=page,
        processed_day=processed_day,
        processed_month=processed_month,
        processed_year=processed_year,
        report_id=report_id,
        report_id_in=report_id_in,
        report_id_isnull=report_id_isnull,
        status=status,
        status_icontains=status_icontains,
        status_iexact=status_iexact,
        status_in=status_in,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_at_day: Union[Unset, float] = UNSET,
    created_at_month: Union[Unset, float] = UNSET,
    created_at_year: Union[Unset, float] = UNSET,
    failure_reason: Union[Unset, str] = UNSET,
    failure_reason_icontains: Union[Unset, str] = UNSET,
    failure_reason_iexact: Union[Unset, str] = UNSET,
    failure_reason_in: Union[Unset, list[str]] = UNSET,
    id: Union[Unset, int] = UNSET,
    id_in: Union[Unset, list[int]] = UNSET,
    limit: Union[Unset, int] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    processed_day: Union[Unset, float] = UNSET,
    processed_month: Union[Unset, float] = UNSET,
    processed_year: Union[Unset, float] = UNSET,
    report_id: Union[Unset, int] = UNSET,
    report_id_in: Union[Unset, list[int]] = UNSET,
    report_id_isnull: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    status_icontains: Union[Unset, str] = UNSET,
    status_iexact: Union[Unset, str] = UNSET,
    status_in: Union[Unset, list[str]] = UNSET,
) -> Optional[PaginatedSubmissionList]:
    """
    Args:
        created_at_day (Union[Unset, float]):
        created_at_month (Union[Unset, float]):
        created_at_year (Union[Unset, float]):
        failure_reason (Union[Unset, str]):
        failure_reason_icontains (Union[Unset, str]):
        failure_reason_iexact (Union[Unset, str]):
        failure_reason_in (Union[Unset, list[str]]):
        id (Union[Unset, int]):
        id_in (Union[Unset, list[int]]):
        limit (Union[Unset, int]):
        ordering (Union[Unset, str]):
        page (Union[Unset, int]):
        processed_day (Union[Unset, float]):
        processed_month (Union[Unset, float]):
        processed_year (Union[Unset, float]):
        report_id (Union[Unset, int]):
        report_id_in (Union[Unset, list[int]]):
        report_id_isnull (Union[Unset, bool]):
        status (Union[Unset, str]):
        status_icontains (Union[Unset, str]):
        status_iexact (Union[Unset, str]):
        status_in (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedSubmissionList
    """

    return (
        await asyncio_detailed(
            client=client,
            created_at_day=created_at_day,
            created_at_month=created_at_month,
            created_at_year=created_at_year,
            failure_reason=failure_reason,
            failure_reason_icontains=failure_reason_icontains,
            failure_reason_iexact=failure_reason_iexact,
            failure_reason_in=failure_reason_in,
            id=id,
            id_in=id_in,
            limit=limit,
            ordering=ordering,
            page=page,
            processed_day=processed_day,
            processed_month=processed_month,
            processed_year=processed_year,
            report_id=report_id,
            report_id_in=report_id_in,
            report_id_isnull=report_id_isnull,
            status=status,
            status_icontains=status_icontains,
            status_iexact=status_iexact,
            status_in=status_in,
        )
    ).parsed
