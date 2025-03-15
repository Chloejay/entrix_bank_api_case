FROM python:3.12.1 as base 

#install Poetry and set environement
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH = "/root/.local/bin:$PATH"

# create app folder
WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-dev
COPY . . 

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0,0,0,0","--port", "8000"]
