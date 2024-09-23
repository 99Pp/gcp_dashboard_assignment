
import time
import json
from google.cloud import pubsub_v1
from google.cloud import monitoring_v3
from google.protobuf.json_format import MessageToDict

# Set your Google Cloud Project ID and Pub/Sub topic ID



import time
import json
from google.cloud import pubsub_v1
from google.cloud import monitoring_v3

# Set your Google Cloud Project ID and Pub/Sub topic ID
PROJECT_ID = 'my-assignment-2-432009'
TOPIC_ID = 'tenant-perf-metrics'

def collect_metrics():
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"
    interval = monitoring_v3.TimeInterval({
        'end_time': {'seconds': int(time.time())},
        'start_time': {'seconds': int(time.time()) - 300},  # Expanded to 5 minutes
    })

    metric_type = 'compute.googleapis.com/instance/cpu/utilization'

    metrics = []
    try:
        print("Attempting to list time series...")
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": f'metric.type = "{metric_type}" AND resource.type = "gce_instance"',
                "interval": interval,
                "aggregation": {
                    "alignment_period": {"seconds": 60},
                    "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                    "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
                    "group_by_fields": [
                        "metadata.system_labels.\"name\"",
                        "resource.label.\"zone\"",
                        "resource.label.\"project_id\"",
                        "resource.label.\"instance_id\""
                    ]
                },
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )

        print("Time series listed successfully.")
        for result in results:
            print(f"Processing result: {result}")
            for point in result.points:
                metrics.append({
                    'tenant_id': result.resource.labels['instance_id'],
                    'metric_name': metric_type.split('/')[-1],
                    'metric_value': point.value.double_value,
                    'timestamp': point.interval.end_time.timestamp()
                })

        print(f"Collected Metrics: {metrics}")  # Debugging message
    except Exception as e:
        print(f"Error collecting metrics: {e}")  # Debugging message

    return metrics

def publish_to_pubsub(metrics):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    for metric in metrics:
        message_json = json.dumps(metric)
        message_bytes = message_json.encode('utf-8')
        future = publisher.publish(topic_path, data=message_bytes)
        print(f"Published message ID: {future.result()}")  # Debugging message

if __name__ == "__main__":
    while True:
        metrics = collect_metrics()
        if metrics:
            publish_to_pubsub(metrics)
        else:
            print("No metrics collected in this interval.")
        time.sleep(300)  # Collect metrics every 5 minutes