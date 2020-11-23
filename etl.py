import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Load the records stored in the .json file in AWS S3 serve to the staging table.
    :param cur: The cluster use to take the queries.
    :param conn: manual commit will be make for each query.
    :return: void
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Perform the transformation of the data from the staging tables. Insert the transformed data
    into the fact table and dimension tables.
    :param cur: The cluster use to take the queries.
    :param conn: manual commit will be make for each query.
    :return: void
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    The main part of the program, the connection to the AWS redshift
    has been established using the information required in the dwh.cfg file
    perform the whole ETL process.
    :return:
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()