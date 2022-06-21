import sys
from pathlib import Path
import zipfile
import shutil
import argparse

def err(arg):
    print(arg, file=sys.stderr)
    sys.exit(1)

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('file', type=Path, help='.sb2 file to extract')
    p.add_argument('-u', '--unzip', help='Also unzip file',action='store_true')
    p.add_argument('-T', '--keep-temp', help='Keep temporary files',action='store_true')
    p.add_argument('-t', '--target', help='Target file', type=Path)
    args = p.parse_args(argv)
    src_path = args.file
    if not src_path.exists():
        err(f"No such file or directory: {src_path}")
    if not src_path.is_file():
        err(f"No such file: {src_path}")
    if not src_path.suffix == '.sb2':
        err(f"Is not .sb2 file: {src_path}")
    if args.keep_temp or not args.unzip:
        dst_zip = src_path.with_suffix('.zip')
        shutil.copy2(src_path, dst_zip)
    if args.unzip:
        dst = src_path.with_suffix('')
        with zipfile.ZipFile(src_path, 'r') as zipref:
            zipref.extractall(dst)

if __name__ == '__main__':
    main(sys.argv[1:])
