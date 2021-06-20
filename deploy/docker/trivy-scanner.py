#!/usr/bin/env python3
from flask import Flask, request, jsonify
import os
import sys
import json
import subprocess

# Download trivy cache
TRIVY_CACHE = ["trivy", "-q", "-f", "json", "fs", "/app"]
trivy_cache_result = (
    subprocess.check_output(TRIVY_CACHE).decode("UTF-8")
)

admission_controller = Flask(__name__)

# POST route for Admission Controller  
@admission_controller.route('/validate', methods=['POST'])

# Admission Control Logic
def deployment_webhook():
    request_info = request.get_json()
    uid = request_info["request"].get("uid")
    result_cache = {}
    vul_list = {}

# Debug
#    try:
#       print(request_info, file=sys.stderr)
#    except:
#       print("request: FAILED", file=sys.stderr)
## Debug

# Main Logic
    try:
      print("request: " + uid, file=sys.stderr)
      # get the images
      containers = request_info["request"]["object"]["spec"]["containers"]
      for obj in containers:
        image_name=obj['image']
        if image_name in result_cache.keys():
            continue
        image_name = image_name.strip(" \"'").strip()
        if len(image_name) == 0:
            continue
        # scan images
        print("Scanning " + image_name, file=sys.stderr)
        TRIVY = ["trivy", "-q", "i", "-f", "json", image_name]
        # --ignore-policy trivy.rego
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

# Debug
      # Log vulnerabilities from image
      for severity in vul_list[image_name].keys():
        vul_num = vul_list[image_name][severity]
        print(severity + ": " + str(vul_num), file=sys.stderr)
## Debug

      # Get vulnerabilities from annotations
      print("Gather annotations:", file=sys.stderr)
      annotations = request_info["request"]["object"]["metadata"]["annotations"]
      vul_annotations= {
            "UNKNOWN": 0,"LOW": 0,
            "MEDIUM": 0,"HIGH": 0,
            "CRITICAL": 0
        }
      for sev in vul_annotations:
        try:
# Debug
          print(sev + ": " + annotations['trivy.security.devopstales.io/' + sev.lower()], file=sys.stderr)
## Debug
          vul_annotations[sev["Severity"]] = int(annotations['trivy.security.devopstales.io/' + sev.lower()])
        except:
          continue

      # Check vulnerabilities
      print("Check vulnerabilities:", file=sys.stderr)
      for sev in vul_annotations:
        try:
          an_vul_num = vul_annotations[sev]
          vul_num = vul_list[image_name][sev]
          if vul_num > an_vul_num:
            print(sev + " is bigger", file=sys.stderr)
            return k8s_response(False, "Too much vulnerability in the image")
          else:
            print(sev + " is ok", file=sys.stderr)
        except:
          continue

      return k8s_response(True, "All Image is OK")
    except:
      print("request: " + uid + " FAILED", file=sys.stderr)
      return k8s_response(True, "Error in mail Logic")

# Function to respond back to the Admission Controller
def k8s_response(allowed, message):
    return jsonify({"response": {"allowed": allowed, "status": {"message": message}}})

if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', ssl_context=("server.pem", "server.pem"), debug=True)

