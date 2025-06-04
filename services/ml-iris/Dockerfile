FROM python:3.12-slim AS base
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM base AS testing
COPY ./requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r requirements-dev.txt
ENV MLMODEL_URI=ommited-in-unit-testing
ENV MLMODELS_DIR=ommited-in-unit-testing
COPY . .
CMD ["pytest", "-q", "--tb=short", "--disable-warnings"]


FROM base AS service
ENV MLMODELS_DIR=/models
ENV PYTHONPATH=/app
COPY src/ .
CMD ["fastapi", "run", "/app/app.py", "--port", "80"]
