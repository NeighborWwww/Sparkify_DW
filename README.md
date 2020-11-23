# Data Warehouse using AWS Redshift
## 1. Introduction
In this project, data collected from the music platform are stored in the AWS S3 storages. The data are organized using ```.json``` files. An AWS Redshift cluster will be created to transfer the data from the AWS S3 storage to the Data Warehouse. SQL queries will be provided to read data and ETL the data.

## 2. Code
There are 5 files in this project, they are 
```sql_queries.py```
In this file, SQL queries are designed to perform 
* ```CREATE``` staging tables to hold data from AWS S3.
* ```CREATE``` a star schema with desired fact table and dimension tables.
* ```COPY``` data from AWS S3 to staging table using a created ARN role.
* ```INSERT``` the transformed data to the fact table and dimension tables.
* ```DROP``` all the table.

The schema of the database is shown below:
