import boto3

AMI_UBUNTU_T4G = 'ami-0a7a4e87939439934'
AMI_UBUNTU_T3 = 'ami-04b4f1a9cf54c11d0'
AMI_AMAZON_T4G = 'ami-0c518311db5640eff'
AMI_AMAZON_T3 = 'ami-053a45fff0a704a47'
MAX_NUM_RUNNING_EC2 = 2
RESOURCE = boto3.resource('ec2')
IAM = boto3.client('iam')
EC2 = boto3.client('ec2')
USER_RESPONSE = IAM.get_user()
USER_NAME = USER_RESPONSE['User']['UserName']
OPTION1 = '1'
OPTION2 = '2'
OPTION3 = '3'
OPTION4 = '4'
YES = 'yes'
TAG_KEY_VALUE = 'Name'
T3 = 't3.nano'
T4 = 't4g.nano'

def dict_of_instances(filters):
    dict_instances = {}
    ec2_response = RESOURCE.instances.filter(Filters=filters)
    for instance in ec2_response:
        for tag in instance.tags:
            if tag['Key'] == TAG_KEY_VALUE:
                dict_instances[instance.id] = tag['Value']
    return dict_instances


def can_create_ec2(filters):
    return len(dict_of_instances(filters)) < MAX_NUM_RUNNING_EC2


def information_for_the_new_EC2_instance():
    instance_name = input("enter the name of the EC2 instance: ")
    type_op_num = input("enter the number of the type you prefer:\n[1]t3.nano\n[2]t4g.nano\n")
    ami_choice = input("enter the number of the AMI you prefer:\n[1]ubuntu\n[2]amazon linux\n")
    print("The information collected successfully")
    return instance_name, type_op_num, ami_choice


def create_parameter_from_info(instance_name, type_op_num, ami_choice):
    if type_op_num == OPTION1:
        ec2_type = T3
        if ami_choice == OPTION1:
            ami = AMI_UBUNTU_T3
        elif ami_choice == OPTION2:
            ami = AMI_AMAZON_T3
    elif type_op_num == OPTION2:
        ec2_type = T4
        if ami_choice == OPTION1:
            ami = AMI_UBUNTU_T4G
        elif ami_choice == OPTION2:
            ami = AMI_AMAZON_T4G
    else:
        print("it appeared that something was incorrect")
    return instance_name, ec2_type, ami


def create_EC2_instance(instance_name, ec2_type, ami):
    instances = RESOURCE.create_instances(
        ImageId=ami,
        InstanceType=ec2_type,
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
    print(
        f'the creation completed, you created EC2 instance with\nthe name: {instance_name}\nthe type: {ec2_type}\nthe AMI: {ami}')



def stop_instance():
    run_filters = [{'Name': 'instance-state-name', 'Values': ['running']}, {'Name': 'tag:Owner', 'Values': [USER_NAME]}, {'Name': 'tag:from', 'Values': ['cli']}]
    instances_dict = dict_of_instances(run_filters)
    flag = True
    while flag:
        instance_id = input(f'choose from here what would you like to stop: {instances_dict}')
        if instance_id in instances_dict:
            flag = False
        else:
            print(f'the instance with the id {instance_id} cannot be stopped from here')
    response = EC2.stop_instances(InstanceIds=[instance_id])
    print(f'the instance with the id {instance_id} has successfully stopped')

def start_instance():
    stop_filters = [{'Name': 'instance-state-name', 'Values': ['stopped']}, {'Name': 'tag:Owner', 'Values': [USER_NAME]}, {'Name': 'tag:from', 'Values': ['cli']}]
    instances_dict = dict_of_instances(stop_filters)
    flag = True
    while flag:
        instance_id = input(f'choose from here what would you like to start: {instances_dict}')
        if instance_id in instances_dict:
            flag = False
        else:
            print(f'the instance with the id {instance_id} cannot be started from here')
        response = EC2.start_instances(InstanceIds=[instance_id])
        print(f'the instance with the id {instance_id} has successfully started')


def main():
    filters = [{'Name': 'tag:from', 'Values': ['cli']}, {'Name': 'tag:Owner', 'Values': [USER_NAME]}]
    run_filters = [{'Name': 'instance-state-name', 'Values': ['running']}, {'Name': 'tag:Owner', 'Values': [USER_NAME]},{'Name': 'tag:from', 'Values': ['cli']}]
    option = input("select what you would like to do:\n[1]Create EC2 Instances\n[2]start EC2 Instances\n[3]stop EC2 Instances\n[4]list of EC2 Instances")
    if option == OPTION1:
        if can_create_ec2(run_filters):
            instance_name, type_op_num, ami_choice = information_for_the_new_EC2_instance()
            instance_name, ec2_type, ami = create_parameter_from_info(instance_name, type_op_num, ami_choice)
            create_EC2_instance(instance_name, ec2_type, ami)
    elif option == OPTION2:
        start_instance()
    elif option == OPTION3:
        stop_instance()
    elif option == OPTION4:
        instances_dict = dict_of_instances(filters)
        print(instances_dict)
    else:
        print("you typed something wrong")


