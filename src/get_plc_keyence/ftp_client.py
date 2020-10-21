#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
from ftplib import FTP
from aion.logger import lprint


class FTPClient:

    def __init__(self):
        ftp_user = os.environ.get('FTP_USER')
        ftp_passwd = os.environ.get('FTP_PASSWD')
        lprint(f'{ftp_user}:{ftp_passwd}')
        self.ftp = FTP(host='ftp', user=ftp_user, passwd=ftp_passwd)

    def get_file_list(self, remote_dir):
        result = self.ftp.nlst(remote_dir)
        return result
        
    def download_file(self, remote_dir, target_name, save_dir):
        save_path = os.path.join(save_dir, target_name)
        #remote_path = os.path.join(remote_dir, target_name)
        with open(save_path, 'wb') as fp:
            self.ftp.retrbinary('RETR '+target_name, fp.write)
        return save_path

    def __del__(self):
        if self.ftp:
            self.ftp.quit()
