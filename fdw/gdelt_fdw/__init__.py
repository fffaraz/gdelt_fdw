from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
from datetime import datetime, timedelta
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

	def execute(self, quals, columns):
		yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
		lastday = yesterday.strftime('%Y%m%d')
		lastdayfile = '/data/' + lastday + '.export.CSV.zip'
		if not os.path.exists(lastdayfile):
			url = 'http://data.gdeltproject.org/events/' + lastday + '.export.CSV.zip'
			urllib.urlretrieve(url, lastdayfile)
		files = glob.glob('/data/*.export.CSV.zip')
		for filename in files:
			with zipfile.ZipFile(filename) as myzip:
				with myzip.open(filename[6:-4]) as stream:
					reader = csv.reader(stream, delimiter='\t')
					for line in reader:
						yield line;
