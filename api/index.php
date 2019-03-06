<?php
ob_end_flush();
ob_end_clean();
ob_implicit_flush();
for ($i=0; $i < 1000000; $i++)
{
	for ($j=0; $j < 58; $j++)
	{
		echo $j . "\t";
	}
	echo "\n";
	flush();
}
