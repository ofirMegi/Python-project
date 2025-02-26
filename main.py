import ec2_actions
import s3_actions
import route53_actions
YES = 'yes'



try:
    while True:
        option = input("on what would you like to do action?\n[1]EC2\n[2]S3 Bucket\n[3]Route53")
        if option == '1':
            ec2_actions.main()
        elif option == '2':
            s3_actions.main()
        elif option == '3':
            route53_actions.main()
        else:
            print("you typed something wrong")
        question = input("would you like to do another action?yes/no")
        if question.lower() != YES:
            break

except Exception as e:
    print(e)


