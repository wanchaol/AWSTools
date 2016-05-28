# usage: python awscreate.py num_instances outputfile

import sys
from sys import argv
import json
import subprocess

def extractIPs(outputname):

    with open("awsinstances.json") as data_file:    
                data = json.load(data_file)

    outputfile = open(outputname, "w")

    instances = data["Reservations"][0]["Instances"]

    for instance in instances:
        ipaddr = instance["PublicIpAddress"]
        outputfile.write(ipaddr)
        outputfile.write("\n")

    outputfile.close()


def describeInstances():

    jsonoutput = open("awsinstances.json", "w")
    p = subprocess.Popen(["aws", "ec2", "describe-instances"], stdout= jsonoutput)

    p.wait()
    jsonoutput.flush()

    jsonoutput.close()

def createInstances(num):



if __name__ == "__main__":

    if argc != 3:
        print "Create AWS EC2 instances"
        print "Usage: python awscreate.py num_instances outputfile"
        sys.exit("arguments wrong")


    script, num_instances, outputname = argv

    createInstances(num_instances)
    describeInstances()

    extractIPs(outputname)

