#!/usr/bin/env python3

import subprocess
import logging
import os

logging.basicConfig(level = os.getenv('LOG_LEVEL', 'DEBUG').strip().upper())
LOG = logging.getLogger(__name__)

_RCLONE_SOURCE = '/mnt/movies'
_RCLONE_TARGET = 'rclone-test'

_RCLONE_BINARY = '/home/glatki/dev/slowsync/rclone-v1.42-linux-amd64/rclone'

def _rclone_command(command):
    LOG.debug('Run command: %s %s', _RCLONE_BINARY, command)
    p = subprocess.run([_RCLONE_BINARY] + command, capture_output = True)
    return p.stdout.decode()

def _get_rel_path(root_dir, full_dir, file_name):
    rel_dir = ''
    if root_dir != full_dir:
        rel_dir = os.path.relpath(full_dir, root_dir)
    return os.path.join(rel_dir, file_name)

def _upload_item(item):
    LOG.info('Upload item: ' , item)
    _rclone_command('copy --dry-run %s')


def read_local():
    res = dict()
    for root, dirnames, files in os.walk(_RCLONE_SOURCE, topdown=False):
        for name in files:
            res[_get_rel_path(_RCLONE_SOURCE, root, name)] = True
        for name in dirnames:
            res[_get_rel_path(_RCLONE_SOURCE, root, name)] = True

    return dict()

def read_remote():
    remote_files = _rclone_command(['lsf', '-R', _RCLONE_TARGET + ':']).splitlines()
    res = dict()
    for item in remote_files:
        res[item] = True
    print(res)
    return res

def main():
    LOG.info('Read local files from %s', _RCLONE_SOURCE)
    #local_files = read_local()
    LOG.info('Read remote files from %s', _RCLONE_TARGET)
    remote_files = read_remote()

    for item in local_files:
        if not item in remote_files:
            _upload_item(item)
        sys.exit(0)

main()
