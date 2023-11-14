from time import gmtime
from os import path, mkdir
from json import dump


def setup_dir() -> str:
    """
    Check if /data folder exists, create and return a directory for extracted data
    """
    if not(path.exists("./data")): mkdir("./data")
    t = gmtime()
    dir_path = f"./data/books_{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}"
    mkdir(dir_path)
    return dir_path

def write_data(result: dict, dir_path: str) -> int:
    """
    Write product info into json file
    """
    try:
        with open(f"{dir_path}/{result['Название']}.json", "w", encoding = "utf-8") as f:
            dump(result, f, ensure_ascii = False, indent = 4)
        return 0
    except:
        return 1