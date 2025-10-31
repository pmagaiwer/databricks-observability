# 🚀 Observabilidade no Databricks – Projeto Completo

Monitore e aumente a **confiabilidade, performance e custo** dos jobs e clusters Databricks com **Prometheus + Grafana + Alertmanager**.  
Este projeto demonstra como aplicar **observabilidade e práticas SRE** em um ambiente **Data Lake / Big Data** baseado em **Databricks + AWS**.

---

## 🧠 Conceito – O que é o Databricks?

O **Databricks** é uma plataforma unificada de análise de dados e IA construída sobre o **Apache Spark**, que permite:
- Criar pipelines de dados escaláveis (ETL/ELT);
- Treinar e servir modelos de machine learning;
- Analisar dados em larga escala em **Data Lakes (Lakehouse Architecture)**;
- Integrar com AWS, Azure e GCP.

Ele combina **Data Engineering + Data Science + Analytics** em um único ambiente colaborativo, com notebooks, jobs e clusters gerenciados.

---

## 🔍 Observabilidade no Databricks

A observabilidade permite **entender o comportamento interno do sistema** a partir de logs, métricas e traces.  
No contexto Databricks, isso significa:

| Tipo | Exemplos | Ferramentas |
|------|-----------|-------------|
| 📈 Métricas | Jobs concluídos, duração média, custo do cluster | Prometheus + Exporters |
| 📜 Logs | Execuções, erros Spark, logs de driver/executor | CloudWatch Logs, Log Analytics |
| 🔎 Traces | Latência de pipelines, dependências ETL | OpenTelemetry, Datadog APM |

### 🔗 Integração de Observabilidade

1. **Databricks Exporter (custom Python)** coleta métricas via API REST (jobs, clusters, runs).  
2. **Prometheus** armazena as métricas.  
3. **Grafana** visualiza os SLIs/SLOs.  
4. **Alertmanager** dispara alertas proativos (ex: job falhando, latência alta).  

---

## 🧱 Estrutura do Projeto

```
databricks-observability/
├── dashboards/
│   └── grafana-databricks-dashboard.json
├── exporters/
│   └── databricks-metrics-exporter.py
├── slo/
│   └── databricks-slo.yaml
├── alerts/
│   └── alertmanager-rules.yaml
├── docs/
│   └── architecture_overview.md
└── README.md
```

---

## 🧩 Visão Geral do Dashboard

**Nome:** 🧩 Databricks Reliability – Jobs & Clusters  
**Objetivo:** Monitorar confiabilidade, performance e custo dos jobs e clusters Databricks.

### 📍 Painéis principais

- Visão geral de confiabilidade (SLI/SLO geral)  
- Databricks Jobs – sucesso e duração  
- Clusters – performance, custo e uso de recursos  
- Alertas e falhas recentes  

---

## 📊 Estrutura do Dashboard (visão hierárquica)

```
📊 Databricks Reliability Dashboard
├── 1️⃣ Overview
│   ├── SLI: % de jobs concluídos
│   ├── SLI: Tempo médio de execução (P95)
│   └── SLO: 99% jobs completando < 15min
├── 2️⃣ Databricks Jobs
│   ├── Painel: Taxa de sucesso dos jobs
│   ├── Painel: Duração média dos jobs
│   ├── Painel: Falhas por tipo
│   └── Painel: Tempo de fila/execução
├── 3️⃣ Clusters
│   ├── Painel: Uso de CPU e memória
│   ├── Painel: Tempo de inicialização
│   ├── Painel: Custo estimado
│   └── Painel: Capacidade ociosa
└── 4️⃣ Alertas e Logs
    ├── Painel: Alertas críticos (Alertmanager)
    └── Painel: Últimos logs de falha (CloudWatch)
```

---

## 🧮 Exemplo de Métricas e Consultas (PromQL)

### 🔹 Jobs Databricks

| Métrica | Descrição | Fonte | SLI | SLO |
|----------|------------|--------|------|------|
| `databricks_job_run_success_total` | Total de execuções bem-sucedidas | Exporter | % sucesso = sucesso / total | ≥ 99% |
| `databricks_job_run_duration_seconds` | Duração média dos jobs | Exporter | P95 < 900s | ≤ 15 min |
| `databricks_job_run_failed_total` | Total de falhas | Exporter | — | — |

**Consultas PromQL simuladas:**

```promql
# SLI 1: Taxa de sucesso dos jobs (7d)
(sum(increase(databricks_job_run_success_total[7d])) 
 / sum(increase(databricks_job_run_started_total[7d]))) * 100

# SLI 2: Duração média (15min window)
avg_over_time(databricks_job_run_duration_seconds[15m])
```

---

### 🔹 Clusters Databricks

| Métrica | Descrição | Fonte | SLI | SLO |
|----------|------------|--------|------|------|
| `databricks_cluster_cpu_utilization` | Uso médio de CPU por cluster | Exporter | < 80% | — |
| `databricks_cluster_memory_usage` | Uso médio de memória | Exporter | < 85% | — |
| `databricks_cluster_cost_estimated` | Custo estimado (USD/h) | Exporter | — | — |

```promql
# Latência média (P95)
histogram_quantile(0.95, sum(rate(databricks_job_run_duration_seconds_bucket[5m])) by (le))
```

---

## 🧮 Exemplo de Definição de SLO (YAML)

```yaml
service: "databricks-pipelines"
indicators:
  - name: "job_success_rate"
    metric_query: |
      (sum(increase(databricks_job_run_success_total[30d])) 
       / sum(increase(databricks_job_run_started_total[30d]))) * 100
    target: 99.0
    alert:
      warning: "< 99"
      critical: "< 98"
  - name: "job_duration_p95"
    metric_query: |
      histogram_quantile(0.95, sum(rate(databricks_job_run_duration_seconds_bucket[5m])) by (le))
    target: 900
    alert:
      warning: "> 900"
      critical: "> 1200"
```

---

## ⚙️ Passo a Passo – Execução Local

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/databricks-observability.git
cd databricks-observability
```

### 2️⃣ Criar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configurar variáveis de ambiente

```bash
export DATABRICKS_HOST="https://<seu-workspace>.cloud.databricks.com"
export DATABRICKS_TOKEN="<seu-token-api>"
```

### 4️⃣ Executar o Exporter

```bash
python exporters/databricks-metrics-exporter.py
```

O serviço ficará disponível em `http://localhost:9101/metrics` para coleta pelo Prometheus.

---

### 5️⃣ Configurar Prometheus

Adicione ao seu `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "databricks"
    static_configs:
      - targets: ["localhost:9101"]
```

### 6️⃣ Importar o Dashboard no Grafana

- Acesse **Grafana → Dashboards → Import**
- Cole o conteúdo de `dashboards/grafana-databricks-dashboard.json`
- Conecte à fonte de dados Prometheus (`http://localhost:9090`)

---

### 7️⃣ Configurar Alertmanager (opcional)

Adicione em `alertmanager.yml`:

```yaml
route:
  receiver: 'slack'
receivers:
  - name: 'slack'
    slack_configs:
      - send_resolved: true
        channel: '#alerts'
        username: 'AlertBot'
        text: '{{ .CommonAnnotations.summary }}'
```

---

## 📈 Exemplo Visual (conceitual)

```
🟢 Job Success Rate (SLI)
▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  99.3%

🕐 Job Duration (P95)
▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  870s

🔥 Cluster CPU Utilization
▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  72%

💸 Cost Trend (USD/dia)
💹 line chart showing EC2 + Databricks compute cost

⚠️ Recent Incidents
Job “etl_customer_data” failed @ 2025-10-31T08:45
```

---

## 🚀 Nota Pessoal

> “Eu implementaria observabilidade completa no Databricks com Prometheus e Grafana, monitorando SLIs e SLOs como taxa de sucesso e latência P95 dos jobs.  
> As métricas seriam expostas via exporter customizado, correlacionadas com custo e uso de clusters, para detectar gargalos antes de afetar o negócio.”

---

## 📚 Créditos e Inspiração

- [Databricks REST API](https://docs.databricks.com/api)
- [Prometheus Exporters](https://prometheus.io/docs/instrumenting/exporters/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards)
- [Alertmanager Rules](https://prometheus.io/docs/alerting/latest/alertmanager/)

---

## 🧩 Licença
MIT License © 2025 [Pierre Santos](https://github.com/pmagaiwer/)
📍 Projeto pessoal para fins de estudo e demonstração de práticas SRE em Data Lake/Big Data.
