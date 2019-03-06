from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import csv
import urllib2

class ApiForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(GdeltForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns
		self.url = options["api"]

	def execute(self, quals, columns):
		contents = urllib2.urlopen(self.url).read()
		reader = csv.reader(contents, delimiter='\t')
		for row in reader:
			yield row
