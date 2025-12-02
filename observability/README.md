# Observabilidade

Este diretório documenta a configuração de observabilidade:

- Prometheus coleta métricas dos endpoints `/metrics` dos serviços.
- Grafana consome Prometheus para dashboards.
- Loki recebe logs estruturados.

Sugestão:
- Implantar Prometheus, Grafana e Loki via Helm charts.
- Adicionar os serviços `catalog-service`, `order-service` e `worker-service` como scrape targets.
