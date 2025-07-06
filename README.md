# -Real-Time-Data-Pipeline-Using-Kafka-and-Spark

Real-Time Data Pipeline Using Kafka and Spark
Pipeline Architecture Overview
API
A mock API is developed using the Flask framework to simulate water quality sensor data. The output format is as follows:

makefile
Copy
Edit
‘2020-02-17T11:12:58.765969 26.04 540.1 13.12 Montrose_Beach 758028’
This string represents:

Timestamp

Battery life

Turbidity

Water temperature

Beach name

Measurement ID

Kafka Producer (Topic: RawSensorData)
Sensor data from the API is continuously pushed into a Kafka topic named RawSensorData via a Kafka producer.

Apache Spark + Kafka Consumer (Topic: CleanSensorData)
Spark Streaming reads data from the RawSensorData topic using a Kafka consumer. The data is parsed, validated, and structured. Once cleaned, it is sent to both:

MongoDB for storage

Another Kafka topic named CleanSensorData

MongoDB
The structured and validated data is stored in a MongoDB collection using the following schema:

Key	Data Type
_id	ObjectId
Beach	String
MeasurementID	Long
BatteryLife	Double
RawData	String
WaterTemperature	Double
Turbidity	Double
TimeStamp	Timestamp

Real-Time Dashboard
The real-time dashboard is built using the Bokeh library. It consumes data from the CleanSensorData Kafka topic and visualizes it in real time.

How to Run the Pipeline
Step-by-Step Execution
Start the Sensor API (Port: 3030)

bash
Copy
Edit
python sensor.py
Start Zookeeper

bash
Copy
Edit
bash /opt/zookeeper-3.4.14/bin/zkServer.sh start
Start Kafka Server

bash
Copy
Edit
bin/kafka-server-start.sh config/server.properties
Create Kafka Topics

bash
Copy
Edit
./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic RawSensorData

./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic CleanSensorData
Push API Data to Kafka Topic RawSensorData

bash
Copy
Edit
python push_data_to_kafka.py
Validate, Structure, and Store Data (MongoDB + CleanSensorData Topic)

bash
Copy
Edit
./bin/spark-submit structure_validate_store.py
View Kafka Topics (Optional)

bash
Copy
Edit
# RawSensorData topic
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic RawSensorData --from-beginning

# CleanSensorData topic
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic CleanSensorData --from-beginning
Launch the Real-Time Dashboard

bash
Copy
Edit
bokeh serve --show dashboard.py
