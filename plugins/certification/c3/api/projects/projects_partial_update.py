from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_write_project import PatchedWriteProject
from ...models.write_project import WriteProject
from ...types import Response


def _get_kwargs(
    project_id: int,
    *,
    body: Union[
        PatchedWriteProject,
        PatchedWriteProject,
        PatchedWriteProject,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v2/projects/{project_id}/".format(
            project_id=project_id,
        ),
    }

    if isinstance(body, PatchedWriteProject):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedWriteProject):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedWriteProject):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[WriteProject]:
    if response.status_code == 200:
        response_200 = WriteProject.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WriteProject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWriteProject,
        PatchedWriteProject,
        PatchedWriteProject,
    ],
) -> Response[WriteProject]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        project_id (int):
        body (PatchedWriteProject):
        body (PatchedWriteProject):
        body (PatchedWriteProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WriteProject]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWriteProject,
        PatchedWriteProject,
        PatchedWriteProject,
    ],
) -> Optional[WriteProject]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        project_id (int):
        body (PatchedWriteProject):
        body (PatchedWriteProject):
        body (PatchedWriteProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WriteProject
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWriteProject,
        PatchedWriteProject,
        PatchedWriteProject,
    ],
) -> Response[WriteProject]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        project_id (int):
        body (PatchedWriteProject):
        body (PatchedWriteProject):
        body (PatchedWriteProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WriteProject]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWriteProject,
        PatchedWriteProject,
        PatchedWriteProject,
    ],
) -> Optional[WriteProject]:
    """Stricted variation of the custom permission mixin to check whether
    a user or an application is authenticated to access the data
    behind the API call.

    Args:
        project_id (int):
        body (PatchedWriteProject):
        body (PatchedWriteProject):
        body (PatchedWriteProject):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WriteProject
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
