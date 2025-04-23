# Set the alembic base command with custom config path
alembic_cmd = docker-compose exec python_data alembic -c db/alembic.ini

# Run migrations (upgrades the DB to latest schema)
alembic_migrate:
	@echo "⏫ Upgrading to latest schema..."
	$(alembic_cmd) upgrade head

# Create a new revision with autogeneration
alembic_revision:
	@read -p "Enter migration message: " msg; \
	$(alembic_cmd) revision --autogenerate -m "$$msg"

# Downgrade one revision
alembic_downgrade:
	@echo "⏬ Downgrading one revision..."
	$(alembic_cmd) downgrade -1

# Show current migration status
alembic_current:
	$(alembic_cmd) current

# Show full migration history
alembic_history:
	$(alembic_cmd) history

# Run tests inside container
test:
	docker compose exec python_data pytest

# Run the main script
run:
	docker compose exec python_data python main.py

# Start containers
docker-up:
	docker compose up -d

docker-airflow-up:
	docker compose -f docker-compose.airflow.yml up -d

# Stop and remove containers
docker-down:
	docker compose down

docker-airflow-down:
	docker compose -f airflow/docker-compose.airflow.yml down

init-airflow:
	docker compose -f airflow/docker-compose.airflow.yml run --rm webserver airflow db init
	docker compose -f airflow/docker-compose.airflow.yml run --rm webserver airflow users create \
		--username airflow \
		--password airflow \
		--firstname Air \
		--lastname Flow \
		--role Admin \
		--email airflow@example.com
