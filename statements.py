from bs4 import BeautifulSoup as bs
import aiohttp
import asyncio
from pylatexenc.latex2text import LatexNodes2Text

async def get(which_soup, to_find, attrs_: dict = {}, index=None):
    divs = [div.find(text=True, recursive=False)
            for div in which_soup.find_all(to_find, attrs=attrs_)]
    if index != None:
        return divs[index]
    return ' '.join(divs)


async def get_text_from_latex(s: str) -> str:
    return ' '.join(LatexNodes2Text().latex_to_text(s).split()).strip()


async def parse_statement(c_id: str, p_id: str):
    c_url = f'https://codeforces.com/contest/{c_id}'
    p_url = f'{c_url}/problem/{p_id}'
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.get(c_url, allow_redirects=False),
                session.get(p_url, allow_redirects=False)
            ]
            cpage, page = await asyncio.gather(*tasks)

            if cpage.status != 200:
                return {'status': 'ERROR', 'details': f"{c_url} not accessible"}

            if page.status != 200:
                return {'status': 'ERROR', 'details': f"{p_url} not accessible"}

            html = await page.text()
            soup = bs(html, 'html.parser')

            resp = {}
            resp['status'] = 'OK'
            resp['details'] = 'problem fetched'
            resp['title'] = (await get(soup, 'div', {'class': 'title'}, 0))[3:].strip()
            resp['time_limit'] = await get(soup, 'div', {'class': 'time-limit'})
            resp['memory_limit'] = await get(soup, 'div', {'class': 'memory-limit'})
            resp['input'] = await get(soup, 'div', {'class': 'input-file'})
            resp['output'] = await get(soup, 'div', {'class': 'output-file'})

            for div in soup.find_all('div', {'class': 'problem-statement'}):
                for paras in div.find_all('div', {'class': None}):
                    resp['statement'] = [
                        await get_text_from_latex(para.text) for para in paras]

            for paras in soup.find_all('div', {'class': 'input-specification'}):
                resp['input_format'] = [
                    await get_text_from_latex(para.text) for para in paras.find_all('p')]

            for paras in soup.find_all('div', {'class': 'output-specification'}):
                resp['output_format'] = [
                    await get_text_from_latex(para.text) for para in paras.find_all('p')]

            resp['samples'] = []
            sample_ins = []
            for div in soup.find_all('div', {'class': 'input'}):
                for input in div.find_all('pre'):
                    test_case = ""
                    for x in input.find_all('div', {'class': lambda value: value and value.startswith("test-example-line")}):
                        test_case += x.get_text() + '\n'
                    if len(test_case) == 0:  # if not multiple test cases in a given sample
                        test_case = input.get_text()
                    sample_ins.append(
                        test_case.strip().splitlines())
            sample_outs = []
            for div in soup.find_all('div', {'class': 'output'}):
                for output in div.find_all('pre'):
                    sample_outs.append(
                        output.text.strip().splitlines())

            for i in range(0, len(sample_ins)):
                resp['samples'].append(
                    {'input': sample_ins[i], 'output': sample_outs[i]})

            return resp
    except:
        return {'status': 'ERROR', 'details': 'Internal Server Error :('}
