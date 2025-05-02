install-backend:
	chmod +x backend/install.sh
	chmod +x backend/run.sh
	cd backend && ./install.sh

install-frontend:
	chmod +x frontend/install.sh
	chmod +x frontend/run.sh
	cd frontend && ./install.sh

install: install-backend install-frontend

run-backend:
	cd /Users/agents/Desktop/mcp-cli/backend && chmod +x run.sh && ./run.sh

run-frontend:
	cd frontend && ./run.sh

.DEFAULT_GOAL := install
