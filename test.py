#!/usr/bin/env python3
import os
import json
import subprocess

image_name="nginx:latest"
vul_list = {}

"""
TRIVY = ["trivy", "-q", "i", "-f", "json", image_name]
trivy_result = json.loads(
    subprocess.check_output(TRIVY).decode("UTF-8")
)
item_list = trivy_result[0]["Vulnerabilities"]
vuls = {
    "UNKNOWN": 0,"LOW": 0,
    "MEDIUM": 0,"HIGH": 0,
    "CRITICAL": 0
}
for item in item_list:
    vuls[item["Severity"]] += 1
vul_list[image_name] = vuls
for severity in vul_list[image_name].keys():
    vul_num = vul_list[image_name][severity]
    print(severity + ": " + str(vul_num))
"""


f = open("request.json")
data = json.load(f)

"""
containers = data["request"]["object"]["spec"]["containers"]
for obj in containers:
    print(obj)
#  image_name=obj['image']
"""


annotations = data["request"]["object"]["metadata"]["annotations"]
vuls = {
    "UNKNOWN": 0,"LOW": 0,
    "MEDIUM": 0,"HIGH": 0,
    "CRITICAL": 0
}

for vul in vuls:
    try:
      print(vul.lower() + ": " + annotations['trivy.security.devopstales.io/' + vul.lower()])
    except:
      continue

#for obj in annotations:
#  print(obj)