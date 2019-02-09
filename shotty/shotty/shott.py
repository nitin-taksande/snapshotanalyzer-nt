import boto3
import botocore
import click

#This is making sure that the script always have a session and an ec2 resource
session = boto3.Session(profile_name='nitin')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances =[]

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('snapshot')
def snapshots():
    """Commands for snapshot"""

@snapshots.command('list')
@click.option('--project' , default=None,
            help ="only instance for project (tag project:<name>)")
#function to give list of EC2 instances volumes
def list_volumes(project):
        "List EC2 Instances volumes snapshot"
        instances = filter_instances(project)

        for i in instances:
            for v in i.volumes.all():
                for s in v.snapshots.all():
                    print(",".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                    )))
        return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""
@volumes.command('list')
@click.option('--project' , default=None,
            help ="only instance for project (tag project:<name>)")
#function to give list of EC2 instances volumes
def list_volumes(project):
        "List EC2 Instances volumes"
        instances = filter_instances(project)
        for i in instances:
            for v in i.volumes.all():
                print(",".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
                )))

        return

@cli.group('instances')
def instances():
    """Commands for instances"""
@instances.command('snapshot',
                    help="create snapshot of all volumes")
@click.option('--project' , default=None,
            help ="only instance for project (tag project:<name>)")

def create_snapshot(project):
    "Create snapshot of all volumes"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshot 3000")

        print("Starting {0}...".format(i.id))

        i.start()
        i.wait_until_running()

    print("Job is done!")
    return

@instances.command('list')
@click.option('--project' , default=None,
            help ="only instance for project (tag project:<name>)")
#function to give list of EC2 instances
def list_instances(project):
        "List EC2 Instances"
        instances = filter_instances(project)

        for i in instances:

            tags = { t['Key']: t['Value'] for t in i.tags or []}
            print(', ' .join((
                i.id,
                i.instance_type,
                i.placement['AvailabilityZone'],
                i.state['Name'],
                i.public_dns_name,
                tags.get('Project', '<no project>'))))
        return


@instances.command('stop')
@click.option('--project', default = None,
            help="Only instance for project")
def stop_instances(project):
    "Stop EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stoppint {0}...".format(i.id))

        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}. ".format(i,id) + str(e))
            continue
    return


@instances.command('start')
@click.option('--project', default = None,
            help="Only instance for project")
def start_instances(project):
    "Start EC2 Instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}. ".format(i,id) + str(e))
            continue
    return

if __name__ == '__main__':
    cli()
    input()
