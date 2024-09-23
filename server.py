from flask import Flask, render_template
import pandas as pd
from google.cloud import bigquery

app = Flask(__name__)

# Root route
@app.route('/')
def index():
    """
    Redirects to the dashboard or provides basic information.
    """
    return "Welcome to the Multi-Tenant Performance Dashboard. Visit /dashboard to view the metrics."

# Dashboard route
@app.route('/dashboard')
def dashboard():
    """
    Renders the visualization dashboard.

    Returns:
    str: Rendered HTML template for the dashboard.
    """
    client = bigquery.Client()
    query = """
    SELECT tenant_id, metric_name, AVG(metric_value) as avg_metric_value, TIMESTAMP_TRUNC(timestamp, HOUR) as hour
    FROM `my-assignment-2-432009.tenant_performance.metrics`
    GROUP BY tenant_id, metric_name, hour
    ORDER BY hour
    """
    query_job = client.query(query)
    data = query_job.to_dataframe()

    # Print the data to verify it's retrieved correctly
    print(data)

    return render_template('dashboard.html', data=data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)