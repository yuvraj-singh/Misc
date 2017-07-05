import os
import sys
import datetime
import openpyxl
from dateutil.parser import parse
from subprocess import call

def weekday(d):
    wwb = openpyxl.Workbook()
    wsheet = wwb.get_sheet_by_name('Sheet')
    owb = openpyxl.load_workbook("newbidFile"+str(d)+".xlsx")
    osheet = owb.get_sheet_by_name('Sheet')
    wsheet['A1'] = 'Date'
    wsheet['B1'] = 'MCP'
    wsheet['C1'] = 'Purchase Bid'
    wsheet['D1'] = 'Sell Bid'
    rc=1
    weekend = 1
    for i in range(3,1924):
        if(weekend >= 6):
            if(weekend == 7):
                weekend = 1
            else:
                weekend += 1
        else:
            rc+=1
            wsheet['A'+str(rc)] = osheet['A'+str(i)].value
            wsheet['B'+str(rc)] = osheet['G'+str(i)].value
            wsheet['C'+str(rc)] = osheet['B'+str(i)].value
            wsheet['D'+str(rc)] = osheet['C'+str(i)].value
            weekend+=1
    sameday_val = [0, 0, 0]
    column = ['B', 'C', 'D']
    for col in range(1,4):
        sameday = 89 - (3 * 5)
        for i in range(1,8):
            if (i   ==  4):
                sameday += 5
            else:
                sameday_val[col-1] += float(wsheet[column[col-1]+str(sameday)].value)
                sameday += 5
    wsheet['B'+str(89)] = round(sameday_val[0] / 6, 2)
    wsheet['C'+str(89)] = round(sameday_val[1] / 6, 2)
    wsheet['D'+str(89)] = round(sameday_val[2] / 6, 2)
    print "saving BidFileweekday"+str(d)+".xlsx......."
    wwb.save('BidFileweekday'+str(d)+'.xlsx')

for i in range(1,97):
    weekday(i)
