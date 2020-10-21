#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import aion.mysql as mysql

class SukibaAnalyticsDB(mysql.BaseMysqlAccess):
    def __init__(self):
        super().__init__("sukibaAnalytics")

    def get_base_master(self):
        sql = """
            SELECT * FROM baseMaster;
        """
        return self.get_query_list(100,sql)

    def update_latest_cache(self, args):
        sql = """
            INSERT INTO latestCache (vehicleCode, sukibaNo, baseID, mainBackup, l, h, w, temperature, timestamp)
                VALUES (%(vehicleCode)s, %(sukibaNo)s, %(baseID)s, %(mainBackup)s, %(l)s, %(h)s, %(w)s, %(temperature)s, %(timestamp)s)
            ON DUPLICATE KEY UPDATE
                l = %(l)s,
                h = %(h)s,
                w = %(w)s,
                temperature = %(temperature)s,
                timestamp = %(timestamp)s ;
        """
        self.set_query(sql, args)
