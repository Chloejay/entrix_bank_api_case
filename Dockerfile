FROM python:3.12.1 as base 

#install Poetry and set environement
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy app files
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction  --no-root

RUN poetry config virtualenvs.in-project false && \
    poetry install --no-interaction --no-root && \
    export POETRY_VENV=$(poetry env info -p) && \
    export PATH="$POETRY_VENV/bin:$PATH"

#Copy app source code
COPY . .

EXPOSE 8082
CMD ["poetry", "run", "uvicorn", "bankAPI.main:app", "--host", "0.0.0.0","--port", "8082"]