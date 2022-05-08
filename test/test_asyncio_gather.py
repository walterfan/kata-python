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

    L = await asyncio.gather(
         say_after(2, "hello"),
         say_after(1, "world")
    )
    print(L)
    assert len(L) == 2
    assert L[0] == L[1] == None


def test_asynio_gather(capsys):

    asyncio.run(main())

    captured = capsys.readouterr()
    assert captured.out == 'world\nhello\n[None, None]\n'
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
        print(captured)

