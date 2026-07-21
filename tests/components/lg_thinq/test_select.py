"""Tests for the LG ThinQ select platform."""

from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.components.select import (
    ATTR_OPTION,
    ATTR_OPTIONS,
    DOMAIN as SELECT_DOMAIN,
    SERVICE_SELECT_OPTION,
)
from homeassistant.const import ATTR_ENTITY_ID, STATE_UNKNOWN, Platform
from homeassistant.core import HomeAssistant

from . import setup_integration

from tests.common import MockConfigEntry

OPERATION_ENTITY_ID = "select.test_washtower_dryer_operation"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize("device_fixture", ["washtower_dryer"])
async def test_washtower_dryer_operation_select(
    hass: HomeAssistant,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that a WashTower dryer gets an operation select entity.

    The WashTower dryer profile exposes a writable dryerOperationMode,
    so an operation select must be created for it.
    """
    with patch("homeassistant.components.lg_thinq.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)

    state = hass.states.get(OPERATION_ENTITY_ID)
    assert state is not None
    assert state.state == STATE_UNKNOWN
    assert state.attributes[ATTR_OPTIONS] == [
        "start",
        "stop",
        "power_off",
        "power_on",
    ]


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize("device_fixture", ["washtower_dryer"])
async def test_washtower_dryer_operation_select_start(
    hass: HomeAssistant,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that selecting start posts dryerOperationMode START."""
    with patch("homeassistant.components.lg_thinq.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SERVICE_SELECT_OPTION,
        {ATTR_ENTITY_ID: OPERATION_ENTITY_ID, ATTR_OPTION: "start"},
        blocking=True,
    )

    devices.async_post_device_control.assert_called_once_with(
        device_id="MW2-1E7C3325-9C2B-4E1F-8D64-0A5B7C11F203",
        payload={"operation": {"dryerOperationMode": "START"}},
    )
