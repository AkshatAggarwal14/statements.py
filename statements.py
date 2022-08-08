from bs4 import BeautifulSoup
import requests
from pylatexenc.latex2text import LatexNodes2Text


def prettify(s: str) -> str:
    return (' '.join(s.split())).strip()


def get(which_soup, to_find, attrs_: dict = {}, index=None):
    divs = [div.find(text=True, recursive=False)
            for div in which_soup.find_all(to_find, attrs=attrs_)]
    if index != None:
        return divs[index]
    return ' '.join(divs)


def get_text_from_latex(s: str) -> str:
    return prettify(LatexNodes2Text().latex_to_text(s))


def parse_statement(c_id: str, p_id: str):
    # RCPC = token_decoder.get_RCPC()
    # cookies = {'RCPC': RCPC}
    # print('RCPC Token Decoded: {}'.format(RCPC))
    c_url = f'http://codeforces.com/contest/{c_id}'
    p_url = f'{c_url}/problem/{p_id}'
    # page = requests.get(c_url, cookies=cookies)
    page = requests.get(c_url)
    if page.status_code == 200:
        # page = requests.get(p_url, cookies=cookies)
        page = requests.get(p_url)
        if page.status_code == 200:
            html = page.text
            soup = BeautifulSoup(html, 'html.parser')
            resp = {}
            resp['status'] = 'OK'
            resp['details'] = 'problem fetched'
            resp['title'] = (
                get(soup, 'div', {'class': 'title'}, 0))[3:]
            resp['time_limit'] = get(
                soup, 'div', {'class': 'time-limit'})
            resp['memory_limit'] = get(
                soup, 'div', {'class': 'memory-limit'})
            resp['input'] = get(soup, 'div', {'class': 'input-file'})
            resp['output'] = get(soup, 'div', {'class': 'output-file'})

            for div in soup.find_all('div', {'class': 'problem-statement'}):
                for paras in div.find_all('div', {'class': None}):
                    resp['statement'] = [
                        get_text_from_latex(prettify(para.text)) for para in paras]

            for paras in soup.find_all('div', {'class': 'input-specification'}):
                resp['input_format'] = [
                    get_text_from_latex(prettify(para.text)) for para in paras.find_all('p')]

            for paras in soup.find_all('div', {'class': 'output-specification'}):
                resp['output_format'] = [
                    get_text_from_latex(prettify(para.text)) for para in paras.find_all('p')]

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
        else:
            return {'status': 'ERROR', 'details': f"{p_url} not accessible"}
    else:
        return {'status': 'ERROR', 'details': f"{c_url} not accessible"}
