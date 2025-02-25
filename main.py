import ec2_actions
import s3_actions
import route53_actions
import connect_cli
import subprocess
YES = 'yes'
OPTION1 = '1'
OPTION2 = '2'
OPTION3 = '3'

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
flag = True
while flag:
    connect_cli.main()
    option = input("on what would you like to do action?\n[1]EC2\n[2]S3 Bucket\n[3]Route53")
    if option == OPTION1:
        ec2_actions.main()
    elif option == OPTION2:
        s3_actions.main()
    elif option == OPTION3:
        route53_actions.main()
    else:
        print("you typed something wrong")
        break
    question = input("would you like to do another action?yes/no")
    if question.lower() != YES:
        flag = False
