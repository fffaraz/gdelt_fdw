CREATE SERVER csv_srv foreign data wrapper multicorn options (
    wrapper 'multicorn.csvfdw.CsvFdw'
);

create foreign table csvtest (
       year numeric,
       make character varying,
       model character varying,
       length numeric
) server csv_srv options (
       filename '/data/test.csv',
       skip_header '1',
       delimiter ',');
