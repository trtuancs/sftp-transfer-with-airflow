from ftplib import FTP
from logging import info
import os

HISTORY_FILE = '/opt/history.log'
FTP_PATH_START = ''
LOCAL_PATH = '/tmp'


def _get_history_files(history_file):
    """
    Retrieve a set of history files from the specified history file.

    :param history_file: Path to the history file.
    :return: A set containing the history files.
    """
    history_files = set()
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history_files.update(f.read().splitlines())
    return history_files


def _write_history(history_file, files_dir):
    """
    Write a list of new files to the history file.

    :param history_file: Path to the history file.
    :param files_dir: List of new file paths to write.
    """
    with open(history_file, 'a') as f:
        f.write('\n'.join(files_dir) + '\n')


def _integrate_ele(ftp_source, ftp_target, history_files, mem, ftp_path_start):
    """
    Recursively integrate files and folders from the source FTP server to the target FTP server.

    :param ftp_source: FTP object for the source server.
    :param ftp_target: FTP object for the target server.
    :param history_files: Set of history files.
    :param mem: Dictionary to store memory during recursion.
    :param ftp_path_start: Initial path on the FTP server to start integration.
    """
    mem['absolute_path'] = ftp_path_start if mem['absolute_path'] == '' else f"{mem['absolute_path']}/{ftp_path_start}"
    ftp_source.cwd(ftp_path_start)
    ftp_target.cwd(ftp_path_start)
    eles = ftp_source.nlst()
    files = [ele for ele in eles if '.' in ele]
    folders = [ele for ele in eles if '.' not in ele]
    for file in files:
        path = f"{mem['absolute_path']}/{file}"
        if path not in history_files:
            ftp_source.retrbinary("RETR " + file, open(file, 'wb').write)
            respond = ftp_target.storbinary("STOR " + file, fp=open(file, "rb"))
            os.remove(file)
            info(f"===> Integrated file: {path}")
            mem['new_files'].append(path)
    for folder in folders:
        if folder not in ftp_target.nlst():
            ftp_target.mkd(folder)
        _integrate_ele(ftp_source, ftp_target, history_files, mem, folder)
        ftp_source.cwd('..')
        ftp_target.cwd('..')
        mem['absolute_path'] = '/'.join(ele for ele in mem['absolute_path'].split('/')[:-1])


def integrate_ftp_server(source, target, **kwargs):
    """
    Integrate files and folders from a source FTP server to a target FTP server.

    :param source: Object containing FTP connection details for the source server.
    :param target: Object containing FTP connection details for the target server.
    :param kwargs: Additional optional arguments.
        - history_file: Path to the history file (optional, default is '/opt/history.log').
        - ftp_path_start: Initial path on the FTP server to start integration (optional, default is '').
    """
    os.chdir(LOCAL_PATH)
    history_file = kwargs.get('history_file') if kwargs.get('history_file') is not None else HISTORY_FILE
    ftp_path_start = kwargs.get('ftp_path_start') if kwargs.get('ftp_path_start') is not None else FTP_PATH_START
    history_files = _get_history_files(history_file)
    ftp_source = FTP(source.HOST, user=source.USER, passwd=source.PASSWD)
    ftp_target = FTP(target.HOST, user=target.USER, passwd=target.PASSWD)
    mem = {
        'absolute_path': '',
        'new_files': []
    }
    _integrate_ele(ftp_source, ftp_target, history_files, mem, ftp_path_start)
    _write_history(history_file, mem['new_files'])
