
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
        validate = input('do you need to install boto3?yes/no')
        if validate.lower() == YES:
            try:
                subprocess.check_call(["pip", "install", "boto3"])
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing boto3: {e}")
        validate = input('do you need to install awscli?yes/no')
        if validate.lower() == YES:
            try:
                subprocess.check_call(["pip", "install", "awscli"])
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing AWS CLI: {e}")
        if not check_if_aws_user_connected():
            aws_access_key_id, aws_secret_access_key, aws_region = collect_and_return_aws_connection_information()
            connect_to_aws_account(aws_access_key_id, aws_secret_access_key, aws_region)


if __name__ == '__main__':
    main()

