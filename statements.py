from bs4 import BeautifulSoup
import requests
import json
import aiohttp
import re
from pylatexenc.latex2text import LatexNodes2Text as l2t


async def parse_id(id: str) -> list:
    c_id = ""
    cnt = 0
    for c in id:
        if c.isalpha():
            break
        cnt += 1
        c_id += c
    p_id = id[-len(id)+cnt:]
    return [c_id, p_id]


async def parse_statement(c_id: str, p_id: str):
    async with aiohttp.ClientSession() as session:
        c_url = f'http://codeforces.com/contest/{c_id}'
        async with session.get(c_url, allow_redirects=False) as page:
            if page.status == 200:
                p_url = f'http://codeforces.com/contest/{c_id}/problem/{p_id}'
                async with session.get(p_url, allow_redirects=False) as page:
                    if page.status == 200:
                        page = await page.text()
                        soup = BeautifulSoup(page, 'html.parser')
                        divs = soup.find_all('div')
                        # for i in range(len(divs)):
                        # print(i, ':', divs[i], '\n')
                        stuff = [75, 76, 78, 81, 83, 84, 85, 87, 92, 94, 96]
                        res = []
                        for i in stuff:
                            res.append(l2t(strict_latex_spaces=True).latex_to_text(
                                divs[i].text))
                        for line in res:
                            print(line, file=open('output.txt',
                                  mode='a', encoding='utf-8'))
                        return res

# 75+
