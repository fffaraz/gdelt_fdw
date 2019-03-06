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
		if isinstance(sqldate, datetime.datetime):
			strdate = sqldate.strftime('%Y%m%d')
		else:
			strdate = str(sqldate)
		filename = '/data/' + strdate + '.export.CSV.zip'
		if not os.path.exists(filename):
			url = 'http://data.gdeltproject.org/events/' + strdate + '.export.CSV.zip'
			urllib.urlretrieve(url, filename)
			if os.path.getsize(filename) < 1:
				os.remove(filename)
				return ''
		return filename

	def cleanfield(self, field):
		if field == '':
			return None
		if len(field) < 6 and field[0].isdigit():
			return field.replace('#', '')
		return field

	def execute(self, quals, columns):
		mindate = datetime.datetime.strptime('20130401', '%Y%m%d')
		maxdate = datetime.datetime.now() - datetime.timedelta(days = 1)
		checkrange = False
		filedates = []
		for qual in quals:
			if qual.field_name == 'sqldate':
				if qual.list_any_or_all:
					for value in qual.value:
						filedates.append(datetime.datetime.strptime(str(value), '%Y%m%d'))
					continue
				sqldate = datetime.datetime.strptime(str(qual.value), '%Y%m%d')
				if qual.operator == '=' or qual.operator == '~~':
					filedates.append(sqldate)
				if qual.operator == '>' or qual.operator == '>=':
					checkrange = True
					if mindate < sqldate:
						mindate = sqldate
				if qual.operator == '<' or qual.operator == '<=':
					checkrange = True
					if maxdate > sqldate:
						maxdate = sqldate

		if checkrange:
			delta = maxdate - mindate
			for d in range(delta.days + 1):
				filedates.append(mindate + datetime.timedelta(d))

		if not filedates:
			files = glob.glob('/data/*.export.CSV.zip')
			for file in files:
				filedates.append(file[6:-15])

		for filedate in list(set(filedates)):
			filepath = self.download(filedate)
			if len(filepath) > 0:
				with zipfile.ZipFile(filepath) as myzip:
					with myzip.open(filepath[6:-4]) as stream:
						reader = csv.reader(stream, delimiter='\t', quoting=csv.QUOTE_NONE)
						for row in reader:
							yield [self.cleanfield(field) for field in row]
