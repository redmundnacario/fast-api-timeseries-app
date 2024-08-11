#!/bin/sh

export PYTHONPATH=$(pwd)

python db/reset_db.py

alembic upgrade head

python db/seed_db.py

uvicorn main:app --host 0.0.0.0 --port 8000