#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from datetime import datetime
from time import sleep
import os
from pathlib import Path

# AION func
from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.mongo import BaseMongoAccess
from aion.logger import lprint

# my lib
from .open_csv import open_csv
from .ftp_client import FTPClient
from .get_log import tact, strain, PLC_ENCODING
from .sukiba_analytics_db import SukibaAnalyticsDB

SERVICE_NAME = "get-plc-data-from-keyence"
LOG_INTERVAL = 1
AION_HOME = os.environ.get("AION_HOME", "/var/lib/aion/")

MONGO_DB_NAME = "Vision"
MONGO_TACT_NAME = "Tact"
MONGO_HIZUMI_NAME = "Strain"
FTP_TACT_PATH = "KEYENCE/VISION"
FTP_HIZUMI_PATH = "KEYENCE/STRAIN"


def get_latest_file(ftp_dir, copy_dir):
    ftp = FTPClient()
    file_list = ftp.get_file_list(ftp_dir)

    if len(file_list) > 0:
        sorted_list = sorted(file_list, reverse=True)
        ftp.download_file(ftp_dir, sorted_list[0], copy_dir)
        del ftp
        return os.path.join(copy_dir, sorted_list[0])
    else:
        del ftp
        return ""

def separate_lhw(base_master, tact_log):
    result = []
    for base in base_master:
        base_name = base.get('name')
        if tact_log.get(base_name+'L') is not None:
            result.append({
                'vehicleCode' : int(tact_log.get('VisionCarModelNo')),
                'sukibaNo' : int(tact_log.get('VisionSukibaNo')),
                'baseID' : int(base.get('id')),
                'mainBackup' : int(tact_log.get('VisionMainBackup')),
                'l' : float(tact_log.get(base_name+'L')),
                'h' : float(tact_log.get(base_name+'H', '0')),
                'w' : float(tact_log.get(base_name+'W', '0')),
                'temperature' : float(tact_log.get('VisionTemperature')),
                'timestamp' : str(tact_log.get('timestamp'))
            })
    return result

class GetData:
    def __init__(self, ftp_dir, file_dir, log_format, collection_name):
        self.ftp_dir = ftp_dir
        self.file_dir = file_dir
        self.log_format = log_format
        self.collection_name = collection_name
        #self.last_check_file = ''
        self.last_check_file = get_latest_file(self.ftp_dir, self.file_dir)

    def getData(self):
        latest_file = get_latest_file(self.ftp_dir, self.file_dir)
        lprint(f'latest_file:{latest_file}')
        if latest_file == "":
            return # skip if file isn't exists in LOG_BASE_PATH
        if latest_file == self.last_check_file:
            return # skip if file is same as last opened

        # get robot data
        latest_dir = os.path.join(self.file_dir, latest_file)
        csv_list = open_csv(latest_file, PLC_ENCODING)
        robot_data = self.log_format(csv_list[1:])

        # get timestamp
        timestamp = datetime.now().isoformat()

        try:
            with SukibaAnalyticsDB() as db:
                base_master = db.get_base_master()
                lhw_data = separate_lhw(base_master, robot_data[-1])
                for args in lhw_data:       
                    db.update_latest_cache(args)
                db.commit_query()
        except Exception as e:
            lprint(str(e))

        with BaseMongoAccess(MONGO_DB_NAME) as db:
            db.insert_many(self.collection_name,robot_data)

        # output after kanban
        '''
        conn.output_kanban(
            result=True,
            connection_key="key",
            output_data_path=data_path,
            process_number=num + 1,
            metadata={
                "RobotData": robot_data,
                "timestamp": timestamp,
            },
        )
        '''

        self.last_check_file = latest_file
        return


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()
    # get cache kanban
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)
    # get output data path
    data_path = kanban.get_data_path()

    ######### main function #############


    service_dir = "%s_%d" % (SERVICE_NAME, num)
    file_dir = os.path.join(AION_HOME, "Data", service_dir, "output") 
    os.makedirs(file_dir, exist_ok=True)
    os.makedirs(os.path.join(file_dir,FTP_TACT_PATH), exist_ok=True)
    os.makedirs(os.path.join(file_dir,FTP_HIZUMI_PATH), exist_ok=True)

    tact_get = GetData(FTP_TACT_PATH, file_dir, tact, MONGO_TACT_NAME)
    strain_get = GetData(FTP_HIZUMI_PATH, file_dir, strain, MONGO_HIZUMI_NAME)

    while True:
        sleep( LOG_INTERVAL )
        tact_get.getData()
        strain_get.getData()
