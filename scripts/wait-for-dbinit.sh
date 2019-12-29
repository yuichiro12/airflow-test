#!/bin/bash
set -e

# jobテーブルがあるか確認
until python -c "import MySQLdb; MySQLdb.connect(user='root', host='mysql', db='airflow').cursor().execute('SELECT 1 FROM job')"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $@