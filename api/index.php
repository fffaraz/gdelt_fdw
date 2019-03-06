<?php
set_time_limit(0);
ob_end_flush();

$sqldate = '20190305';
$filename = '/data/' . $sqldate . '.export.CSV.zip';
if(!file_exists($filename)) file_put_contents($filename, fopen('http://data.gdeltproject.org/events/' . $sqldate . '.export.CSV.zip', 'r'));
$zip = zip_open($filename);
if($zip)
{
	$zip_entry = zip_read($zip)
	if(zip_entry_open($zip, $zip_entry, 'r'))
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
