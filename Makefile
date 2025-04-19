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
	docker-compose exec python_data pytest

# Run the main script
run:
	docker-compose exec python_data python main.py

# Start containers
up:
	docker-compose up -d

# Stop and remove containers
down:
	docker-compose down
