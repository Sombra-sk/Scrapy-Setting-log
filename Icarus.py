import os

from setting import DATA_PATH


def Icarus(strs):
    strs = strs.replace('\\', "%2A").replace('/', "%2A").replace('>', "%2A").replace('<', "%2A").replace(':',"%2A").replace('*', "%2A").replace('"', "%2A").replace('|', "%2A").replace('?', "%2A").strip()
    return strs


def html(data, path, html_name):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(rf'{path}/{html_name}.html', 'w', encoding='utf-8') as f:
        f.write(data)
    html(data, path, html_name)
