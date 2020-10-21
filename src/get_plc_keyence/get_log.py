#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from datetime import datetime

PLC_MANUFACTURER = 'KEYENCE'
PLC_ENCODING = 'cp932'

def get_time_stamp(data_no, date, time):
    datestring = f'{date} {time}.{int(data_no):02}0000'
    return datetime.strptime(datestring, '%Y/%m/%d %H:%M:%S.%f')

def parse_strain_log(line):
    return {
        'VisionDate' : line[1],
        'VisionTime' : line[2],
        'VisionSerialNo' : line[3],
        'VisionCarModelNo' : line[4],
        'VisionSukibaNo' : line[5],
        'VisionTemperature' : line[6],
        'VisionMainBackup' : line[7],
        'UD01' : line[8],
        'UD02-1' : line[9],
        'UD02-2' : line[10],
        'UD03' : line[11],
        'UD04' : line[12],
        'UD05-1' : line[13],
        'UD05-2' : line[14],
        'UD05-3' : line[15],
        'UD06' : line[16],
        'UD07' : line[17],
        'UD08' : line[18],
        'UD09' : line[19],
        'UD10' : line[20],
        'LR01' : line[21],
        'LR02-1' : line[22],
        'LR02-2' : line[23],
        'LR03' : line[24],
        'LR04' : line[25],
        'LR05-1' : line[26],
        'LR05-2' : line[27],
        'LR05-3' : line[28],
        'LR06' : line[29],
        'LR07' : line[30],
        'LR08' : line[31],
        'LR09' : line[32],
        'LR10' : line[33],
        'timestamp': get_time_stamp(line[0],line[1],line[2]),
    }

def parse_tact_log(line):
    return {
        'VisionDate' : line[1],
        'VisionTime' : line[2],
        'VisionSerialNo' : line[3],
        'VisionCarModelNo' : line[4],
        'VisionSukibaNo' : line[5],
        'VisionTemperature' : line[6],
        'VisionCutoffMeasurement' : line[7],
        'VisionMainBackup' : line[8],
        'SF21L' : line[9],
        'SF21H' : line[10],
        'SF21W' : line[11],
        'SF01L' : line[12],
        'SF01H' : line[13],
        'SF01W' : line[14],
        'SF20W' : line[15],
        'SR01-1L' : line[16],
        'SR01-1H' : line[17],
        'SR01-1W' : line[18],
        'SR01-2L' : '0',
        'SR01-2H' : '0',
        'SR01-2W' : line[19],
        'SR03L' : line[20],
        'SR03H' : line[21],
        'SR03W' : line[22],
        'SC01L' : line[23],
        'SC01H' : line[24],
        'SC21L' : line[25],
        'SC21H' : line[26],
        'SC20W' : line[27],
        'SR02L' : line[28],
        'SR02H' : line[29],
        'SR02W' : line[30],
        'SW20L' : line[31],
        'SW20H' : line[32],
        'SW20W' : line[33],
        'SW21L' : line[34],
        'SW21H' : line[35],
        'SW21W' : line[36],
        'SW01L' : line[37],
        'SW01H' : line[38],
        'SW01W' : line[39],
        'timestamp': get_time_stamp(line[0],line[1],line[2]),
    }

def strain(csv_list):
    result = []
    for row in csv_list:
        result.append(parse_strain_log(row))
    return result

def tact(csv_list):
    result = []
    for row in csv_list:
        result.append(parse_tact_log(row))
    return result


