"""Blebox binary_sensor entities test."""
from unittest.mock import PropertyMock

import blebox_uniapi
import pytest

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import ATTR_DEVICE_CLASS, STATE_ON
from homeassistant.helpers import device_registry as dr

from .conftest import async_setup_entity, mock_feature


@pytest.fixture(name="rainsensor")
def airsensor_fixture():
    """Return a default air quality fixture."""
    feature = mock_feature(
        "binary_sensors",
        blebox_uniapi.binary_sensor.Rain,
        unique_id="BleBox-windRainSensor-ea68e74f4f49-0.rain",
        full_name="windRainSensor-0.rain",
        device_class="moisture",
    )
    product = feature.product
    type(product).name = PropertyMock(return_value="My rain sensor")
    type(product).model = PropertyMock(return_value="rainSensor")
    return (feature, "binary_sensor.windrainsensor_0_rain")


async def test_init(rainsensor, hass, config):
    """Test binary_sensor initialisation."""
    _, entity_id = rainsensor
    entry = await async_setup_entity(hass, config, entity_id)
    assert entry.unique_id == "BleBox-windRainSensor-ea68e74f4f49-0.rain"

    state = hass.states.get(entity_id)
    assert state.name == "windRainSensor-0.rain"

    assert state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.MOISTURE
    assert state.state == STATE_ON

    device_registry = dr.async_get(hass)
    device = device_registry.async_get(entry.device_id)

    assert device.name == "My rain sensor"
