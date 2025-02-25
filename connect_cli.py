
import subprocess

YES = 'yes'

def check_if_aws_user_connected():
    question = input("are you connected to the aws cli? yes/no")
    if question.lower() == YES:
        return True
    return False


def collect_and_return_aws_connection_information():
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = input("AWS Secret Key: ")
    aws_region = input("AWS Region: ")
    print("The information collected successfully")
    return aws_access_key_id, aws_secret_access_key, aws_region


def connect_to_aws_account(aws_access_key_id, aws_secret_access_key, aws_region):
    aws_credentials = {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "region": aws_region
    }
    for key, value in aws_credentials.items():
        print(f"Configuring {key} with value {value}")
        subprocess.run(["aws", "configure", "set", key, value])
    print("AWS credentials configured successfully")


def main():
    if not check_if_aws_user_connected():
        aws_access_key_id, aws_secret_access_key, aws_region = collect_and_return_aws_connection_information()
        connect_to_aws_account(aws_access_key_id, aws_secret_access_key, aws_region)




