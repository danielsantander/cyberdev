# AWS CLI

- Sources:
- [aws reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html)
- [Command Examples](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-code-examples.html)
- [AWS Account](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/account/index.html#cli-aws-account)
    - [list-regions](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/account/list-regions.html)
- [EC2 CLI](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
    - [Describe Instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)
    - [EC2 Examples using AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli_ec2_code_examples.html)

---

## Configure Settings

- [src V1](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html)
- [src V2](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [Install and configure the AWS CLI and AWS SDKs](https://docs.aws.amazon.com/codeguru/latest/security-ug/aws-cli-sdk.html)

```shell
# check version
aws --version
```

## Account

List Regions

```shell
aws account list-regions --account-id <account_id_here>
aws account list-regions --account-id <account_id_here>
```

## EC2

```shell
# describe instances
aws ec2 describe-instances --instance-ids <instance_id_here>

# filter by private ip address
aws ec2 describe-instances --filters "Name=private-ip-address,Values=0.0.0.0"

# get state of instance
aws ec2 describe-instances --filters "Name=private-ip-address,Values=0.0.0.0" | grep -A 3 "State\": {"
                    "State": {
                        "Code": 16,
                        "Name": "running"
                    },
```