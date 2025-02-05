from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.machine_report import MachineReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    arch: Union[Unset, str] = UNSET,
    audio_name: Union[Unset, str] = UNSET,
    audio_vendor: Union[Unset, str] = UNSET,
    board_name: Union[Unset, str] = UNSET,
    board_vendor: Union[Unset, str] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cert_level: Union[Unset, str] = UNSET,
    cert_status: Union[Unset, str] = UNSET,
    completed: Union[Unset, str] = UNSET,
    cpu_codename: Union[Unset, str] = UNSET,
    cpu_id: Union[Unset, str] = UNSET,
    cpu_model: Union[Unset, str] = UNSET,
    deb_package: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    enablement_status: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached_to_platform: Union[Unset, str] = UNSET,
    gpu_name: Union[Unset, str] = UNSET,
    gpu_vendor: Union[Unset, str] = UNSET,
    has_child: Union[Unset, str] = UNSET,
    has_child_with_platform: Union[Unset, str] = UNSET,
    has_expansion_card_slots: Union[Unset, str] = UNSET,
    has_expansion_card_slots_type: Union[Unset, str] = UNSET,
    has_expansion_card_slots_width: Union[Unset, str] = UNSET,
    has_parent: Union[Unset, str] = UNSET,
    has_parent_with_platform: Union[Unset, str] = UNSET,
    in_testflinger: Union[Unset, str] = UNSET,
    kernel_version: Union[Unset, str] = UNSET,
    labresource_ip: Union[Unset, str] = UNSET,
    launchpad_tag: Union[Unset, str] = UNSET,
    level: Union[Unset, str] = UNSET,
    loaded_kernel_module: Union[Unset, str] = UNSET,
    location: Union[Unset, str] = UNSET,
    maas_node_id: Union[Unset, str] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    make: Union[Unset, str] = UNSET,
    memory_gte: Union[Unset, int] = UNSET,
    memory_lte: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_vendor: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    requested_provision_type: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    snap_package: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    test_case: Union[Unset, str] = UNSET,
    test_status: Union[Unset, str] = UNSET,
    testflinger_approved: Union[Unset, str] = UNSET,
    tf_provision_type: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    wireless_name: Union[Unset, str] = UNSET,
    wireless_vendor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arch"] = arch

    params["audio_name"] = audio_name

    params["audio_vendor"] = audio_vendor

    params["board_name"] = board_name

    params["board_vendor"] = board_vendor

    params["canonical_id"] = canonical_id

    params["category"] = category

    params["cert_level"] = cert_level

    params["cert_status"] = cert_status

    params["completed"] = completed

    params["cpu_codename"] = cpu_codename

    params["cpu_id"] = cpu_id

    params["cpu_model"] = cpu_model

    params["deb_package"] = deb_package

    params["device_id"] = device_id

    params["enablement_status"] = enablement_status

    params["expansion_card_slot_is_attached"] = expansion_card_slot_is_attached

    params["expansion_card_slot_is_attached_to_platform"] = (
        expansion_card_slot_is_attached_to_platform
    )

    params["gpu_name"] = gpu_name

    params["gpu_vendor"] = gpu_vendor

    params["has_child"] = has_child

    params["has_child_with_platform"] = has_child_with_platform

    params["has_expansion_card_slots"] = has_expansion_card_slots

    params["has_expansion_card_slots_type"] = has_expansion_card_slots_type

    params["has_expansion_card_slots_width"] = has_expansion_card_slots_width

    params["has_parent"] = has_parent

    params["has_parent_with_platform"] = has_parent_with_platform

    params["in_testflinger"] = in_testflinger

    params["kernel_version"] = kernel_version

    params["labresource_ip"] = labresource_ip

    params["launchpad_tag"] = launchpad_tag

    params["level"] = level

    params["loaded_kernel_module"] = loaded_kernel_module

    params["location"] = location

    params["maas_node_id"] = maas_node_id

    params["mac_address"] = mac_address

    params["make"] = make

    params["memory_gte"] = memory_gte

    params["memory_lte"] = memory_lte

    params["model"] = model

    params["network_name"] = network_name

    params["network_vendor"] = network_vendor

    params["ordering"] = ordering

    params["project"] = project

    params["project_id"] = project_id

    params["release"] = release

    params["requested_provision_type"] = requested_provision_type

    params["serial_number"] = serial_number

    params["snap_package"] = snap_package

    params["status"] = status

    params["test_case"] = test_case

    params["test_status"] = test_status

    params["testflinger_approved"] = testflinger_approved

    params["tf_provision_type"] = tf_provision_type

    params["vendor"] = vendor

    params["wireless_name"] = wireless_name

    params["wireless_vendor"] = wireless_vendor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/machinereports/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["MachineReport"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_paginated_machine_report_list_item_data in _response_200:
            componentsschemas_paginated_machine_report_list_item = (
                MachineReport.from_dict(
                    componentsschemas_paginated_machine_report_list_item_data
                )
            )

            response_200.append(componentsschemas_paginated_machine_report_list_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MachineReport"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    arch: Union[Unset, str] = UNSET,
    audio_name: Union[Unset, str] = UNSET,
    audio_vendor: Union[Unset, str] = UNSET,
    board_name: Union[Unset, str] = UNSET,
    board_vendor: Union[Unset, str] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cert_level: Union[Unset, str] = UNSET,
    cert_status: Union[Unset, str] = UNSET,
    completed: Union[Unset, str] = UNSET,
    cpu_codename: Union[Unset, str] = UNSET,
    cpu_id: Union[Unset, str] = UNSET,
    cpu_model: Union[Unset, str] = UNSET,
    deb_package: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    enablement_status: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached_to_platform: Union[Unset, str] = UNSET,
    gpu_name: Union[Unset, str] = UNSET,
    gpu_vendor: Union[Unset, str] = UNSET,
    has_child: Union[Unset, str] = UNSET,
    has_child_with_platform: Union[Unset, str] = UNSET,
    has_expansion_card_slots: Union[Unset, str] = UNSET,
    has_expansion_card_slots_type: Union[Unset, str] = UNSET,
    has_expansion_card_slots_width: Union[Unset, str] = UNSET,
    has_parent: Union[Unset, str] = UNSET,
    has_parent_with_platform: Union[Unset, str] = UNSET,
    in_testflinger: Union[Unset, str] = UNSET,
    kernel_version: Union[Unset, str] = UNSET,
    labresource_ip: Union[Unset, str] = UNSET,
    launchpad_tag: Union[Unset, str] = UNSET,
    level: Union[Unset, str] = UNSET,
    loaded_kernel_module: Union[Unset, str] = UNSET,
    location: Union[Unset, str] = UNSET,
    maas_node_id: Union[Unset, str] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    make: Union[Unset, str] = UNSET,
    memory_gte: Union[Unset, int] = UNSET,
    memory_lte: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_vendor: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    requested_provision_type: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    snap_package: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    test_case: Union[Unset, str] = UNSET,
    test_status: Union[Unset, str] = UNSET,
    testflinger_approved: Union[Unset, str] = UNSET,
    tf_provision_type: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    wireless_name: Union[Unset, str] = UNSET,
    wireless_vendor: Union[Unset, str] = UNSET,
) -> Response[list["MachineReport"]]:
    """Base class that contains multiple fields and methods used by
    different API endpoints for Machine Reports

    Args:
        arch (Union[Unset, str]):
        audio_name (Union[Unset, str]):
        audio_vendor (Union[Unset, str]):
        board_name (Union[Unset, str]):
        board_vendor (Union[Unset, str]):
        canonical_id (Union[Unset, str]):
        category (Union[Unset, str]):
        cert_level (Union[Unset, str]):
        cert_status (Union[Unset, str]):
        completed (Union[Unset, str]):
        cpu_codename (Union[Unset, str]):
        cpu_id (Union[Unset, str]):
        cpu_model (Union[Unset, str]):
        deb_package (Union[Unset, str]):
        device_id (Union[Unset, str]):
        enablement_status (Union[Unset, str]):
        expansion_card_slot_is_attached (Union[Unset, str]):
        expansion_card_slot_is_attached_to_platform (Union[Unset, str]):
        gpu_name (Union[Unset, str]):
        gpu_vendor (Union[Unset, str]):
        has_child (Union[Unset, str]):
        has_child_with_platform (Union[Unset, str]):
        has_expansion_card_slots (Union[Unset, str]):
        has_expansion_card_slots_type (Union[Unset, str]):
        has_expansion_card_slots_width (Union[Unset, str]):
        has_parent (Union[Unset, str]):
        has_parent_with_platform (Union[Unset, str]):
        in_testflinger (Union[Unset, str]):
        kernel_version (Union[Unset, str]):
        labresource_ip (Union[Unset, str]):
        launchpad_tag (Union[Unset, str]):
        level (Union[Unset, str]):
        loaded_kernel_module (Union[Unset, str]):
        location (Union[Unset, str]):
        maas_node_id (Union[Unset, str]):
        mac_address (Union[Unset, str]):
        make (Union[Unset, str]):
        memory_gte (Union[Unset, int]):
        memory_lte (Union[Unset, int]):
        model (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_vendor (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, str]):
        project_id (Union[Unset, str]):
        release (Union[Unset, str]):
        requested_provision_type (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        snap_package (Union[Unset, str]):
        status (Union[Unset, str]):
        test_case (Union[Unset, str]):
        test_status (Union[Unset, str]):
        testflinger_approved (Union[Unset, str]):
        tf_provision_type (Union[Unset, str]):
        vendor (Union[Unset, str]):
        wireless_name (Union[Unset, str]):
        wireless_vendor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MachineReport']]
    """

    kwargs = _get_kwargs(
        arch=arch,
        audio_name=audio_name,
        audio_vendor=audio_vendor,
        board_name=board_name,
        board_vendor=board_vendor,
        canonical_id=canonical_id,
        category=category,
        cert_level=cert_level,
        cert_status=cert_status,
        completed=completed,
        cpu_codename=cpu_codename,
        cpu_id=cpu_id,
        cpu_model=cpu_model,
        deb_package=deb_package,
        device_id=device_id,
        enablement_status=enablement_status,
        expansion_card_slot_is_attached=expansion_card_slot_is_attached,
        expansion_card_slot_is_attached_to_platform=expansion_card_slot_is_attached_to_platform,
        gpu_name=gpu_name,
        gpu_vendor=gpu_vendor,
        has_child=has_child,
        has_child_with_platform=has_child_with_platform,
        has_expansion_card_slots=has_expansion_card_slots,
        has_expansion_card_slots_type=has_expansion_card_slots_type,
        has_expansion_card_slots_width=has_expansion_card_slots_width,
        has_parent=has_parent,
        has_parent_with_platform=has_parent_with_platform,
        in_testflinger=in_testflinger,
        kernel_version=kernel_version,
        labresource_ip=labresource_ip,
        launchpad_tag=launchpad_tag,
        level=level,
        loaded_kernel_module=loaded_kernel_module,
        location=location,
        maas_node_id=maas_node_id,
        mac_address=mac_address,
        make=make,
        memory_gte=memory_gte,
        memory_lte=memory_lte,
        model=model,
        network_name=network_name,
        network_vendor=network_vendor,
        ordering=ordering,
        project=project,
        project_id=project_id,
        release=release,
        requested_provision_type=requested_provision_type,
        serial_number=serial_number,
        snap_package=snap_package,
        status=status,
        test_case=test_case,
        test_status=test_status,
        testflinger_approved=testflinger_approved,
        tf_provision_type=tf_provision_type,
        vendor=vendor,
        wireless_name=wireless_name,
        wireless_vendor=wireless_vendor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arch: Union[Unset, str] = UNSET,
    audio_name: Union[Unset, str] = UNSET,
    audio_vendor: Union[Unset, str] = UNSET,
    board_name: Union[Unset, str] = UNSET,
    board_vendor: Union[Unset, str] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cert_level: Union[Unset, str] = UNSET,
    cert_status: Union[Unset, str] = UNSET,
    completed: Union[Unset, str] = UNSET,
    cpu_codename: Union[Unset, str] = UNSET,
    cpu_id: Union[Unset, str] = UNSET,
    cpu_model: Union[Unset, str] = UNSET,
    deb_package: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    enablement_status: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached_to_platform: Union[Unset, str] = UNSET,
    gpu_name: Union[Unset, str] = UNSET,
    gpu_vendor: Union[Unset, str] = UNSET,
    has_child: Union[Unset, str] = UNSET,
    has_child_with_platform: Union[Unset, str] = UNSET,
    has_expansion_card_slots: Union[Unset, str] = UNSET,
    has_expansion_card_slots_type: Union[Unset, str] = UNSET,
    has_expansion_card_slots_width: Union[Unset, str] = UNSET,
    has_parent: Union[Unset, str] = UNSET,
    has_parent_with_platform: Union[Unset, str] = UNSET,
    in_testflinger: Union[Unset, str] = UNSET,
    kernel_version: Union[Unset, str] = UNSET,
    labresource_ip: Union[Unset, str] = UNSET,
    launchpad_tag: Union[Unset, str] = UNSET,
    level: Union[Unset, str] = UNSET,
    loaded_kernel_module: Union[Unset, str] = UNSET,
    location: Union[Unset, str] = UNSET,
    maas_node_id: Union[Unset, str] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    make: Union[Unset, str] = UNSET,
    memory_gte: Union[Unset, int] = UNSET,
    memory_lte: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_vendor: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    requested_provision_type: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    snap_package: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    test_case: Union[Unset, str] = UNSET,
    test_status: Union[Unset, str] = UNSET,
    testflinger_approved: Union[Unset, str] = UNSET,
    tf_provision_type: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    wireless_name: Union[Unset, str] = UNSET,
    wireless_vendor: Union[Unset, str] = UNSET,
) -> Optional[list["MachineReport"]]:
    """Base class that contains multiple fields and methods used by
    different API endpoints for Machine Reports

    Args:
        arch (Union[Unset, str]):
        audio_name (Union[Unset, str]):
        audio_vendor (Union[Unset, str]):
        board_name (Union[Unset, str]):
        board_vendor (Union[Unset, str]):
        canonical_id (Union[Unset, str]):
        category (Union[Unset, str]):
        cert_level (Union[Unset, str]):
        cert_status (Union[Unset, str]):
        completed (Union[Unset, str]):
        cpu_codename (Union[Unset, str]):
        cpu_id (Union[Unset, str]):
        cpu_model (Union[Unset, str]):
        deb_package (Union[Unset, str]):
        device_id (Union[Unset, str]):
        enablement_status (Union[Unset, str]):
        expansion_card_slot_is_attached (Union[Unset, str]):
        expansion_card_slot_is_attached_to_platform (Union[Unset, str]):
        gpu_name (Union[Unset, str]):
        gpu_vendor (Union[Unset, str]):
        has_child (Union[Unset, str]):
        has_child_with_platform (Union[Unset, str]):
        has_expansion_card_slots (Union[Unset, str]):
        has_expansion_card_slots_type (Union[Unset, str]):
        has_expansion_card_slots_width (Union[Unset, str]):
        has_parent (Union[Unset, str]):
        has_parent_with_platform (Union[Unset, str]):
        in_testflinger (Union[Unset, str]):
        kernel_version (Union[Unset, str]):
        labresource_ip (Union[Unset, str]):
        launchpad_tag (Union[Unset, str]):
        level (Union[Unset, str]):
        loaded_kernel_module (Union[Unset, str]):
        location (Union[Unset, str]):
        maas_node_id (Union[Unset, str]):
        mac_address (Union[Unset, str]):
        make (Union[Unset, str]):
        memory_gte (Union[Unset, int]):
        memory_lte (Union[Unset, int]):
        model (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_vendor (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, str]):
        project_id (Union[Unset, str]):
        release (Union[Unset, str]):
        requested_provision_type (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        snap_package (Union[Unset, str]):
        status (Union[Unset, str]):
        test_case (Union[Unset, str]):
        test_status (Union[Unset, str]):
        testflinger_approved (Union[Unset, str]):
        tf_provision_type (Union[Unset, str]):
        vendor (Union[Unset, str]):
        wireless_name (Union[Unset, str]):
        wireless_vendor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MachineReport']
    """

    return sync_detailed(
        client=client,
        arch=arch,
        audio_name=audio_name,
        audio_vendor=audio_vendor,
        board_name=board_name,
        board_vendor=board_vendor,
        canonical_id=canonical_id,
        category=category,
        cert_level=cert_level,
        cert_status=cert_status,
        completed=completed,
        cpu_codename=cpu_codename,
        cpu_id=cpu_id,
        cpu_model=cpu_model,
        deb_package=deb_package,
        device_id=device_id,
        enablement_status=enablement_status,
        expansion_card_slot_is_attached=expansion_card_slot_is_attached,
        expansion_card_slot_is_attached_to_platform=expansion_card_slot_is_attached_to_platform,
        gpu_name=gpu_name,
        gpu_vendor=gpu_vendor,
        has_child=has_child,
        has_child_with_platform=has_child_with_platform,
        has_expansion_card_slots=has_expansion_card_slots,
        has_expansion_card_slots_type=has_expansion_card_slots_type,
        has_expansion_card_slots_width=has_expansion_card_slots_width,
        has_parent=has_parent,
        has_parent_with_platform=has_parent_with_platform,
        in_testflinger=in_testflinger,
        kernel_version=kernel_version,
        labresource_ip=labresource_ip,
        launchpad_tag=launchpad_tag,
        level=level,
        loaded_kernel_module=loaded_kernel_module,
        location=location,
        maas_node_id=maas_node_id,
        mac_address=mac_address,
        make=make,
        memory_gte=memory_gte,
        memory_lte=memory_lte,
        model=model,
        network_name=network_name,
        network_vendor=network_vendor,
        ordering=ordering,
        project=project,
        project_id=project_id,
        release=release,
        requested_provision_type=requested_provision_type,
        serial_number=serial_number,
        snap_package=snap_package,
        status=status,
        test_case=test_case,
        test_status=test_status,
        testflinger_approved=testflinger_approved,
        tf_provision_type=tf_provision_type,
        vendor=vendor,
        wireless_name=wireless_name,
        wireless_vendor=wireless_vendor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arch: Union[Unset, str] = UNSET,
    audio_name: Union[Unset, str] = UNSET,
    audio_vendor: Union[Unset, str] = UNSET,
    board_name: Union[Unset, str] = UNSET,
    board_vendor: Union[Unset, str] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cert_level: Union[Unset, str] = UNSET,
    cert_status: Union[Unset, str] = UNSET,
    completed: Union[Unset, str] = UNSET,
    cpu_codename: Union[Unset, str] = UNSET,
    cpu_id: Union[Unset, str] = UNSET,
    cpu_model: Union[Unset, str] = UNSET,
    deb_package: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    enablement_status: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached_to_platform: Union[Unset, str] = UNSET,
    gpu_name: Union[Unset, str] = UNSET,
    gpu_vendor: Union[Unset, str] = UNSET,
    has_child: Union[Unset, str] = UNSET,
    has_child_with_platform: Union[Unset, str] = UNSET,
    has_expansion_card_slots: Union[Unset, str] = UNSET,
    has_expansion_card_slots_type: Union[Unset, str] = UNSET,
    has_expansion_card_slots_width: Union[Unset, str] = UNSET,
    has_parent: Union[Unset, str] = UNSET,
    has_parent_with_platform: Union[Unset, str] = UNSET,
    in_testflinger: Union[Unset, str] = UNSET,
    kernel_version: Union[Unset, str] = UNSET,
    labresource_ip: Union[Unset, str] = UNSET,
    launchpad_tag: Union[Unset, str] = UNSET,
    level: Union[Unset, str] = UNSET,
    loaded_kernel_module: Union[Unset, str] = UNSET,
    location: Union[Unset, str] = UNSET,
    maas_node_id: Union[Unset, str] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    make: Union[Unset, str] = UNSET,
    memory_gte: Union[Unset, int] = UNSET,
    memory_lte: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_vendor: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    requested_provision_type: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    snap_package: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    test_case: Union[Unset, str] = UNSET,
    test_status: Union[Unset, str] = UNSET,
    testflinger_approved: Union[Unset, str] = UNSET,
    tf_provision_type: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    wireless_name: Union[Unset, str] = UNSET,
    wireless_vendor: Union[Unset, str] = UNSET,
) -> Response[list["MachineReport"]]:
    """Base class that contains multiple fields and methods used by
    different API endpoints for Machine Reports

    Args:
        arch (Union[Unset, str]):
        audio_name (Union[Unset, str]):
        audio_vendor (Union[Unset, str]):
        board_name (Union[Unset, str]):
        board_vendor (Union[Unset, str]):
        canonical_id (Union[Unset, str]):
        category (Union[Unset, str]):
        cert_level (Union[Unset, str]):
        cert_status (Union[Unset, str]):
        completed (Union[Unset, str]):
        cpu_codename (Union[Unset, str]):
        cpu_id (Union[Unset, str]):
        cpu_model (Union[Unset, str]):
        deb_package (Union[Unset, str]):
        device_id (Union[Unset, str]):
        enablement_status (Union[Unset, str]):
        expansion_card_slot_is_attached (Union[Unset, str]):
        expansion_card_slot_is_attached_to_platform (Union[Unset, str]):
        gpu_name (Union[Unset, str]):
        gpu_vendor (Union[Unset, str]):
        has_child (Union[Unset, str]):
        has_child_with_platform (Union[Unset, str]):
        has_expansion_card_slots (Union[Unset, str]):
        has_expansion_card_slots_type (Union[Unset, str]):
        has_expansion_card_slots_width (Union[Unset, str]):
        has_parent (Union[Unset, str]):
        has_parent_with_platform (Union[Unset, str]):
        in_testflinger (Union[Unset, str]):
        kernel_version (Union[Unset, str]):
        labresource_ip (Union[Unset, str]):
        launchpad_tag (Union[Unset, str]):
        level (Union[Unset, str]):
        loaded_kernel_module (Union[Unset, str]):
        location (Union[Unset, str]):
        maas_node_id (Union[Unset, str]):
        mac_address (Union[Unset, str]):
        make (Union[Unset, str]):
        memory_gte (Union[Unset, int]):
        memory_lte (Union[Unset, int]):
        model (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_vendor (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, str]):
        project_id (Union[Unset, str]):
        release (Union[Unset, str]):
        requested_provision_type (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        snap_package (Union[Unset, str]):
        status (Union[Unset, str]):
        test_case (Union[Unset, str]):
        test_status (Union[Unset, str]):
        testflinger_approved (Union[Unset, str]):
        tf_provision_type (Union[Unset, str]):
        vendor (Union[Unset, str]):
        wireless_name (Union[Unset, str]):
        wireless_vendor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MachineReport']]
    """

    kwargs = _get_kwargs(
        arch=arch,
        audio_name=audio_name,
        audio_vendor=audio_vendor,
        board_name=board_name,
        board_vendor=board_vendor,
        canonical_id=canonical_id,
        category=category,
        cert_level=cert_level,
        cert_status=cert_status,
        completed=completed,
        cpu_codename=cpu_codename,
        cpu_id=cpu_id,
        cpu_model=cpu_model,
        deb_package=deb_package,
        device_id=device_id,
        enablement_status=enablement_status,
        expansion_card_slot_is_attached=expansion_card_slot_is_attached,
        expansion_card_slot_is_attached_to_platform=expansion_card_slot_is_attached_to_platform,
        gpu_name=gpu_name,
        gpu_vendor=gpu_vendor,
        has_child=has_child,
        has_child_with_platform=has_child_with_platform,
        has_expansion_card_slots=has_expansion_card_slots,
        has_expansion_card_slots_type=has_expansion_card_slots_type,
        has_expansion_card_slots_width=has_expansion_card_slots_width,
        has_parent=has_parent,
        has_parent_with_platform=has_parent_with_platform,
        in_testflinger=in_testflinger,
        kernel_version=kernel_version,
        labresource_ip=labresource_ip,
        launchpad_tag=launchpad_tag,
        level=level,
        loaded_kernel_module=loaded_kernel_module,
        location=location,
        maas_node_id=maas_node_id,
        mac_address=mac_address,
        make=make,
        memory_gte=memory_gte,
        memory_lte=memory_lte,
        model=model,
        network_name=network_name,
        network_vendor=network_vendor,
        ordering=ordering,
        project=project,
        project_id=project_id,
        release=release,
        requested_provision_type=requested_provision_type,
        serial_number=serial_number,
        snap_package=snap_package,
        status=status,
        test_case=test_case,
        test_status=test_status,
        testflinger_approved=testflinger_approved,
        tf_provision_type=tf_provision_type,
        vendor=vendor,
        wireless_name=wireless_name,
        wireless_vendor=wireless_vendor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arch: Union[Unset, str] = UNSET,
    audio_name: Union[Unset, str] = UNSET,
    audio_vendor: Union[Unset, str] = UNSET,
    board_name: Union[Unset, str] = UNSET,
    board_vendor: Union[Unset, str] = UNSET,
    canonical_id: Union[Unset, str] = UNSET,
    category: Union[Unset, str] = UNSET,
    cert_level: Union[Unset, str] = UNSET,
    cert_status: Union[Unset, str] = UNSET,
    completed: Union[Unset, str] = UNSET,
    cpu_codename: Union[Unset, str] = UNSET,
    cpu_id: Union[Unset, str] = UNSET,
    cpu_model: Union[Unset, str] = UNSET,
    deb_package: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    enablement_status: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached: Union[Unset, str] = UNSET,
    expansion_card_slot_is_attached_to_platform: Union[Unset, str] = UNSET,
    gpu_name: Union[Unset, str] = UNSET,
    gpu_vendor: Union[Unset, str] = UNSET,
    has_child: Union[Unset, str] = UNSET,
    has_child_with_platform: Union[Unset, str] = UNSET,
    has_expansion_card_slots: Union[Unset, str] = UNSET,
    has_expansion_card_slots_type: Union[Unset, str] = UNSET,
    has_expansion_card_slots_width: Union[Unset, str] = UNSET,
    has_parent: Union[Unset, str] = UNSET,
    has_parent_with_platform: Union[Unset, str] = UNSET,
    in_testflinger: Union[Unset, str] = UNSET,
    kernel_version: Union[Unset, str] = UNSET,
    labresource_ip: Union[Unset, str] = UNSET,
    launchpad_tag: Union[Unset, str] = UNSET,
    level: Union[Unset, str] = UNSET,
    loaded_kernel_module: Union[Unset, str] = UNSET,
    location: Union[Unset, str] = UNSET,
    maas_node_id: Union[Unset, str] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    make: Union[Unset, str] = UNSET,
    memory_gte: Union[Unset, int] = UNSET,
    memory_lte: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_vendor: Union[Unset, str] = UNSET,
    ordering: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    release: Union[Unset, str] = UNSET,
    requested_provision_type: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    snap_package: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    test_case: Union[Unset, str] = UNSET,
    test_status: Union[Unset, str] = UNSET,
    testflinger_approved: Union[Unset, str] = UNSET,
    tf_provision_type: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    wireless_name: Union[Unset, str] = UNSET,
    wireless_vendor: Union[Unset, str] = UNSET,
) -> Optional[list["MachineReport"]]:
    """Base class that contains multiple fields and methods used by
    different API endpoints for Machine Reports

    Args:
        arch (Union[Unset, str]):
        audio_name (Union[Unset, str]):
        audio_vendor (Union[Unset, str]):
        board_name (Union[Unset, str]):
        board_vendor (Union[Unset, str]):
        canonical_id (Union[Unset, str]):
        category (Union[Unset, str]):
        cert_level (Union[Unset, str]):
        cert_status (Union[Unset, str]):
        completed (Union[Unset, str]):
        cpu_codename (Union[Unset, str]):
        cpu_id (Union[Unset, str]):
        cpu_model (Union[Unset, str]):
        deb_package (Union[Unset, str]):
        device_id (Union[Unset, str]):
        enablement_status (Union[Unset, str]):
        expansion_card_slot_is_attached (Union[Unset, str]):
        expansion_card_slot_is_attached_to_platform (Union[Unset, str]):
        gpu_name (Union[Unset, str]):
        gpu_vendor (Union[Unset, str]):
        has_child (Union[Unset, str]):
        has_child_with_platform (Union[Unset, str]):
        has_expansion_card_slots (Union[Unset, str]):
        has_expansion_card_slots_type (Union[Unset, str]):
        has_expansion_card_slots_width (Union[Unset, str]):
        has_parent (Union[Unset, str]):
        has_parent_with_platform (Union[Unset, str]):
        in_testflinger (Union[Unset, str]):
        kernel_version (Union[Unset, str]):
        labresource_ip (Union[Unset, str]):
        launchpad_tag (Union[Unset, str]):
        level (Union[Unset, str]):
        loaded_kernel_module (Union[Unset, str]):
        location (Union[Unset, str]):
        maas_node_id (Union[Unset, str]):
        mac_address (Union[Unset, str]):
        make (Union[Unset, str]):
        memory_gte (Union[Unset, int]):
        memory_lte (Union[Unset, int]):
        model (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_vendor (Union[Unset, str]):
        ordering (Union[Unset, str]):
        project (Union[Unset, str]):
        project_id (Union[Unset, str]):
        release (Union[Unset, str]):
        requested_provision_type (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        snap_package (Union[Unset, str]):
        status (Union[Unset, str]):
        test_case (Union[Unset, str]):
        test_status (Union[Unset, str]):
        testflinger_approved (Union[Unset, str]):
        tf_provision_type (Union[Unset, str]):
        vendor (Union[Unset, str]):
        wireless_name (Union[Unset, str]):
        wireless_vendor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MachineReport']
    """

    return (
        await asyncio_detailed(
            client=client,
            arch=arch,
            audio_name=audio_name,
            audio_vendor=audio_vendor,
            board_name=board_name,
            board_vendor=board_vendor,
            canonical_id=canonical_id,
            category=category,
            cert_level=cert_level,
            cert_status=cert_status,
            completed=completed,
            cpu_codename=cpu_codename,
            cpu_id=cpu_id,
            cpu_model=cpu_model,
            deb_package=deb_package,
            device_id=device_id,
            enablement_status=enablement_status,
            expansion_card_slot_is_attached=expansion_card_slot_is_attached,
            expansion_card_slot_is_attached_to_platform=expansion_card_slot_is_attached_to_platform,
            gpu_name=gpu_name,
            gpu_vendor=gpu_vendor,
            has_child=has_child,
            has_child_with_platform=has_child_with_platform,
            has_expansion_card_slots=has_expansion_card_slots,
            has_expansion_card_slots_type=has_expansion_card_slots_type,
            has_expansion_card_slots_width=has_expansion_card_slots_width,
            has_parent=has_parent,
            has_parent_with_platform=has_parent_with_platform,
            in_testflinger=in_testflinger,
            kernel_version=kernel_version,
            labresource_ip=labresource_ip,
            launchpad_tag=launchpad_tag,
            level=level,
            loaded_kernel_module=loaded_kernel_module,
            location=location,
            maas_node_id=maas_node_id,
            mac_address=mac_address,
            make=make,
            memory_gte=memory_gte,
            memory_lte=memory_lte,
            model=model,
            network_name=network_name,
            network_vendor=network_vendor,
            ordering=ordering,
            project=project,
            project_id=project_id,
            release=release,
            requested_provision_type=requested_provision_type,
            serial_number=serial_number,
            snap_package=snap_package,
            status=status,
            test_case=test_case,
            test_status=test_status,
            testflinger_approved=testflinger_approved,
            tf_provision_type=tf_provision_type,
            vendor=vendor,
            wireless_name=wireless_name,
            wireless_vendor=wireless_vendor,
        )
    ).parsed
