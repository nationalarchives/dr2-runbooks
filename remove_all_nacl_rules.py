import boto3

client = boto3.client("ec2")


def remove_all_nacl_rules():
    network_acls = client.describe_network_acls()['NetworkAcls']
    for acl in network_acls:
        all_custom_rules = [entry for entry in acl['Entries'] if entry['RuleNumber'] < 32767]
        for rule in all_custom_rules:
            client.delete_network_acl_entry(
                Egress=rule['Egress'],
                NetworkAclId=acl['NetworkAclId'],
                RuleNumber=rule['RuleNumber'])


if __name__ == '__main__':
    remove_all_nacl_rules()
