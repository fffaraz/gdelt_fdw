from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
from logging import ERROR, WARNING

import codecs
import csv
import datetime
import glob
import os.path
import urllib.request
import zipfile

class GdeltForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(GdeltForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns
		self.table = options['table']

	def download(self, dateadded):
		if isinstance(dateadded, datetime.datetime):
			strdate = dateadded.strftime('%Y%m%d')
		else:
			strdate = str(dateadded)

		if(self.table == 'gdeltv2_gkg'):
			filename = '/data/' + strdate + '.gkg.csv.zip'
		else:
			filename = '/data/' + strdate + '.export.CSV.zip'

		if not os.path.exists(filename):
			if(len(strdate) > 8):
				if(self.table == 'gdeltv2_gkg'):
					url = 'http://data.gdeltproject.org/gdeltv2/' + strdate + '.gkg.csv.zip'
				else:
					url = 'http://data.gdeltproject.org/gdeltv2/' + strdate + '.export.CSV.zip'
			else:
				url = 'http://data.gdeltproject.org/events/' + strdate + '.export.CSV.zip'

			urllib.request.urlretrieve(url, filename)
			os.chmod(filename, 0o666)

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
			if qual.field_name.lower() == 'dateadded' or qual.field_name.lower() == 'date':
				if qual.list_any_or_all:
					for value in qual.value:
						filedates.append(datetime.datetime.strptime(str(value), '%Y%m%d'))
					continue
				if qual.operator == '=' or qual.operator == '~~':
					filedates.append(str(qual.value))
					continue
				dateadded = datetime.datetime.strptime(str(qual.value), '%Y%m%d')
				if qual.operator == '>' or qual.operator == '>=':
					checkrange = True
					if mindate < dateadded:
						mindate = dateadded
				if qual.operator == '<' or qual.operator == '<=':
					checkrange = True
					if maxdate > dateadded:
						maxdate = dateadded

		if checkrange:
			delta = maxdate - mindate
			for d in range(delta.days + 1):
				filedates.append(mindate + datetime.timedelta(d))

		#if not filedates:
		#	for file in glob.glob('/data/*.export.CSV.zip'):
		#		filedates.append(file[6:-15])

		log_to_postgres("gdelt_fdw filedates: '%s'" % ', '.join(map(str, filedates)), WARNING)

		for filedate in sorted(list(set(filedates))):
			filepath = self.download(filedate)
			if len(filepath) > 0:
				with zipfile.ZipFile(filepath) as myzip:
					csvname = myzip.namelist()[0];
					with myzip.open(csvname) as stream:
						for row in csv.reader(codecs.iterdecode(stream, 'utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
							yield [self.cleanfield(field) for field in row]
