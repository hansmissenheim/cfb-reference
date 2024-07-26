#! /usr/bin/env bash
echo "Running prestart..."

# Run migrations
alembic upgrade head
