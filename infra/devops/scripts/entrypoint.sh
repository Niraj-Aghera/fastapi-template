#!/bin/bash
set -e

# Show debug information
echo "🔍 Environment validation..."

# Check for essential environment variables
if [ -z "$POSTGRES_DATABASE_USERNAME" ] || [ -z "$POSTGRES_DATABASE_PASSWORD" ] || [ -z "$POSTGRES_DATABASE_NAME" ]; then
  echo "❌ ERROR: Required database environment variables are not set"
  echo "Required variables: POSTGRES_DATABASE_USERNAME, POSTGRES_DATABASE_PASSWORD, POSTGRES_DATABASE_NAME"
  exit 1
fi

# Start the application
echo "🚀 Starting Fastapi template..."
exec python -m main
