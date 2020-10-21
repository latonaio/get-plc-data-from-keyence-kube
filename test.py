
import os
from ftplib import FTP
from pprint import pprint

class FTPClient:
    ftp = None

    def __init__(self):
        ftp_user = "KV"#os.environ.get('FTP_USER')
        ftp_passwd = "admin"#os.environ.get('FTP_PASSWD')
        #self.ftp = FTP(host='localhost', user=ftp_user, passwd=ftp_passwd, source_address=('localhost',30001))
        self.ftp = FTP()
        self.ftp.connect('localhost', 30001)
        self.ftp.login('KV','admin')

    def get_file_list(self, remote_dir):
        result = self.ftp.nlst('.'+remote_dir)
        return result
        
    def download_file(self, remote_dir, target_name, save_dir):
        save_path = os.path.join(save_dir, target_name)
        with open(save_path, 'wb') as fp:
            self.ftp.retrbinary('RETR '+target_name, fp.write)
        return save_path

    def __del__(self):
        if self.ftp:
            self.ftp.quit()


if __name__ == "__main__":
    ftp_client = FTPClient()
    fl = ftp_client.get_file_list('')
    ftp_client.download_file('', fl[0] ,'')
    
