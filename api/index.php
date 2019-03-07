<?php
require 'include.php';

// https://github.com/googleapis/google-cloud-php-bigquery
// https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-php

ini_set('memory_limit', -1);
set_time_limit(0);
ob_end_flush();

foreach(glob('/data/*.export.CSV.zip') as $filename)
{
	$sqldate = substr($filename, 6, -15);
	if(!file_exists($filename)) file_put_contents($filename, fopen('http://data.gdeltproject.org/events/' . $sqldate . '.export.CSV.zip', 'r'));
	$zip = zip_open($filename);
	if(is_resource($zip))
	{
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
	//else echo "Error: " . zipFileErrMsg($zip);
}
