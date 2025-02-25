import ec2_actions
import s3_actions
import route53_actions
import connect_cli
import subprocess


validate = input('do you need to install boto3 or awscli?yes/no')
if validate.lower() == 'yes':
    requirements_file = "requirements.txt"
    subprocess.check_call(["pip", "install", "-r", requirements_file])
flag = True
while flag:
    connect_cli.main()
    option = input("on what would you like to do action?\n[1]EC2\n[2]S3 Bucket\n[3]Route53")
    if option == '1':
        ec2_actions.main()
    elif option == '2':
        s3_actions.main()
    elif option == '3':
        route53_actions.main()
    else:
        print("you typed something wrong")
        break
    question = input("would you like to do another action?yes/no")
    if question.lower() != 'yes':
        flag = False
