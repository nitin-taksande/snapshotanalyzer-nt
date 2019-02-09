# snapshotanalyzer-nt
This is a demo project

##About

This project is a demo, and uses boto3 to manage AWS EC2 snapshots

##Configuring
shotty uses the configuration file created by AWS cli.

`aws configure --profile nitin`

##Running

`pipenv run python shotty/shott.py <command> <project>`

*command* is list, start, or stop
*project* is optional

## Modification log
Added input() command so the pipenv window does not close after execution of the python script. If running python2 use raw_input(). Pyhon3 uses input(). For this to work make sure c:\Python is in PATH of environment variable.
