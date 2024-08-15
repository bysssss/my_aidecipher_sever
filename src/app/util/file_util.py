import json
import os
import shutil


def is_exists(file_path):
    try:
        flag = os.path.exists(file_path)
    except Exception as e:
        raise Exception(f"file_util.is_exists() : e={e}")
    return flag


def copy(src_path, dst_path):
    try:
        shutil.copyfile(src_path, dst_path)
    except Exception as e:
        raise Exception(f"file_util.copy() : e={e}")
    return


def read_json(json_path):
    try:
        fd = open(json_path, 'r', encoding="UTF-8")
        json_obj = json.load(fd)
        fd.close()
    except Exception as e:
        raise Exception(f"file_util.read_json() : e={e}")
    return json_obj


def write_json(json_path, json_obj):
    try:
        fd = open(json_path, 'w', encoding="UTF-8")
        fd.write(json.dumps(json_obj, ensure_ascii=False))
        fd.close()
    except Exception as e:
        raise Exception(f"file_util.write_json() : e={e}")
    return


def read_txt(txt_path):
    try:
        fd = open(txt_path, 'r', encoding='utf-8')
        text = fd.read()
        fd.close()
    except Exception as e:
        raise Exception(f"file_util.read_txt() : e={e}")
    return text


def write_txt(txt_path, text):
    try:
        fd = open(txt_path, 'w', encoding='utf-8')
        fd.write(text)
        fd.close()
    except Exception as e:
        raise Exception(f"file_util.write_txt() : e={e}")
    return
