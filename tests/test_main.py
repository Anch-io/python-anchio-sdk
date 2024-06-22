import os
from time import sleep
from typing import Any
from unittest.mock import patch

import pytest


from anchio_sdk import AnchioInit, AnchioMaxEnqueuedAttempts
from async_anchio.models.meter_entry_schema import MeterEntrySchema

class MockDefaultApi:
    def __init__(self, *args: Any, **kwarg: Any) -> None:
        pass

    async def create_meter_entries_api_v1_metering_meter_entry_post(self, data):
        return data

@patch('anchio_sdk.main.DefaultApi', MockDefaultApi)
def test_main_monitor_running_stable_5_seconds():
    service = AnchioInit(
        token="test",
        max_queue_size=100
    )
    raise_exception = False
    try:
        for i in range(500):
            sleep(0.002)
            service.send_entry({"value": 1, "metric": "A", "service": "Service"}, max_attempts=1)
    except AnchioMaxEnqueuedAttempts:
        raise_exception = True
    sleep(5)
    assert not raise_exception


@pytest.mark.asyncio
@patch('anchio_sdk.main.DefaultApi', MockDefaultApi)
async def test_run_inside_of_async_context():
    service = AnchioInit(
        token="test",
        max_queue_size=100
    )
    raise_exception = False
    try:
        for i in range(500):
            sleep(0.002)
            await service.async_send_entry({"value": 1, "metric": "A", "service": "Service"}, max_attempts=1)
    except AnchioMaxEnqueuedAttempts:
        raise_exception = True
    sleep(5)
    assert not raise_exception

    
    

