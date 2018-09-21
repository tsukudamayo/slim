#!/bin/bash

cat all_table.txt | while read f
do
    psql -c "\COPY $f TO ../csv/$f.csv WITH CSV HEADER DELIMITER ',';" --username=postgres --dbname=postgres
done

