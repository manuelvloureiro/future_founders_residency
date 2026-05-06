.PHONY: install dev dev-backend dev-frontend clean

install:
	cd backend && uv sync
	cd frontend && uv sync

dev:
	$(MAKE) dev-backend & $(MAKE) dev-frontend & wait

dev-backend:
	cd backend && uv run uvicorn main:app --reload --port 8000

dev-frontend:
	cd frontend && uv run uvicorn main:app --reload --port 3000

clean:
	rm -rf frontend/.venv frontend/__pycache__ frontend/components/__pycache__
	rm -rf backend/.venv backend/__pycache__
