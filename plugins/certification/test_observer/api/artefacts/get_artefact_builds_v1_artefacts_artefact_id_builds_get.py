from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artefact_build_response import ArtefactBuildResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    artefact_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/artefacts/{artefact_id}/builds".format(
            artefact_id=artefact_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArtefactBuildResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
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
) -> Response[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
    """Get Artefact Builds

     Get latest artefact builds of an artefact together with their test executions

    Args:
        artefact_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ArtefactBuildResponse']]]
    """

    kwargs = _get_kwargs(
        artefact_id=artefact_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
    """Get Artefact Builds

     Get latest artefact builds of an artefact together with their test executions

    Args:
        artefact_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ArtefactBuildResponse']]
    """

    return sync_detailed(
        artefact_id=artefact_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
    """Get Artefact Builds

     Get latest artefact builds of an artefact together with their test executions

    Args:
        artefact_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ArtefactBuildResponse']]]
    """

    kwargs = _get_kwargs(
        artefact_id=artefact_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artefact_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, list["ArtefactBuildResponse"]]]:
    """Get Artefact Builds

     Get latest artefact builds of an artefact together with their test executions

    Args:
        artefact_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ArtefactBuildResponse']]
    """

    return (
        await asyncio_detailed(
            artefact_id=artefact_id,
            client=client,
        )
    ).parsed
