#!/bin/sh
pg_dump -U kalkinine torildb | gzip > torildb.`date +"%Y-%m-%d"`.sql.gz
#restore: gunzip -c torildb.`date +"%Y-%m-%d"`.sql.gz | psql -U kalkinine -d torildb
