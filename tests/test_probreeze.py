from unittest.mock import MagicMock, patch

from smart_home_hub.devices.probreeze import ProBreeze


def _make_device():
    with patch("smart_home_hub.devices.probreeze.tinytuya.Device") as mock_cls:
        mock_tuya = MagicMock()
        mock_tuya.status.return_value = {
            "dps": {
                "1": True,
                "2": "0",
                "4": 70,
                "5": False,
                "6": "3",
                "7": False,
                "11": 1,
                "102": False,
                "103": 20,
                "104": 56,
                "105": False,
            }
        }
        mock_cls.return_value = mock_tuya

        device = ProBreeze(
            name="test_dehumidifier",
            host="192.168.1.2",
            device_id="abc123",
            local_key="key456",
        )
    return device, mock_tuya


def test_probreeze_on():
    device, mock_tuya = _make_device()
    device.on()
    mock_tuya.set_value.assert_called_once_with("1", True)


def test_probreeze_off():
    device, mock_tuya = _make_device()
    device.off()
    mock_tuya.set_value.assert_called_once_with("1", False)


def test_probreeze_status():
    device, mock_tuya = _make_device()
    status = device.status()

    assert status["running"] is True
    assert status["current_humidity"] == 56
    assert status["target_humidity"] == 70
    assert status["current_temp"] == 20
    assert status["tank_full"] is False


def test_probreeze_set_humidity():
    device, mock_tuya = _make_device()
    device.set_humidity(50)
    mock_tuya.set_value.assert_called_once_with("4", 50)
