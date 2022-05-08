#!/usr/bin/env python3
import pytest

import asyncio
import time


def setup_function(function):
    print("start...", function)
    
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    
async def main():
    print(f"started at {time.strftime('%X')}")
    
    await say_after(2, "hello")
    await say_after(1, "world")
    
    print(f"finished at {time.strftime('%X')}")

def test_asynio_run():
    asyncio.run(main())