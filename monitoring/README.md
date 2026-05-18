# Monitoring Stack — Grafana + Postgres

Stack de observabilidade pro pipeline. Grafana lê de uma tabela `pipeline_runs`
no Postgres alimentada pelo notebook `00_audit_log` do Databricks.

## Subir local

```bash
cd monitoring
docker-compose up -d
```

- Grafana: http://localhost:3000 (admin / cervejaria2025)
- Postgres: localhost:5432 (metrics / metrics)

Dashboard `Pipeline Cervejaria — Saúde Operacional` provisionado automaticamente
com 30 dias de dados sintéticos pra demonstração.

## Em produção

- Postgres seria Azure Database for PostgreSQL
- Grafana seria Azure Managed Grafana
- Audit log sync: notebook `00_audit_log` escreve no Postgres via JDBC depois
  de cada execução do pipeline (ou via Databricks SQL Connector)

## Métricas monitoradas

| Painel | O que mostra |
|---|---|
| Taxa de Sucesso (24h) | % de runs SUCCESS |
| Duração Média (24h) | Latência média end-to-end |
| Falhas (24h) | Contador de runs FAILED |
| Linhas Processadas (24h) | Throughput total |
| Duração por Camada | Time series — detecta degradação |
| Volume por Camada | Time series — detecta queda de volume |
| Histórico (audit table) | Últimas 50 execuções com detalhe |

## Alertas (em prod)

```sql
-- Taxa de falha > 5% em 1h: SLO breach
SELECT 100.0 * COUNT(*) FILTER (WHERE status = 'FAILED') / COUNT(*)
FROM pipeline_runs
WHERE started_at > NOW() - INTERVAL '1 hour';

-- Latência p95 > SLA: lentidão
SELECT percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_seconds)
FROM pipeline_runs
WHERE layer = 'gold' AND started_at > NOW() - INTERVAL '1 hour';
```

Alertas via Grafana Alerting → PagerDuty / Slack / Email.