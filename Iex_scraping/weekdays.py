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
    rc=2
    weekend = 1

    for i in range(3,1897):
        if(weekend>=6):
            if(weekend==7):
                weekend = 1
            else:
                weekend+=1
        else:
            rc+=1
            wsheet['A'+str(rc)] = osheet['A'+str(i)].value
            wsheet['B'+str(rc)] = osheet['B'+str(i)].value
            weekend+=1
    print "saving newFileweekday"+str(d)+".xlsx......."
    wwb.save('newFileweekday'+str(d)+'.xlsx')

for i in range(1,97):
    weekday(i)
