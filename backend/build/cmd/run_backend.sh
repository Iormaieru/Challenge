#!/bin/bash

if [ -z "$ENV" ]; then
  ENV="local"
fi

CONFIG="config.settings.${ENV}"

# Function to run migrations
run_migrations_dev() {
  echo "Running migrations..."
  python manage.py makemigrations
  python manage.py migrate --no-input
  echo "Migrations complete"
}

run_migrations() {
  bash /backend/build/cmd/wait-for.sh db:5432 -- echo "DB is up"
  echo "Running migrations..."
  python manage.py makemigrations
  python manage.py migrate --no-input
  echo "Migrations complete"
}

# Function to start the Django server
start_server_dev() {
  echo "Starting Django local server..."
  python manage.py runserver &
  echo "Django local server started"
}

start_server() {
  bash /backend/build/cmd/wait-for.sh db:5432 -- echo "DB is up"
  echo "Starting Django development server..."
  gunicorn core.wsgi:application --bind "0.0.0.0:${PORT}" &
  echo "Django development server started"
}

# Main execution flow
if [ "$ENV" = "local" ]; then
  run_migrations_dev
else
  run_migrations
fi

if [ "$ENV" = "local" ]; then
  start_server_dev
else
  start_server
fi

tail -f /dev/null
