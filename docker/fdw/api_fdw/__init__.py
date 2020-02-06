from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
from logging import ERROR, WARNING

import codecs
import csv
import urllib.parse
import urllib.request

class ApiForeignDataWrapper(ForeignDataWrapper):

	def __init__(self, options, columns):
		super(ApiForeignDataWrapper, self).__init__(options, columns)
		self.options = options
		self.columns = columns
		self.url = options['url']
		self.table = options['table']

	def execute(self, quals, columns):
		data = {'method': 'execute', 'url': self.url, 'table': self.table, 'options': self.options, 'all_columns': self.columns, 'quals': quals, 'query_columns': columns}
		url = self.url + '?' + urllib.parse.urlencode(data)
		for row in csv.reader(codecs.iterdecode(urllib.request.urlopen(url), 'utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
			yield [field if field != '' else None for field in row]
