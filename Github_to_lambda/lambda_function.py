import json
import pymysql.cursors
import boto3 
from botocore.client import ClientError
def lambda_handler(event,context):  
    session = boto3.session.Session()
    Client = session.client('secretsmanager','us-east-2')
    secret_response={}
    keys={}
    try:
        secret_response = Client.get_secret_value(
            SecretId='aws-key-eventswedo-db-us-east-2',VersionStage='AWSCURRENT')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + "secret_name" + " was not found")
    keys=json.loads(secret_response["SecretString"])
    print(keys['access_key'])
    bucket_name='aws-suraj-eventswedo'
    client=boto3.client('s3',aws_access_key_id=keys['access_key'], aws_secret_access_key = keys['security_key'])
    try:   
        client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint':'ap-south-1'})
    except:  
        pass


    connection=pymysql.connect(host=keys['host'],
                             user=keys['user'],
                             password=keys['password'],
                             database=keys['database'],
                             cursorclass=pymysql.cursors.DictCursor)
    cur=connection.cursor()
    cur.execute(f"select * from  eventswedonew.tbl_vendor_categories")
    #Getting all records in dictionary form {}
    records=cur.fetchall()
    #Iterate every element in list
    for i in range(len(records)):
        # every record should have some value to load the data
        if records[i]['basicinfo'] !='':
            (records[i]['basicinfo'])=(json.loads(records[i]['basicinfo']))
        if records[i]['enquiryquestions'] is not None:
            records[i]['enquiryquestions']=(json.loads(records[i]['enquiryquestions']))
        try:
            records[i]['extrainfo']=json.loads(records[i]['extrainfo'])
            records[i]['faqs']=json.loads(records[i]['faqs'])
        except:
            pass
        try:
            records[i]['features']=json.loads(records[i]['features'])
        except:
            pass
        try:
            records[i]['policies']=json.loads(records[i]['policies'])
        except:
            pass
        try:
            records[i]['seoinfo']=json.loads(records[i]['seoinfo'])
            records[i]['filters']=json.loads(records[i]['filters'])
        except:
            continue
    # print(records)
    #Convert dictionary to Json File
    json_file=json.dumps(records,indent=4, sort_keys=True, default=str)
    # Replace the some content of Json File
    json_file = json_file.replace('basicinfo','basic_info').replace('enquiryquestions','enquiry_questions')
    # with open('categories_output.json',"w+") as json_output:
    #     json_output.write(json_file)    
    # print(type(abc))
    print(json_file)
    connection.close()
    client.put_object(Bucket='aws-suraj-eventswedo', Key='json_code.json',Body=json.dumps(json_file))
    # client.upload_file(Bucket='aws-suraj-eventswedo', Key='json_data', Body=json_file)
 