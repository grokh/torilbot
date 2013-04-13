#!/bin/sh
pg_dump -U kalkinine torildb | gzip > torildb.`date +"%Y-%m-%d"`.sql.gz
