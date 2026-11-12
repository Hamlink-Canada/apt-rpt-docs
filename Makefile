.PHONY: sync serve check build
sync:
	uv sync --locked
serve:
	uv run --locked zensical serve --dev-addr 127.0.0.1:8000
check build:
	uv run --locked zensical build --strict
