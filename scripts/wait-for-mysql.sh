#!/bin/bash
set -e

until python -c "import MySQLdb; MySQLdb.connect(user='root', host='mysql', db='airflow')"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $@