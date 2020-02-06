<?php

function zipFileErrMsg($errno) {
  // using constant name as a string to make this function PHP4 compatible
  $zipFileFunctionsErrors = array(
    'ZIPARCHIVE::ER_MULTIDISK' => 'Multi-disk zip archives not supported.',
    'ZIPARCHIVE::ER_RENAME' => 'Renaming temporary file failed.',
    'ZIPARCHIVE::ER_CLOSE' => 'Closing zip archive failed',
    'ZIPARCHIVE::ER_SEEK' => 'Seek error',
    'ZIPARCHIVE::ER_READ' => 'Read error',
    'ZIPARCHIVE::ER_WRITE' => 'Write error',
    'ZIPARCHIVE::ER_CRC' => 'CRC error',
    'ZIPARCHIVE::ER_ZIPCLOSED' => 'Containing zip archive was closed',
    'ZIPARCHIVE::ER_NOENT' => 'No such file.',
    'ZIPARCHIVE::ER_EXISTS' => 'File already exists',
    'ZIPARCHIVE::ER_OPEN' => 'Can\'t open file',
    'ZIPARCHIVE::ER_TMPOPEN' => 'Failure to create temporary file.',
    'ZIPARCHIVE::ER_ZLIB' => 'Zlib error',
    'ZIPARCHIVE::ER_MEMORY' => 'Memory allocation failure',
    'ZIPARCHIVE::ER_CHANGED' => 'Entry has been changed',
    'ZIPARCHIVE::ER_COMPNOTSUPP' => 'Compression method not supported.',
    'ZIPARCHIVE::ER_EOF' => 'Premature EOF',
    'ZIPARCHIVE::ER_INVAL' => 'Invalid argument',
    'ZIPARCHIVE::ER_NOZIP' => 'Not a zip archive',
    'ZIPARCHIVE::ER_INTERNAL' => 'Internal error',
    'ZIPARCHIVE::ER_INCONS' => 'Zip archive inconsistent',
    'ZIPARCHIVE::ER_REMOVE' => 'Can\'t remove file',
    'ZIPARCHIVE::ER_DELETED' => 'Entry has been deleted',
  );
  $errmsg = 'unknown';
  foreach ($zipFileFunctionsErrors as $constName => $errorMessage) {
    if (defined($constName) and constant($constName) === $errno) {
      return 'Zip File Function error: '.$errorMessage;
    }
  }
  return 'Zip File Function error: unknown';
}

function parseQuery($input)
{
	$result = [];

	$result['method'] = $input['method'];

	$result['options'] = json_decode(str_replace('\'', '"', $input['options']), true);
	$result['url'] = $result['options']['url'];
	$result['table'] = $result['options']['table'];

	$all_columns = $input['all_columns'];
	$all_columns = substr($all_columns, strlen('OrderedDict(['));
	$all_columns = substr($all_columns, 0, -2); // ])
	$all_columns = explode('), ', $all_columns);
	$all_columns2 = [];
	foreach ($all_columns as $value)
	{
		$value = substr($value, 1);
		$value = substr($value, 0, -1);
		$value = explode(', ColumnDefinition(', $value);
		$value = substr($value[1], 0, -1);
		$value = explode(', ', $value);
		$obj = [];
		$obj['name'] = $value[0];
		$obj['type'] = $value[2];
		$all_columns2[] = $obj;
	}
	$result['all_columns'] = $all_columns2;

	$query_columns = $input['query_columns'];
	$query_columns = substr($query_columns, strlen('set('));
	$query_columns = substr($query_columns, 0, -1); // )
	$result['query_columns'] = json_decode(str_replace('\'', '"', $query_columns), true);

	$quals = $input['quals'];
	$quals = substr($quals, 1);
	$quals = substr($quals, 0, -1);
	$quals = explode(', ', $quals);
	$result['quals'] = $quals;

	return $result;
}

function test($query)
{
	for($i = 1; $i <= 100; $i++)
	{
		$sample = $i . "\t";
		for($j = 2; $j <= count($query['all_columns']); $j++) $sample .= rand(1, 100) . "\t";
		echo(trim($sample) . "\n");
	}
	die();
}

function parseFile($filename)
{
	$zip = zip_open($filename);
	if(!is_resource($zip))
	{
		file_put_contents('/app/data/error.log', zipFileErrMsg($zip) . "\n---\n", FILE_APPEND | LOCK_EX);
		return;
	}
	$zip_entry = zip_read($zip);
	if($zip_entry && zip_entry_open($zip, $zip_entry, 'r'))
	{
		$buffer = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));
		zip_entry_close($zip_entry);
		$lines = explode("\r\n", $buffer);
		foreach($lines as $line)
		{
			$csv = str_getcsv($line, "\t");
			foreach($csv as $field)
			{
				echo $field . "\t";
			}
			echo "\n";
			flush();
		}
	}
	zip_close($zip);
}

function parseDate($dateadded)
{
	$filename = '/app/data/' . $dateadded . '.export.CSV.zip';
	if(!file_exists($filename)) file_put_contents($filename, fopen('http://data.gdeltproject.org/events/' . $dateadded . '.export.CSV.zip', 'r'));
	return parseFile($filename);
}

function parseAll()
{
	// $dateadded = substr($filename, 6, -15);
	foreach(glob('/app/data/*.export.CSV.zip') as $filename) parseFile($filename);
}
