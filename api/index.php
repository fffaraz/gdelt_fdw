<?php
set_time_limit(0);
ob_end_flush();
for ($i=0; $i < 1000000; $i++)
{
	for ($j=0; $j < 58; $j++)
	{
		echo $j . "\t";
	}
	echo "\n";
	flush();
}
