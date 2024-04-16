from ftplib import FTP
from logging import info
import os
from pathlib import Path

def _get_history_files(history_file):
    with open(history_file, "r") as file:
        files = [file.replace('\n', '') for file in file.readlines()]
    return files

def _write_history(history_file, files_dir):
    with open(history_file, "a") as file:
        for line in files_dir:
            file.write(line + "\n")

def _integrate_ele(ftp_source, ftp_target, ftp_path_start=''):
    global history, new_files
    if history == '':
        history += ftp_path_start
    else:
        history = f"{history}/{ftp_path_start}"
    ftp_source.cwd(ftp_path_start)
    ftp_target.cwd(ftp_path_start)
    eles = ftp_source.nlst()
    files = [ele for ele in eles if '.' in ele]
    folders = [ele for ele in eles if '.' not in ele]
    for file in files:
        path = f"{history}/{file}"
        if path not in history_files:
            ftp_source.retrbinary("RETR " + file, open(file, 'wb').write)
            respond = ftp_target.storbinary("STOR " + file, fp=open(file, "rb"))
            os.remove(file)
            new_files.append(path)
    for folder in folders:
        if folder not in ftp_target.nlst():
            ftp_target.mkd(folder)
        _integrate_ele(ftp_source, ftp_target, folder)
        ftp_source.cwd('..')
        ftp_target.cwd('..')
        history = '/'.join(ele for ele in history.split('/')[:-1])

def integrate_ftp_server(source, target, history_file='/opt/history.log', **kwargs):
    history = ''
    history_files = _get_history_files(history_file)
    new_files = []

    ftp_source = FTP(source.HOST, user=source.USER, passwd=source.PASSWD)
    ftp_target = FTP(target.HOST, user=target.USER, passwd=target.PASSWD)
    _integrate_ele(ftp_source, ftp_target)
    _write_history(history_file,new_files)