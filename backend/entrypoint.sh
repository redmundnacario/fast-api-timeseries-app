#!/bin/sh

alembic upgrade head

python seeder.py

uvicorn main:app --host 0.0.0.0 --port 8000