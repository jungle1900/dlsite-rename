import shutil
import requests
from bs4 import BeautifulSoup
from config import conf

MIME_TYPES = {
    'image/gif': 'gif',
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41'
WEB_PATH = 'https://www.dlsite.com/maniax/work/=/product_id/{code}.html'

s = requests.session()


def get_product_data(code):
    res = s.get(WEB_PATH.format(code=code), headers={'user-agent': USER_AGENT})
    if res.status_code != 200:
        raise RuntimeError(res.status_code, res.content)

    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.select_one('#work_name').string
    maker = soup.select_one('#work_maker .maker_name a').string
    image = soup.select_one('#work_left .slider_item img')['srcset']

    return code, title, maker, image


def create_shortcut(save_path, code):
    file_path = f'{save_path}/{conf["shortcut_filename"]}.url'

    with open(file_path, 'w') as file:
        file.write('[InternetShortcut]\nURL=')
        file.write(WEB_PATH.format(code=code))


def download_image(save_path, url):
    if url.startswith('//'):
        url = 'https:' + url

    res = s.get(url, stream=True)
    if res.status_code != 200:
        raise RuntimeError(res.status_code, res.content)

    extension = MIME_TYPES[res.headers['content-type']]
    file_path = f'{save_path}/{conf["cover_filename"]}.{extension}'

    with open(file_path, 'wb') as file:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, file)
