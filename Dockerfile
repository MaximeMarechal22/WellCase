FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm ci
COPY frontend ./frontend
RUN cd frontend && npm run build

FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt
COPY backend ./backend
COPY --from=frontend-build /app/frontend/build ./frontend/build
ENV PORT=10000
EXPOSE 10000
CMD ["sh","-c","cd backend && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
