import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.window import FixedWindows
import json
import time

class DataTransform(beam.DoFn):
    def process(self, element):
        record = json.loads(element)
        # Replace TimestampParam with current time
        record['processed_timestamp'] = time.time()
        key = record['tenant_id']  # Use tenant_id as the key
        value = {
            'metric_name': record['metric_name'],
            'metric_value': record['metric_value'],
            'timestamp': record['timestamp'],
            'processed_timestamp': record['processed_timestamp']
        }
        print(f"Transformed Record: key={key}, value={value}")  # Debugging message
        yield key, value

class FormatForBigQuery(beam.DoFn):
    def process(self, element):
        key, values = element
        for value in values:
            formatted_record = {
                'tenant_id': key,
                'metric_name': value['metric_name'],
                'metric_value': value['metric_value'],
                'timestamp': value['timestamp'],
                'processed_timestamp': value['processed_timestamp']
            }
            print(f"Formatted Record: {formatted_record}")  # Debugging message
            yield formatted_record

def run():
    options = PipelineOptions(streaming=True)
    p = beam.Pipeline(options=options)

    (p
     | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(topic='projects/my-assignment-2-432009/topics/tenant-perf-metrics')
     | 'Window into Fixed Intervals' >> beam.WindowInto(FixedWindows(300))  # Windowing every 5 minutes
     | 'Transform Data' >> beam.ParDo(DataTransform())
     | 'Group by Tenant ID' >> beam.GroupByKey()
     | 'Format for BigQuery' >> beam.ParDo(FormatForBigQuery())
     | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
            'my-assignment-2-432009:tenant_performance.metrics',
            schema='tenant_id:STRING,metric_name:STRING,metric_value:FLOAT,timestamp:TIMESTAMP,processed_timestamp:TIMESTAMP',
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

    p.run().wait_until_finish()

if __name__ == '__main__':
    run()