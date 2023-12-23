# Use the official Python image as the base image
FROM python:3.10
LABEL org.opencontainers.image.source=https://github.com/Borghese-Gladiator/bank-flask-app
LABEL org.opencontainers.image.description="Flask bank app based off Code Signal problem"
LABEL org.opencontainers.image.licenses=MIT

# Set environment variables
ENV POETRY_NO_INTERACTION 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1
ENV POETRY_VIRTUALENVS_CREATE 1
ENV POETRY_CACHE_DIR /tmp/poetry_cache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry==1.6.1

# Set working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install project dependencies using Poetry
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Copy the Flask project files to the container
COPY . /app/

# Install your project in virtual envrionment (useful for installing any custom script)
RUN poetry install --without dev

# Expose the default port the Flask app runs on
EXPOSE 5000

# Run the Flask server
ENTRYPOINT ["poetry", "run", "python", "app.py"]

## Run the Waitress production server
## ENTRYPOINT ["waitress-serve", "--call", "'flaskr:create_app'"]
