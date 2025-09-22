#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@FileName    : vvv.py.py
@Time    : 2025/7/19 12:54
@Author  : XJC
@Description: 
"""
import asyncio

from pydantic import BaseModel


class Item(BaseModel):
    name: str

    async def item_sleep(self, val):
        print(self.name)
        return await asyncio.sleep(1)


async def main():
    df = Item(name="11")
    www = await df.item_sleep(val="111")
    print(www)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
