from prometheus_client import start_http_server, Gauge
import random, time

job_success = Gauge('databricks_job_succeeded_total', 'Total de jobs concluídos com sucesso')
job_started = Gauge('databricks_job_started_total', 'Total de jobs iniciados')
job_duration = Gauge('databricks_job_duration_seconds', 'Tempo de execução dos jobs (segundos)')
cluster_uptime = Gauge('databricks_cluster_uptime_seconds', 'Tempo de uptime dos clusters (segundos)')
cluster_cost = Gauge('databricks_cluster_cost_usd', 'Custo diário estimado (USD)')

if __name__ == "__main__":
    start_http_server(9100)
    while True:
        started = random.randint(90, 100)
        succeeded = started - random.randint(0, 2)
        job_success.set(succeeded)
        job_started.set(started)
        job_duration.set(random.uniform(300, 900))
        cluster_uptime.set(86400 - random.uniform(0, 100))
        cluster_cost.set(random.uniform(300, 450))
        time.sleep(15)
