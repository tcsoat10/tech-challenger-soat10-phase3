poetry_install_dev:
	poetry install --with test --sync

poetry_install:
	poetry install --sync

build:
	docker compose build

up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

dev:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

migrate_db:
	alembic upgrade head

test_watch:
	ENV=test ptw --runner 'pytest --ff $(extra)'

test_parallel:
	ENV=test pytest --cov=src --numprocesses auto --dist loadfile --max-worker-restart 0 $(extra)

test_coverage_percentage:
	coverage json -q -o /dev/stdout --omit=tests/* | jq .totals.percent_covered

test_coverage:
	coverage report --omit=tests/*
