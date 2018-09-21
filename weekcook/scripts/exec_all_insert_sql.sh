#!/bin/bash

ls | grep -v $0 | while read f
do
    psql -c "\i ${f}" --username=postgres --dbname=postgres
done

