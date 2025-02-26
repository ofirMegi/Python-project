import boto3
from botocore.exceptions import ClientError
import os
import string
import json


MIN_BUCKET_NAME_LEN = 3
MAX_BUCKET_NAME_LEN = 63
S3 = boto3.client('s3')
IAM = boto3.client('iam')
USER_RESPONSE = IAM.get_user()
USER_NAME = USER_RESPONSE['User']['UserName']
S3_BUCKET_NAME_ALLOWED_CHAR = string.ascii_lowercase + string.digits + '.-'
OPTION1 = '1'
OPTION2 = '2'
OPTION3 = '3'
PRIVATE = 'private'
DOT = '.'
NOT_FOUND = '404'
NO_ACCESS = '403'
YES = 'yes'
MAX_OBJECT_NAME_LEN = 1024
SPACE = ' '
SLASH = '/'

def create_bucket_info():
    bucket_name = ""
    while True:
        try:
            while True:
                bucket_name = input("enter the name of the bucket: ")
                if bucket_name[0] == DOT or bucket_name[-1] == DOT:
                    print("the bucket name can not start or end with a dot")
                elif ".." in bucket_name:
                    print("the bucket name can not have sequence of dots")
                elif MIN_BUCKET_NAME_LEN > len(bucket_name) or len(bucket_name) > MAX_BUCKET_NAME_LEN:
                    print("the bucket name len needs to be 3-63 letters")
                for char in bucket_name:
                    if char not in S3_BUCKET_NAME_ALLOWED_CHAR:
                        print("you entered invalid char")
                else:
                    break
            S3.head_bucket(Bucket=bucket_name)
            print(f"the name {bucket_name} already exist")
        except ClientError as error:
            if error.response['Error']['Code'] == NOT_FOUND:
                print(f"the name {bucket_name} is not occupied ")
                break
            if error.response['Error']['Code'] == NO_ACCESS:
                print(f"the name {bucket_name} already exist ")
    acl_value = input("chose public or private:\n[1]public\n[2]private")
    if acl_value == '1':
        validate = input("are you sure?yes/no")
        if validate.lower() == YES:
            acl_value = 'public-read'
    else:
        acl_value = PRIVATE
    return bucket_name, acl_value


def create_bucket(bucket_name, acl_value):
    response = S3.create_bucket(
        Bucket=bucket_name)
    print("the action completed")
    tag_response = S3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={
            'TagSet': [
                {'Key': 'CreatedFromCli', 'Value': 'True'},
                {'Key': 'Owner', 'Value': USER_NAME}
            ]
        }
    )
    if acl_value == 'public-read':
        S3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        public_read_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        policy_string = json.dumps(public_read_policy)

        try:
            S3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=policy_string
            )
            print(f"Public read policy has been applied to the bucket {bucket_name}.")
        except ClientError as e:
            print(f"An error occurred while applying the policy: {e}")


def list_of_buckets():
    tag_key = 'CreatedFromCli'
    tag_value = 'True'
    response = S3.list_buckets()
    buckets = response['Buckets']
    buckets_with_tag = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            tags_response = S3.get_bucket_tagging(Bucket=bucket_name)

            for tag in tags_response.get('TagSet', []):
                if tag['Key'] == tag_key and tag['Value'] == tag_value:
                    buckets_with_tag.append(bucket_name)
        except Exception as e:
            print(e)
    return  buckets_with_tag

def upload_file_info():
    while True:
        list_buckets = list_of_buckets()
        print(f'the buckets you can choose: {list_buckets}')
        bucket_name = input("enter the bucket name: ")
        if bucket_name not in list_buckets:
            print(f'the bucket {bucket_name} cannot be selected ')
        else:
            break


    while True:
        file_path = input("enter the file path: ")
        if os.path.exists(file_path):
            break
        else:
            print(f"the path ({file_path}) you entered is incorrect")

    bool_obj_name = input("would you like to add object name?yes/no ")
    if bool_obj_name.lower() == YES:
        while True:
            object_name = input('enter the object file name: ')
            if SPACE in object_name:
                print('the name you entered is incorrect, the name should be without any spaces')
            elif object_name[-1] == SLASH:
                print('the name you entered is incorrect, the last char cant be /')
            elif len(object_name) > MAX_OBJECT_NAME_LEN:
                print('the name you entered is incorrect, the len cant be above 1024')
            else:
                break
    else:
        object_name = os.path.basename(file_path)

    return file_path, bucket_name, object_name


def upload_file_to_s3(file_path, bucket_name, object_name):
    S3.upload_file(file_path, bucket_name, object_name)



def main():
    option = input("select what you would like to do:\n[1]Create S3 buckets\n[2]File Upload\n[3]List Buckets")
    if option == OPTION1:
        bucket_name, acl_value = create_bucket_info()
        create_bucket(bucket_name, acl_value)
    elif option == OPTION2:
        file_path, bucket_name, object_name = upload_file_info()
        upload_file_to_s3(file_path, bucket_name, object_name)
    elif option == OPTION3:
        print(list_of_buckets())
    else:
        print("you typed something wrong")

