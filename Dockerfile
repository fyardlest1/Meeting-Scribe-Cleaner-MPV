FROM python:3.11-slim

# Install system deps (ghostscript + build essentials for pikepdf if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --fix-missing \
        build-essential \
        gcc \
        git \
        libpq-dev \
        pkg-config \
        libcairo2-dev \
        libffi-dev \
        ghostscript \
        ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements & install
# Install requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY .. /app

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONUNBUFFERED=1

CMD ["/entrypoint.sh"]

