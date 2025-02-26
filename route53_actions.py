import boto3
import string
from datetime import datetime

NOW = datetime.now()
MAX_HOSTED_ZONE_NAME_LEN = 253
MAX_CHAR_LEN_BETWEEN_DOTS = 63
HOSTED_ZONE_NAME_ALLOWED_CHAR = string.ascii_lowercase + string.ascii_uppercase + string.digits + '.-'
PUBLIC_ACL_NUMBER = '1'
ROUTE53 = boto3.client('route53')
IAM = boto3.client('iam')
USER_RESPONSE = IAM.get_user()
USER_NAME = USER_RESPONSE['User']['UserName']
MAX_DOT_IN_IP = 3
OPTION1 = '1'
OPTION2 = '2'
OPTION3 = '3'
DOT = '.'



def create_zone():
    domain_name = input("enter the domain name: ")
    flag = True
    while flag:
        if "." not in domain_name:
            print("you didn't entered a dot")
        for char in domain_name:
            if char not in HOSTED_ZONE_NAME_ALLOWED_CHAR:
                print("you entered invalid char")
        if len(domain_name) > MAX_HOSTED_ZONE_NAME_LEN:
            print('the maximum chars in hosted zone name are 253')
        if domain_name[0] == DOT or domain_name[-1] == DOT:
            print("you can't put '.' in the beginning/end of the name")
            break
        parts = domain_name.split(DOT)
        for part in parts:
            if len(part) == 0:
                break
            if part[0] == "-" or part[-1] == "-":
                print("you can't put '-' in the begging/end of the name")
                break
            if len(part) > MAX_CHAR_LEN_BETWEEN_DOTS:
                print('the maximum chars between dots are 63')
        else:
            flag = False
    caller_reference = f"{domain_name}_{NOW.strftime('%Y-%m-%d_%H-%M-%S')}"
    try:
        response = ROUTE53.create_hosted_zone(
            Name=domain_name,
            CallerReference=caller_reference,
            HostedZoneConfig={
                'Comment': 'Hosted zone created from the Cli',
                'PrivateZone': False
            }
        )
    except Exception as e:
        print(f"Something went wrong: {e}")


def dict_of_hosted_zone_created_cli():
    host_zone_dict = {}
    response = ROUTE53.list_hosted_zones()
    for host_zone in response['HostedZones']:
        if 'Comment' in host_zone['Config']:
            if host_zone['Config']['Comment'] == 'Hosted zone created from the Cli':
                hosted_zone_id = host_zone['Id']
                host_zone_id = hosted_zone_id.split('/')[-1]
                host_zone_name = host_zone['Name']
                host_zone_dict[host_zone_id] = host_zone_name
    return host_zone_dict


def collect_info(host_zone_id):
    host_zone_dict = dict_of_hosted_zone_created_cli()
    while True:
        ttl = input("enter the TTL number: ")
        if ttl.isdigit():
            ttl = int(ttl)
            break
        else:
            print("you can only enter digits")
    while True:
        ip_address = input("enter the ip address you want the record to be on: ")
        if ip_address.count(DOT) == MAX_DOT_IN_IP:
            parts = ip_address.split(DOT)
            for part in parts:
                if not part.isdigit():
                    print("you can only enter digits")
                    break
            break
        else:
            print("the ip is invalid there are too many dots")
    record_set = {
        'Name': host_zone_dict[host_zone_id],
        'Type': 'A',
        'TTL': ttl,
        'ResourceRecords': [{'Value': ip_address}],
    }

    return host_zone_id, record_set


def check_what_action():
    while True:
        action_num = input("select the action you would like to do on the record:\n[1]CREATE\n[2]DELETE\n[3]UPSERT")
        if action_num == OPTION1:
            return 'CREATE'
        if action_num == OPTION2:
            return 'DELETE'
        if action_num == OPTION3:
            return 'UPSERT'
        print("you entered something wrong")


def action_on_dns_record(host_zone_id, record_set, action):
    try:
        change_batch = {
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': record_set
                }
            ]
        }
        response = ROUTE53.change_resource_record_sets(
            HostedZoneId=host_zone_id,
            ChangeBatch=change_batch
        )
        print(f"DNS record {action.lower()}ed successfully")
    except Exception as e:
        print(f"Error {action.lower()}ing DNS record: {e}")


def main():
    option = input("select what you would like to do:\n[1]Create zone\n[2]action on record")
    if option == OPTION1:
        create_zone()
    elif option == OPTION2:
        action = check_what_action()
        while True:
            host_zone_dict = dict_of_hosted_zone_created_cli()
            print(host_zone_dict)
            host_zone_id = input("enter the id of the host zone you would like to work on")
            if host_zone_id in host_zone_dict:
                break
            else:
                print("Error: This zone was not created from the CLI. Cannot create DNS record.")
        host_zone_id, record_set = collect_info(host_zone_id)
        action_on_dns_record(host_zone_id, record_set, action)
    else:
        print("you typed something wrong")


