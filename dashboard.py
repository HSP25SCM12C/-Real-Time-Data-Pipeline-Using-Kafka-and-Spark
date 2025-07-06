import ast
import time
import pytz
import random
import pandas as pd
from datetime import datetime
from kafka import KafkaConsumer

from bokeh.driving import count
from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models.widgets import Div
from bokeh.layouts import row

# Timezone for timestamp formatting
tz = pytz.timezone('Asia/Bangalore')

# Update frequency and number of visible data points
UPDATE_INTERVAL = 1000  # milliseconds
ROLLOVER = 10           # limit of data points on the graph

# Initialize Bokeh data source
source = ColumnDataSource({"x": [], "y": []})

# Kafka consumer for topic CleanSensorData
consumer = KafkaConsumer(
    'CleanSensorData',
    auto_offset_reset='earliest',
    bootstrap_servers=['localhost:9092'],
    consumer_timeout_ms=1000
)

# Widget to display current timestamp
div = Div(text='', width=120, height=35)

@count()
def update(x):
    # Fetch one message from Kafka
    for msg in consumer:
        msg_value = msg
        break

    # Decode and parse the message
    values = ast.literal_eval(msg_value.value.decode("utf-8"))

    # Convert timestamp to datetime
    ts_millis = values["TimeStamp"]["$date"]
    x_time = datetime.fromtimestamp(ts_millis / 1000.0, tz)
    x = pd.to_datetime(x_time)

    # Update the Div widget
    div.text = f"TimeStamp: {x}"

    # Extract water temperature
    y = values["WaterTemperature"]
    print(f"Time: {x}, Temp: {y}")

    # Stream data to Bokeh plot
    source.stream({"x": [x], "y": [y]}, rollover=ROLLOVER)

# Create Bokeh figure
p = figure(
    title="Water Temperature Sensor Data",
    x_axis_type="datetime",
    plot_width=1000
)
p.line("x", "y", source=source)

# Customize plot appearance
p.xaxis.formatter = DatetimeTickFormatter(
