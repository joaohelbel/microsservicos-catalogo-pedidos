# Sistema de Catálogo & Pedidos em Microserviços

Este repositório implementa um sistema de catálogo e pedidos usando uma arquitetura de microserviços,
contêineres Docker, Kubernetes, CI/CD e observabilidade.

## Serviços

- `catalog-service` - CRUD de produtos (FastAPI + SQLAlchemy + PostgreSQL)
- `order-service` - criação de pedidos, publicação em fila Redis
- `worker-service` - consumidor da fila que processa pedidos
- `frontend` - interface web (React + Vite)
- `api-gateway` - NGINX servindo como gateway/Ingress

## Como rodar em desenvolvimento (Docker Compose)

```bash
docker compose up --build
```

Acesse:
- Catálogo: http://localhost:8001/docs
- Pedidos:  http://localhost:8002/docs
- Frontend: http://localhost:3000
<!--  -->