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

CREATE EXTENSION file_fdw;
CREATE SERVER svr_file FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE fdt_film_locations
  (title text ,
  release_year integer ,
  locations text ,
  fun_facts text ,
  production_company text ,
  distributor text ,
  director text ,
  writer text ,
  actor_1 text ,
  actor_2 text ,
  actor_3 text )
  SERVER svr_file
  OPTIONS (format 'csv', header 'true',
  program '/data/myscript.sh "$@"',
  delimiter ',',
  null ''
);
