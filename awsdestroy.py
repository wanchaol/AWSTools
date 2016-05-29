# usage: python awsdestroy.py inputfile

import sys
from sys import argv
import json
import subprocess


def desctroyInstances():

    idfile = open("instance_ids.txt", "r")
    allIds = idfile.readlines()

    destroycmd = ["aws", "ec2", "terminate-instances", "--instance-ids"]

    for singleId in allIds:
        singleId = singleId.strip('\n')
        destroycmd.append(singleId)

    print destroycmd

    p = subprocess.Popen(destroycmd)
    p.wait()


if __name__ == "__main__":

    if len(argv) != 1:
        print "Destroy AWS EC2 instances"
        print "Usage: python awsdestroy.py"
        sys.exit("arguments wrong")


    desctroyInstances()



