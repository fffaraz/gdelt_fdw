from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import csv
import glob
import zipfile

class GdeltForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(GdeltForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns

	def execute(self, quals, columns):
		# http://data.gdeltproject.org/events/index.html
		# https://github.com/dialogbox/py_csvgz_fdw
		for filename in glob.glob('/data/*.export.CSV.zip'):
			with zipfile.ZipFile(filename) as myzip:
				with myzip.open(filename[6:-4]) as stream:
					reader = csv.reader(stream, delimiter='\t')
					for line in reader:
						yield line;
