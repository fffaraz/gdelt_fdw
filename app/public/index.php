<?php
require_once 'include.php';

// https://github.com/googleapis/google-cloud-php-bigquery
// https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-php

header("Content-Type: text/plain");
ini_set('memory_limit', -1);
set_time_limit(0);
ob_end_flush();

file_put_contents('/app/data/last_request.log', json_encode($_REQUEST, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

$query = [];
$query['method'] = $_REQUEST['method'];
$query['options'] = $_REQUEST['options'];
$query['all_columns'] = $_REQUEST['all_columns'];
$query['query_columns'] = $_REQUEST['query_columns'];
$query['quals'] = $_REQUEST['quals'];
$query = parseQuery($query);

file_put_contents('/app/data/last_query.log', json_encode($query, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

//test($query);

$dates = getDates($query);
foreach ($dates as $date) parseDate($date);

//parseDate(20190911);
