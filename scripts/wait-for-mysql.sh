#!/bin/bash
set -e

until python -c "import MySQLdb; MySQLdb.connect(user='root', host='db', db='airflow')"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
#cmd="$*"
#exec $cmd

airflow initdb
nc -lp 10000
nc -lp 20000