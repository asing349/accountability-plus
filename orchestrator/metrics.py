from prometheus_client import Counter, Histogram, start_http_server

LATENCY = Histogram(
    "orchestrator_node_latency_seconds",
    "Time spent in each MCP call",
    ["node"]
)
FAILURES = Counter(
    "orchestrator_failures_total",
    "Total MCP call failures",
    ["node"]
)

def start_metrics_server(port: int = 9000):
    start_http_server(port)
