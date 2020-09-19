echo "Making migrations"
python manage.py makemigrations

echo "Migrating"
python manage.py migrate

echo "Loading fixtures"
python manage.py loaddata json_final/data.json

echo "Running server"
python manage.py runserver