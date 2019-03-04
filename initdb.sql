CREATE EXTENSION multicorn;

CREATE SERVER csv_srv foreign data wrapper multicorn options (
  wrapper 'multicorn.csvfdw.CsvFdw'
);

CREATE FOREIGN TABLE csvtest (
  year numeric,
  make character varying,
  model character varying,
  length numeric
) server csv_srv options (
  filename '/data/test.csv',
  skip_header '1',
  delimiter ','
);

CREATE SERVER myfdw_srv foreign data wrapper multicorn options (
  wrapper 'myfdw.ConstantForeignDataWrapper'
);

CREATE FOREIGN TABLE constanttable (
    test character varying,
    test2 character varying
) server myfdw_srv;
