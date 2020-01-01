#!/bin/bash
set -e

# jobテーブルがあるか確認
#until python -c "import MySQLdb; c=MySQLdb.connect(user='root', host='mysql', db='airflow').cursor();c.execute('SELECT 1 FROM job');c.execute('SELECT 1 FROM task_instance')"; do
until nc -vz dbinit 10000 || nc -vz dbinit 20000; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 5
done

>&2 echo "MySQL is up - executing command"
cmd="$*"
exec $cmd