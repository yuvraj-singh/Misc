import os
import sys
import datetime
import openpyxl
from dateutil.parser import parse
from subprocess import call

# dt = parse('Feb 15 2010')
# print(dt)
# # datetime.datetime(2010, 2, 15, 0, 0)
# print(dt.strftime('%d/%m/%Y'))
# # 15/02/2010
sdate = "05/20/2017" # default starting date
edate = "05/20/2017" # default  ending date

if len(sys.argv) == 2:
	sdate = sys.argv[1]
	edate = sdate

if len(sys.argv) >= 3:
	sdate = sys.argv[1]
	edate = sys.argv[2]

format = "EXCELOPENXML"
if len(sys.argv) >= 4:
	format = sys.argv[3]


def download_files():
	datediff = 30
	stemp = parse(sdate)
	date = stemp + datetime.timedelta(days=datediff-1)
	fc = 1
	while (date < parse(edate)):
		os.system("python download_bid.py"+" "+stemp.strftime('%d/%m/%Y')+" "+date.strftime('%d/%m/%Y')+" "+"BidFile"+str(fc))
		stemp = date + datetime.timedelta(days=1)
		date += datetime.timedelta(days=datediff)
		fc += 1
	os.system("python download_bid.py"+" "+stemp.strftime('%d/%m/%Y')+" "+parse(edate).strftime('%d/%m/%Y')+" "+"BidFile"+str(fc))
	return(fc)

def single_file(i):
	wwb = openpyxl.Workbook()
	wsheet = wwb.get_sheet_by_name('Sheet')
	print "opened newbidFile"+str(i)+".xlsx"
	rc = 2
	wsheet['A1'] = 'Date'
	wsheet['B1'] = 'Purchase Bid (MW)'
	wsheet['C1'] = 'Sell Bid (MW)'
	wsheet['D1'] = 'MCV (MW)'
	wsheet['E1'] = 'Cleared Volume (MW)'
	wsheet['F1'] = 'Final Scheduled Volume (MW)'
	wsheet['G1'] = 'MCP (Rs/MWh)'
	for j in range(1,file_count+1):
		owb = openpyxl.load_workbook("BidFile"+str(j)+".xlsx")
		osheet = owb.get_sheet_by_name('MarketMinute')
		# print "file"+str(j)+"opened"
		k=6+i
		max_row = 2886
		if(j<=63):
			if(j==5):
				wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
				wsheet['B'+str(rc)] = osheet['D'+str(k)].value
				wsheet['C'+str(rc)] = osheet['F'+str(k)].value
				wsheet['D'+str(rc)] = osheet['G'+str(k)].value
				wsheet['E'+str(rc)] = osheet['H'+str(k)].value
				wsheet['F'+str(rc)] = osheet['J'+str(k)].value
				wsheet['G'+str(rc)] = osheet['K'+str(k)].value
			# print osheet['Q'+str(k)].value
				rc+=1
				k+=96
				wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
				wsheet['B'+str(rc)] = osheet['D'+str(k)].value
				wsheet['C'+str(rc)] = osheet['F'+str(k)].value
				wsheet['D'+str(rc)] = osheet['G'+str(k)].value
				wsheet['E'+str(rc)] = osheet['H'+str(k)].value
				wsheet['F'+str(rc)] = osheet['J'+str(k)].value
				wsheet['G'+str(rc)] = osheet['K'+str(k)].value
			# print osheet['Q'+str(k)].value
				rc+=1
				k+=96
				wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
				wsheet['B'+str(rc)] = 'Yuvraj'
				wsheet['C'+str(rc)] = 'Yuvraj'
				wsheet['D'+str(rc)] = 'Yuvraj'
				wsheet['E'+str(rc)] = 'Yuvraj'
				wsheet['F'+str(rc)] = 'Yuvraj'
				wsheet['G'+str(rc)] = 'Yuvraj'
				rc+=1
				while(k <= 2790):
					wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
					wsheet['B'+str(rc)] = osheet['D'+str(k)].value
					wsheet['C'+str(rc)] = osheet['F'+str(k)].value
					wsheet['D'+str(rc)] = osheet['G'+str(k)].value
					wsheet['E'+str(rc)] = osheet['H'+str(k)].value
					wsheet['F'+str(rc)] = osheet['J'+str(k)].value
					wsheet['G'+str(rc)] = osheet['K'+str(k)].value
				# print osheet['Q'+str(k)].value
					rc+=1
					k+=96
			else:
				while(k <= max_row):
					wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
					wsheet['B'+str(rc)] = osheet['D'+str(k)].value
					wsheet['C'+str(rc)] = osheet['F'+str(k)].value
					wsheet['D'+str(rc)] = osheet['G'+str(k)].value
					wsheet['E'+str(rc)] = osheet['H'+str(k)].value
					wsheet['F'+str(rc)] = osheet['J'+str(k)].value
					wsheet['G'+str(rc)] = osheet['K'+str(k)].value
				# print osheet['Q'+str(k)].value
					rc+=1
					k+=96
		else:
			while(k <= 486):
				wsheet['A'+str(rc)] = (parse(sdate)+datetime.timedelta(days=rc-2)).strftime('%d/%m/%Y')
				wsheet['B'+str(rc)] = osheet['D'+str(k)].value
				wsheet['C'+str(rc)] = osheet['F'+str(k)].value
				wsheet['D'+str(rc)] = osheet['G'+str(k)].value
				wsheet['E'+str(rc)] = osheet['H'+str(k)].value
				wsheet['F'+str(rc)] = osheet['J'+str(k)].value
				wsheet['G'+str(rc)] = osheet['K'+str(k)].value
			# print osheet['Q'+str(k)].value
				rc+=1
				k+=96
	print "saving newbidFile"+str(i)+".xlsx......."
	wwb.save('newbidFile'+str(i)+'.xlsx')
# file_count = 64
# downloading files for data of electricity prices within the date range
file_count = download_files()
# creating new files for each 15 minute block from the downloaded dataMercad
# for i in range(1,97):
# 	single_file(i)
