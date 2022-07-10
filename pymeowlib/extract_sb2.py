from pathlib import Path
import shutil


def unzip(src, dst=None):
    dst = dst or Path(src).with_suffix('')
    shutil.unpack_archive(src, dst)


def zip_proj(src, dst):
    dst = dst or Path(src).with_suffix('.sb2')
    shutil.make_archive(dst, 'zip', src)


def get_proj_file_path(base):
    return Path(base) / 'project.json'


def read_proj_file(base):
    with open(get_proj_file_path(base)) as f:
        return f.read()


def write_proj_file(base, text):
    with open(get_proj_file_path(base), 'w') as f:
        f.write(text)


def open_proj_file(base, *args, **kwargs):
    return open(get_proj_file_path(base), *args, **kwargs)
