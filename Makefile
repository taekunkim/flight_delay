docker-build:
	docker compose build  --no-cache

# Start containers
docker-up:
	docker compose up -d

# Stop and remove containers
docker-down:
	docker compose down

# run through the entire ETL scripts
data:
	docker compose exec python_data python main.py

# Set the alembic base command with custom config path
alembic_cmd = docker-compose exec python_data alembic -c ./db/alembic.ini

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






