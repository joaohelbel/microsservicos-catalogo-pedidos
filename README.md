# Catálogo e pedidos em microsserviços

Sistema de catálogo de produtos e pedidos dividido em microsserviços, empacotado em contêineres e orquestrado com Kubernetes. Fiz como projeto semestral da disciplina de DevOps na ESPM, com foco em escalar, observar e entregar o sistema automaticamente, mais do que nas regras de negócio.

## Como funciona

```
  navegador
      │
┌─────▼──────────────────────────────┐
│ frontend (React + Vite, em NGINX)  │  /api/catalog → catálogo
│                                    │  /api/orders  → pedidos
└──────┬──────────────────┬──────────┘
       │                  │
┌──────▼─────────┐  ┌─────▼──────────┐
│ catalog-service│  │ order-service  │  FastAPI
│ CRUD produtos  │  │ cria pedidos   │
└──────┬─────────┘  └─────┬──────────┘
       │                  │ LPUSH na fila "orders"
┌──────▼─────┐      ┌─────▼─────┐     ┌────────────────┐
│ PostgreSQL │      │   Redis   │◀────│ worker-service │  consome a fila (BRPOP)
└────────────┘      └───────────┘     └────────────────┘
```

- **catalog-service**: CRUD de produtos com FastAPI, SQLAlchemy e PostgreSQL.
- **order-service**: recebe o pedido e publica numa fila do Redis, sem esperar o processamento.
- **worker-service**: consome a fila e processa os pedidos em segundo plano.
- **frontend**: interface em React + Vite, servida por um NGINX que também faz o proxy das chamadas de API.
- **api-gateway**: configuração de NGINX como gateway avulso, roteando `/catalog` e `/orders`.

Catálogo e pedidos expõem `/health` e `/metrics` (Prometheus), com contador de requisições e histograma de latência. O worker expõe as métricas dele na porta 9100.

## O que tem de DevOps

- **Docker**: um Dockerfile por serviço e `docker-compose.yml` para subir tudo localmente.
- **Kubernetes** (`k8s/`): namespace, Deployments, Services, Ingress, ConfigMap e Secret, readiness e liveness probes, RBAC, PodDisruptionBudget e HorizontalPodAutoscaler no catálogo (2 a 6 réplicas, alvo de 60% de CPU).
- **CI/CD** (`.github/workflows/ci-cd.yml`): a cada push na `main`, builda as imagens, publica no GitHub Container Registry e aplica os manifests no cluster.
- **Observabilidade** (`observability/`): os serviços expõem métricas no formato do Prometheus, e a pasta documenta como plugar Prometheus, Grafana e Loki.

O relatório técnico completo, com decisões de arquitetura, testes de carga e análise de custo, está em `docs/relatorio-tecnico.md`.

## Rodar localmente

Precisa de Docker e Docker Compose.

```bash
docker compose up --build
```

| O quê | Endereço |
|---|---|
| Catálogo (Swagger) | http://localhost:8001/docs |
| Pedidos (Swagger) | http://localhost:8002/docs |
| Frontend | http://localhost:3000 |

Exemplo de pedido:

```bash
curl -X POST http://localhost:8002/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

O log do `worker-service` mostra o pedido sendo processado.

## Rodar no Kubernetes

Com um cluster local (Minikube, kind) e as imagens disponíveis:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
kubectl get pods -n catalog-orders
```

## Stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Redis, React, Vite, NGINX, Docker, Kubernetes, GitHub Actions e Prometheus.
