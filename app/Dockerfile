# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /install

COPY requirements.txt .
RUN pip install --user -r requirements.txt


# Stage 2: runtime
FROM python:3.11-slim

RUN useradd -m devuser

WORKDIR /app

COPY --from=builder /root/.local /home/devuser/.local
COPY . .

ENV PATH=/home/devuser/.local/bin:$PATH

USER devuser

EXPOSE 8000

CMD ["python", "app.py"]