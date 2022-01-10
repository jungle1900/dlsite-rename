import re
import logging
from datetime import datetime
from time import sleep
from pathlib import Path
from config import conf
import dlsite

RJ_CODE_PATTERN = re.compile('(RJ\d{6})', re.I)
TITLE_SUB_PATTERN = re.compile('【.*?】', re.U)
WINDOWS_REPLACE_TABLE = str.maketrans('<>:"/\|?*', '＜＞：＂／＼｜？＊')


def get_files(path):
    files = []
    for x in path.iterdir():
        if conf['only_dir'] and not x.is_dir():
            continue
        files.append(x)

    return files


def build_filename(code, title, maker):
    title = TITLE_SUB_PATTERN.sub('', title)
    title = title.translate(WINDOWS_REPLACE_TABLE)
    title = title.strip()
    maker = maker.translate(WINDOWS_REPLACE_TABLE)

    return conf["name_format"].format(code=code, title=title, maker=maker)


def main():
    logging.basicConfig(
        filename='error.log',
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8',
        level=logging.ERROR,
    )

    from_dir = Path(conf['from_dir'].rstrip('/'))
    if not from_dir.is_dir():
        print('from_dir 資料夾不存在')
        return

    to_dir = Path(conf['to_dir'].rstrip('/'))
    if not to_dir.is_dir():
        to_dir.mkdir()

    files = get_files(from_dir)

    for file in files:
        match = RJ_CODE_PATTERN.search(str(file))
        if not match:
            continue

        code = match.group().upper()
        print(f'處理 {code} 中...', end='')

        try:
            code, title, maker, image = dlsite.get_product_data(code)
        except Exception as e:
            print('訪問 DLsite 失敗，略過此作品')
            logging.error(e)
            continue

        if conf['create_shortcut'] and file.is_dir():
            try:
                dlsite.create_shortcut(file, code)
            except Exception as e:
                print('建立捷徑失敗，略過此作品')
                logging.error(e)
                continue

        if conf['download_cover'] and file.is_dir():
            try:
                dlsite.download_image(file, image)
            except Exception as e:
                print('下載封面失敗，略過此作品')
                logging.error(e)
                continue

        file.rename(to_dir / build_filename(code, title, maker))

        print('成功')
        sleep(0.2)

    input('處理完畢，按下 enter 退出')


if __name__ == "__main__":
    main()
