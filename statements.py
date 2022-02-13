from attr import attr, attrs
from bs4 import BeautifulSoup
import aiohttp


async def prettify(s: str):
    return (' '.join(s.split())).strip()


async def get(which_soup, to_find, attrs_: dict = {}, index=None, getList=False):

    divs = [div.find(text=True, recursive=False)
            for div in which_soup.find_all(to_find, attrs=attrs_)]
    if getList:
        return divs
    if index != None:
        return divs[index]
    return ' '.join(divs)


async def parse_statement(c_id: str, p_id: str):
    async with aiohttp.ClientSession() as session:
        c_url = f'http://codeforces.com/contest/{c_id}'
        async with session.get(c_url, allow_redirects=False) as page:
            if page.status == 200:
                p_url = f'http://codeforces.com/contest/{c_id}/problem/{p_id}'
                async with session.get(p_url, allow_redirects=False) as page:
                    if page.status == 200:
                        html = await page.read()
                        page.close()
                        resp = {}
                        soup = BeautifulSoup(html, 'html.parser')
                        resp['title'] = await get(soup, 'div', {'class': 'title'}, 0)
                        resp['time_limit'] = await get(soup, 'div', {'class': 'time-limit'})
                        resp['memory_limit'] = await get(soup, 'div', {'class': 'memory-limit'})
                        resp['input'] = await get(soup, 'div', {'class': 'input-file'})
                        resp['output'] = await get(soup, 'div', {'class': 'output-file'})

                        for div in soup.find_all('div', {'class': 'problem-statement'}):
                            for paras in div.find_all('div', {'class': None}):
                                resp['statement'] = [
                                    await prettify(para.text) for para in paras]

                        for paras in soup.find_all('div', {'class': 'input-specification'}):
                            resp['input_specification'] = [
                                await prettify(para.text) for para in paras.find_all('p')]

                        for paras in soup.find_all('div', {'class': 'output-specification'}):
                            resp['output_specification'] = [
                                await prettify(para.text) for para in paras.find_all('p')]

                        sample_ins = []
                        for div in soup.find_all('div', {'class': 'input'}):
                            for input in div.find_all('pre'):
                                sample_ins.append(
                                    input.text.strip().splitlines())
                        resp['sample_input'] = sample_ins

                        sample_outs = []
                        for div in soup.find_all('div', {'class': 'output'}):
                            for output in div.find_all('pre'):
                                sample_outs.append(
                                    input.text.strip().splitlines())
                        resp['sample_output'] = sample_outs

                        return resp
