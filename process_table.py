#Import Packages
import traceback
import os
import json
import boto3
import pandas as pd

from query_package import get_query_package

from rds_connection import connect_rds
from rds_processor import RDS

from s3_bucket_util import update_active_data
from s3_bucket_util import add_archive


#Load Environment Variables
access = os.getenv('ACCESS')    # AWS access token
secret = os.getenv('SECRET')    # AWS secret token
username = os.getenv('USER')    # AWS RDS username
password = os.getenv('PASS')    #AWS RDS password
server = os.getenv('SERVER')    # AWS RDS server
db = os.getenv('DB')    # AWS RDS database
bucket = os.getenv('BUCKET')    # AWS RDS bucket name
project_folder = os.getenv('PROJECTFOLDER')     # AWS S3 Project Folder Path
active_folder = os.getenv('ACTIVEFOLDER')    # AWS S3 Project Active Folder Path
archive_folder = os.getenv('ARCHIVEFOLDER')     # AWS S3 Project Archive Folder Path



def process_table(event, context):


    #----------------------------------------------------------------

    # Pull Query Package from File
    try:
        query_package = get_query_package()

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Pull Query Package from query_package.py") from e


    #----------------------------------------------------------------

    # Connect to AWS RDS Database
    try:
        conn, cursor = connect_rds(username, password, db, server) # Connect to RDS Database
        pass

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Connect to AWS RDS Database") from e   


    #----------------------------------------------------------------

    # Create Instance of RDS Table
    try:
        rds = RDS(conn, cursor, query_package) # Create Instance of RDS Table

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Produce RDS Table from RDSTablePull in rds_connector.py") from e
    


    #----------------------------------------------------------------

    # ADD ANY FURTHER CUSTOM MODIFICATIONS TO THE TABLE
    # DO NOT FORGET TO ADD REMOVALS TO THE CLEANING DICTIONARY













    #----------------------------------------------------------------

    # Create a Boto3 client for S3
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access,
            aws_secret_access_key=secret
        )

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Connect to S3 with Secret and Access Key") from e
        


    #----------------------------------------------------------------

    # Add Active File to Project S3
    try:
        update_active_data(s3 = s3, 
                           bucket = bucket, 
                           project_folder = project_folder, 
                           active_folder = active_folder, 
                           file_name = "Active-FDEM-Hotel-Summary.csv", 
                           data = rds.df)

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Update Active Data for {project_folder}") from e 
    



     #----------------------------------------------------------------

    # Add Archive Versions to Project S3
    try:
        add_archive(s3 = s3, 
                           bucket = bucket, 
                           project_folder = project_folder, 
                           archive_folder = archive_folder, 
                           limit = 50,
                           versions = rds.archive)

    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Failed to Add Archive Folder for {project_folder}") from e 
    
    
    print("DONE")

    # TODO implement
    return {
        
        'statusCode': 200,
        'body': json.dumps('Hotel Summaries Table Processed')
    }
