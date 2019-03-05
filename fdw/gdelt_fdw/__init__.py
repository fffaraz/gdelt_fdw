from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import csv
import gzip

class GdeltForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(GdeltForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns

	def execute(self, quals, columns):
		# http://data.gdeltproject.org/events/index.html
		# https://github.com/dialogbox/py_csvgz_fdw
		with gzip.open('/data/20190303.export.CSV.zip', 'rt') as stream:
			reader = csv.reader(stream, delimiter='\t')
			for line in reader:
				yield line;
