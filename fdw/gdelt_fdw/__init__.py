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

	def download(self, strdate):
		filename = '/data/' + strdate + '.export.CSV.zip'
		if not os.path.exists(filename):
			url = 'http://data.gdeltproject.org/events/' + strdate + '.export.CSV.zip'
			urllib.urlretrieve(url, filename)
			if os.path.getsize(filename) < 1:
				os.remove(filename)

	def execute(self, quals, columns):
		for d in xrange(1,10):
			yesterday = datetime.datetime.now() - datetime.timedelta(days = d)
			self.download(yesterday.strftime('%Y%m%d'))
		files = glob.glob('/data/*.export.CSV.zip')
		for filename in files:
			with zipfile.ZipFile(filename) as myzip:
				with myzip.open(filename[6:-4]) as stream:
					reader = csv.reader(stream, delimiter='\t')
					for line in reader:
						yield line;
