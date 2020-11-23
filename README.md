# Data Warehouse using AWS Redshift
## 1. Introduction
In this project, data collected from the music platform are stored in the AWS S3 storages. The data are organized using ```.json``` files. An AWS Redshift cluster will be created to transfer the data from the AWS S3 storage to the Data Warehouse. SQL queries will be provided to read data and ETL the data.

## 2. Code
There are 5 files in this project, they are 

### ```sql_queries.py```
In this file, SQL queries are designed to perform 
* ```CREATE``` staging tables to hold data from AWS S3.
* ```CREATE``` a star schema with desired fact table and dimension tables.
* ```COPY``` data from AWS S3 to staging table using a created ARN role.
* ```INSERT``` the transformed data to the fact table and dimension tables.
* ```DROP``` all the table.
The ```create_table.py``` and ```etl.py``` will take the queries to perform data import, table building, and ETL process.

### The schema of the database is shown below:
#### Fact table: songplays
|Variables|Type|
|---------|----|
|songplay_id|INT IDENTITY(0,1)| 
|start_time|TIMESTAMP NOT NULL| 
|user_id|VARCHAR NOT NULL| 
|level|VARCHAR|
|song_id|VARCHAR NOT NULL| 
|artist_id|VARCHAR NOT NULL|
|session_id|BIGINT| 
|location|VARCHAR| 
|user_agent|VARCHAR|

#### Dimension table: users
|Variables|Type|
|---------|----|
|user_id|VARCHAR NOT NULL| 
|first_name|VARCHAR| 
|last_name|VARCHAR|
|gender|VARCHAR| 
|level|VARCHAR NOT NULL| 

#### Dimension table: songs
|Variables|Type|
|---------|----|
|song_id|VARCHAR NOT NULL| 
|title|VARCHAR|
|artist_id|VARCHAR NOT NULL|
|year|INTEGER NOT NULL| 
|duration|DOUBLE PRECISION|

#### Dimension table: artists
|Variables|Type|
|---------|----|
|artist_id|VARCHAR NOT NULL| 
|name|VARCHAR NOT NULL|
|location|VARCHAR| 
|latitude|DOUBLE PRECISION|
|longitude|DOUBLE PRECISION| 

#### Dimension table: times
|Variables|Type|
|---------|----|
|start_time|TIMESTAMP|
|hour|INTEGER|
|day|INTEGER|
|week|INTEGER| 
|month|INTEGER|
|year|INTEGER| 
|weekday|INTEGER| 

### ```create_table.py```
In this part, connection to the AWS Redshift cluster will be built and perform ```DROP TABLE``` and ```CREATE TABLE``` queries. Staging table, fact table, and dimension table will be drop then create.

### ```etl.py```
Similar to the ```create_table.py```, ```etl.py``` connect the AWS Redshift cluster and perform data ```COPY``` from AWS S3, which contain the ```.json``` data provided. ```INSERT``` queries will transform the data from staging table and insert the desire data into fact and dimension tables.

### ```dwh.cfg```
A config file contain the AWS Redshift cluster information, ARN, and S3 address and json path. The information will be used to establish connection to the AWS Redshift cluster and data transfer from S3 bucket to the Redshift.

### ```test.ipynb``` (further improvement)
The previous approach is create IAM role, security group, and Redshift cluster at AWS console. The new approach is trying to implement Infrastructure as Code (IaC) in this project. The code is still testing and will be provide soon.

## 3. How to run
1. After configure the AWS Redshift, Security group, and IAM S3 read-only role, copy and paste required information into ```dwh.cfg```.
2. Run ```create_table.py``` to create tables in the AWS Redshift. (Run this to initialized tables if something goes wrong in the ETL process).
3. Run ```etl.py``` to perform ETL process, check the final result using the queries in the AWS console if necessary.
