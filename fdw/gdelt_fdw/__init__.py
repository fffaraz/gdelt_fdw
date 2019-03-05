from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import csv
import datetime
import glob
import os.path
import urllib
import zipfile

class GdeltForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(GdeltForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns

	def download(self, sqldate):
		strdate = sqldate.strftime('%Y%m%d')
		filename = '/data/' + strdate + '.export.CSV.zip'
		if not os.path.exists(filename):
			url = 'http://data.gdeltproject.org/events/' + strdate+ '.export.CSV.zip'
			urllib.urlretrieve(url, filename)
			if os.path.getsize(filename) < 1:
				os.remove(filename)
				return ''
		return filename

	def execute(self, quals, columns):
		mindate = datetime.datetime.strptime('20130401', '%Y%m%d')
		maxdate = datetime.datetime.now() - datetime.timedelta(days = 1)
		startdate = mindate
		enddate = maxdate
		checkrange = False
		filedates = []
		for qual in quals:
			if qual.field_name == 'sqldate':
				if qual.operator == '=':
					filedates.append(datetime.datetime.strptime(str(qual.value), '%Y%m%d'))
				if qual.operator == '>':
					checkrange = True
					testdate = datetime.datetime.strptime(str(qual.value), '%Y%m%d')
					if startdate < testdate:
						startdate = testdate
				if qual.operator == '<':
					checkrange = True
					testdate = datetime.datetime.strptime(str(qual.value), '%Y%m%d')
					if enddate > testdate:
						enddate = testdate
		if checkrange:
			delta = enddate - startdate
			for d in range(delta.days + 1):
				filedates.append(startdate + datetime.timedelta(d))
		##files = glob.glob('/data/*.export.CSV.zip')
		for filedate in list(set(filedates)):
			filepath = self.download(filedate)
			if len(filepath) > 0:
				with zipfile.ZipFile(filepath) as myzip:
					with myzip.open(filepath[6:-4]) as stream:
						reader = csv.reader(stream, delimiter='\t')
						for line in reader:
							yield line;
