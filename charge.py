import requests
import json
import time
import re

with open(r"config.txt", 'r', encoding="utf8") as f:
    read_input = f.readlines()
    for line in read_input:
        value = re.split(r':', line)
        if value[0] == "url":
            url = value[1].replace("\n", "") + ":8080"
        elif value[0] == "robotResourceId":
            robotResourceId = value[1].replace("\n", "")
        elif value[0] == "chargingStationResourceId":
            chargingStationResourceId = value[1].replace("\n", "")
        elif value[0] == "chargin_station_markerId":
            markerId = value[1].replace("\n", "")
        elif value[0] == "threshold":
            threshold = int(value[1].replace("\n", ""))
        elif value[0] == "exe_times":
            exe_times = int(value[1].replace("\n", ""))

data = json.dumps({
    "name": "ScriptCharge",
    "allocationPolicy": "static",
    "resourceId": "%s" % robotResourceId,
    "tasks": [
        {
            "index": 1,
            "name": "go to charging station",
            "type": "navigating",
            "action": {
                "type": "marker",
                "target": {
                    "markerId": "%s" % markerId,
                    "markerAlias": "",
                    "markerType": "charging_station"
                },
                "tolerance": {
                    "distance": 0,
                    "degrees": 0
                },
                "relative": {
                    "distance": 0,
                    "degrees": 0
                },
                "parameter": {
                    "LoadType": ""
                }
            }
        },
        {
            "index": 2,
            "name": "docking charging station",
            "type": "docking",
            "action": {
                "type": "marker",
                "target": {
                    "markerId": "%s" % markerId,
                    "markerAlias": ""
                },
                "relative": {
                    "distance": 0,
                    "degrees": 0
                },
                "parameter": {
                    "mode": "",
                    "feature": "",
                    "direction": "",
                    "stages": 0,
                    "readCode": False,
                    "loadType": "",
                    "forkType": "",
                    "level": ""
                }
            }
        },
        {
            "index": 3,
            "name": "start charging",
            "type": "start_charging",
            "action": {
                "chargingStationResourceId": "%s" % chargingStationResourceId,
                "threshold": threshold
            }
        },
        {
            "index": 4,
            "name": "stop charging",
            "type": "stop_charging",
            "action": {
                "chargingStationResourceId": "%s" % chargingStationResourceId
            }
        },
        {
            "index": 5,
            "name": "undocking charging station",
            "type": "undocking",
            "action": {
                "type": "marker",
                "target": {
                    "markerId": "%s" % markerId,
                    "markerAlias": ""
                },
                "relative": {
                    "distance": 0,
                    "degrees": 0
                },
                "parameter": {
                    "mode": "",
                    "loadType": "",
                    "forkType": "",
                    "level": ""
                }
            }
        }
    ]
})


def send_job(url, data):
    response = requests.post(url="http://" + "%s" % url + "/api/jobs", data=data)
    print(response.json())
    job_id = response.json()["result"]["jobId"]
    return job_id


def get_job_status(url, job_id):
    response = requests.get(url="http://" + "%s" % url + "/api/jobs/" + "%s" % job_id)
    job_status = response.json()["result"]["job"]["status"]
    print(response.json())
    return job_status


if __name__ == "__main__":
    for i in range(0, exe_times):
        job_id = send_job(url=url, data=data)
        job_status = get_job_status(url=url, job_id=job_id)
        print(job_status, type(job_status))
        while True:
            time.sleep(5)
            if job_status not in ["finished", "exception", "aborted", "canceled"]:
                job_status = get_job_status(url=url, job_id=job_id)
                continue
            else:
                break
