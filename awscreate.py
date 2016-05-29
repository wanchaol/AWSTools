#Usage: python awscreate.py keypair securitygroup num_instances instance_type outputfile

import sys
from sys import argv
import json
import subprocess
from subprocess import call
from urllib2 import urlopen


def extractIPs(outputname):

    with open("awsinstances.json") as data_file:    
                data = json.load(data_file)

    outputfile = open(outputname, "w")
    idfile = open("instance_ids.txt", "w")

    instances = data["Reservations"][0]["Instances"]

    for instance in instances:
        ipaddr = instance["PublicIpAddress"]
        instance_id = instance["InstanceId"]
        outputfile.write(ipaddr)
        outputfile.write("\n")
        idfile.write(instance_id)
        idfile.write("\n")

    outputfile.close()
    idfile.close()

def checkInstanceStatus():

    checkcmd = ["aws", "ec2", "describe-instance-status"]

    jsonoutput = open("awsstatus.json", "w")
    p = subprocess.Popen(checkcmd, stdout=jsonoutput)

    p.wait()
    jsonoutput.flush()
    jsonoutput.close()

    with open("awsstatus.json") as data_file:    
                data = json.load(data_file)

    #print data["InstanceStatuses"]
    num_ups = len(data["InstanceStatuses"])
    #print num_ups

    return num_ups

    #data = json.loads(p.stdout.read())
    #print data['Instances']


def describeInstances(num_instances):

    while True:
        
        print "booting..."
        if checkInstanceStatus() == num_instances:
            break

    jsonoutput = open("awsinstances.json", "w")
    p = subprocess.Popen(["aws", "ec2", "describe-instances", "--filters", '''Name=instance-state-name,Values=running'''], stdout= jsonoutput)

    p.wait()
    jsonoutput.flush()

    jsonoutput.close()

def createInstances(keypair, securitygroup, num_instances, instance_type):
    print "creating instances.."

    awscmd = ["aws", "ec2", "run-instances", "--image-id", "ami-d0f506b0", "--count", num_instances, "--instance-type", instance_type, 
          "--key-name", keypair, "--security-group-ids", securitygroup, "--associate-public-ip-address"]
    print awscmd
    #aws ec2 run-instances --image-id ami-d0f506b0 --count 2 --instance-type t2.micro --key-name wanchaol-key-pair-oregon --security-group-ids sg-79e3111f --associate-public-ip-address

    aws_p = subprocess.Popen(awscmd)

    aws_p.wait()

    print "instances created"

if __name__ == "__main__":
    
    if len(argv) != 6:
        print "Create AWS EC2 instances"
        print "Usage: python awscreate.py keypair securitygroup num_instances instance_type outputfile"
        sys.exit("arguments wrong")


    script, keypair, securitygroup, num_instances, instance_type, outputname = argv

    #print argv

    createInstances(keypair, securitygroup, num_instances, instance_type)
    describeInstances(int(num_instances))

    extractIPs(outputname)

    #checkInstanceStatus()
