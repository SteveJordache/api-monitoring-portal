from prometheus_client import Counter, Histogram


HTTP_REQUESTS_TOTAL = Counter(
    "api_monitoring_http_requests_total",
    "Total number of HTTP requests received by the FastAPI application.",
    ["method", "path", "status_code"],
)


HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "api_monitoring_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)


MONITOR_EXECUTIONS_TOTAL = Counter(
    "api_monitoring_monitor_executions_total",
    "Total number of monitor executions.",
    ["monitor_id", "success"],
)


MONITOR_EXECUTION_DURATION_SECONDS = Histogram(
    "api_monitoring_monitor_execution_duration_seconds",
    "Monitor execution duration in seconds.",
    ["monitor_id"],
)


MONITOR_EXECUTION_FAILURES_TOTAL = Counter(
    "api_monitoring_monitor_execution_failures_total",
    "Total number of failed monitor executions.",
    ["monitor_id", "error_type"],
)
