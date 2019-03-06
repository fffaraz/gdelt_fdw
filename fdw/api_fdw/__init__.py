from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
import csv
import urllib
import urllib2

class ApiForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(ApiForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns
		self.url = options["url"]

	def execute(self, quals, columns):
		params1 = urllib.urlencode(self.options)
		params2 = 'columns1="' + ','.join([str(x) for x in self.columns]) + '"'
		params3 = 'columns2="' + ','.join([str(x) for x in columns]) + '"'
		params = params1 + '&' + params2 + '&' + params3
		url = self.url + '?' + params
		log_to_postgres(url)
		contents = urllib2.urlopen(url).read()
		reader = csv.reader(contents.splitlines(), delimiter='\t', quoting=csv.QUOTE_NONE)
		for row in reader:
			yield [field if field != '' else None for field in row]
