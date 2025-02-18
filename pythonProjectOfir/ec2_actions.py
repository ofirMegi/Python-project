import argparse
import boto3

AMI_UBUNTU_T4G = 'ami-0a7a4e87939439934'
AMI_UBUNTU_T3 = 'ami-04b4f1a9cf54c11d0'
AMI_AMAZON_T4G = 'ami-0c518311db5640eff'
AMI_AMAZON_T3 = 'ami-053a45fff0a704a47'
RESOURCE = boto3.resource('ec2')
IAM = boto3.client('iam')
EC2 = boto3.client('ec2')
USER_RESPONSE = IAM.get_user()
USER_NAME = USER_RESPONSE['User']['UserName']


def num_of_running_EC2():
    ec2_response = EC2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    running_instances_num = 0
    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'User' and tag['Value'] == USER_NAME:
                    running_instances_num += 1
    return running_instances_num


def information_for_the_new_EC2_instance():
    parser = argparse.ArgumentParser(description="Collect information about the EC2")
    parser.add_argument("instance_name", help="enter the name of the EC2 instance: ")
    parser.add_argument("type_op_num", help="enter the number of the type you prefer:\n[1]t3.nano\n[2]t4g.nano")
    parser.add_argument("ami_choice", help="enter the number of the AMI you prefer:\n[1]ubuntu\n[2]amazon linux")
    print("The information collected successfully")
    return parser.parse_args()


def create_parameter_from_info(args):
    instance_name = args.instance_name
    if args.type_op_num == "1":
        type = 't3.nano'
        if args.ami_choice == "1":
            ami_choice = AMI_UBUNTU_T3
        elif args.ami_choice == "2":
            ami_choice = AMI_AMAZON_T3
    elif args.type_op_num == "2":
        type = 't4g.nano'
        if args.ami_choice == "1":
            ami_choice = AMI_UBUNTU_T4G
        elif args.ami_choice == "2":
            ami_choice = AMI_AMAZON_T4G
    return instance_name, type, ami_choice


def create_EC2_instance(instance_name, type, ami_choice):
    instances = RESOURCE.create_instances(
        ImageId=ami_choice,
        InstanceType=type,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    },

                    {'Key': 'Owner',
                     'Value': USER_NAME
                     },

                    {'Key': 'from',
                     'Value': 'cli'
                     }
                ]
            },
        ],
    )
    print(f'the creation completed, you created EC2 instance with\nthe name: {instance_name}\nthe type: {type}\nand the AMI: {ami_choice}')

def list_of_instances():
    ec2_response = EC2.describe_instances(Filters=[{'Name': 'tag:from', 'Values': ['cli']}, {'Name': 'tag:Owner', 'Values': [USER_NAME]}])