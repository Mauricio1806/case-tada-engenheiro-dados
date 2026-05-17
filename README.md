# Case TaDa — Data Engineer

Pipeline Lakehouse em Azure Databricks com arquitetura Medallion.

## Estrutura

- `gen_orders.py` — gerador de dados sintéticos
- `data/` — CSVs gerados (origem simulada)
- `notebooks/` — notebooks PySpark do pipeline
  - `01_bronze.ipynb` — ingestão raw
  - `02_silver.ipynb` — limpeza, dedup, quality gates
  - `03_gold.ipynb` — modelagem dimensional Kimball
  - `04_queries_bi.ipynb` — queries de negócio
- `sql/00_ddl_origem.sql` — DDL do banco transacional

## Como executar

1. Rodar `python gen_orders.py` localmente
2. Subir os CSVs no Azure Blob Storage
3. Importar notebooks no Databricks e executar em ordem