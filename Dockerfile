FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set working directory first
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy the rest of the project
COPY . .

# Create data directory for SQLite
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Use uv run to execute commands within the virtual environment
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]