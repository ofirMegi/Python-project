import os
import subprocess
import argparse

def check_if_aws_user_connected():
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if access_key and secret_key:
        print("You are connected")
        return True

    print("You are not connected")
    return False

def collect_and_return_aws_connection_information():
    parser = argparse.ArgumentParser(description="Configure AWS access keys")
    parser.add_argument("aws_access_key_id", help="AWS Access Key ID: ")
    parser.add_argument("aws_secret_access_key", help="AWS Secret Key: ")
    parser.add_argument("aws_region", help="AWS Region: ")
    print("The information collected successfully")
    return parser.parse_args()
#יהיה שווה לargs בעת זימון הפונקציה
def connect_to_aws_account(args):
    args_dict = {"aws_access_key_id": args.aws_access_key_id, "aws_secret_access_key": args.aws_secret_access_key, "aws_region": args.aws_region}
    for key in args_dict.keys():
        subprocess.run(["aws", "configure", "set", key, args_dict[key]])
    print("AWS credentials configured successfully")


