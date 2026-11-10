.PHONY: sync serve check build
sync:
	uv sync --locked
serve:
	uv run --locked mkdocs serve --dev-addr 127.0.0.1:8000
check build:
	uv run --locked mkdocs build --strict
