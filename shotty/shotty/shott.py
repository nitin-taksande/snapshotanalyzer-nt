import boto3
import click

#This is making sure that the script always have a session and an ec2 resource
session = boto3.Session(profile_name='nitin')
ec2 = session.resource('ec2')

@click.command()
#function to give list of EC2 instances
def list_instances():
        "List EC2 Instances"
        for i in ec2.instances.all():
            print(', ' .join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name)))
        return

if __name__ == '__main__':
    list_instances()
    input()
