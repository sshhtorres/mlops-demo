FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:0.7.12-alpine /usr/local/bin/ /bin/
WORKDIR /app
COPY .python-version pyproject.toml uv.lock .
RUN uv sync --locked --no-cache --no-dev
COPY . .
CMD ["uv", "run", "streamlit", "run", "src/app.py"]
