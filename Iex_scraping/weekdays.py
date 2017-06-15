import os
import sys
import datetime
import openpyxl
from dateutil.parser import parse
from subprocess import call

def weekday(d):
    wwb = openpyxl.Workbook()
    wsheet = wwb.get_sheet_by_name('Sheet')
    owb = openpyxl.load_workbook("newFile"+str(d)+".xlsx")
    osheet = owb.get_sheet_by_name('Sheet')
    wsheet['A1'] = 'Date'
    wsheet['B1'] = 'MCP'
    rc=1
    weekend = 1
    for i in range(3,1897):
        if(weekend >= 6):
            if(weekend == 7):
                weekend = 1
            else:
                weekend += 1
        else:
            rc+=1
            wsheet['A'+str(rc)] = osheet['A'+str(i)].value
            wsheet['B'+str(rc)] = osheet['B'+str(i)].value
            weekend+=1

    sameday = 89 - (3 * 5)
    sameday_val = 0
    for i in range(1,8):
        if (i   ==  4):
            sameday += 5
        else:
            sameday_val += float(wsheet['B'+str(sameday)].value)
            sameday += 5
    wsheet['B'+str(89)] = round(sameday_val / 6, 2)
    print "saving Fileweekday"+str(d)+".xlsx......."
    wwb.save('Fileweekday'+str(d)+'.xlsx')

for i in range(1,97):
    weekday(i)
