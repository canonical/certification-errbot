from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artefact_patch import ArtefactPatch
from ...models.artefact_response import ArtefactResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    artefact_id: int,
    *,
    body: ArtefactPatch,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/artefacts/{artefact_id}".format(
            artefact_id=artefact_id,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ArtefactResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ArtefactResponse.from_dict(response.json())

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
) -> Response[Union[ArtefactResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtefactPatch,
) -> Response[Union[ArtefactResponse, HTTPValidationError]]:
    """Patch Artefact

    Args:
        artefact_id (int):
        body (ArtefactPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtefactResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        artefact_id=artefact_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtefactPatch,
) -> Optional[Union[ArtefactResponse, HTTPValidationError]]:
    """Patch Artefact

    Args:
        artefact_id (int):
        body (ArtefactPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtefactResponse, HTTPValidationError]
    """

    return sync_detailed(
        artefact_id=artefact_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtefactPatch,
) -> Response[Union[ArtefactResponse, HTTPValidationError]]:
    """Patch Artefact

    Args:
        artefact_id (int):
        body (ArtefactPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ArtefactResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        artefact_id=artefact_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ArtefactPatch,
) -> Optional[Union[ArtefactResponse, HTTPValidationError]]:
    """Patch Artefact

    Args:
        artefact_id (int):
        body (ArtefactPatch):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ArtefactResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            artefact_id=artefact_id,
            client=client,
            body=body,
        )
    ).parsed
