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
		self.param1 = urllib.urlencode(self.options)
		self.param2 = 'colstable=' + ','.join(self.columns)

	def execute(self, quals, columns):
		param3 = 'colsquery=' + ','.join(columns)
		param4 = 'quals=' + ','.join([str(qual.field_name) + str(qual.operator) + str(qual.value) for qual in quals])
		params = self.param1 + '&' + self.param2 + '&' + param3 + '&' + param4
		url = self.url + '?method=execute&' + params
		reader = csv.reader(urllib2.urlopen(url), delimiter='\t', quoting=csv.QUOTE_NONE)
		for row in reader:
			yield [field if field != '' else None for field in row]
