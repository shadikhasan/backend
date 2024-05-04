import requests
import json
def aws_map_route_api(source_lat, source_lon, dest_lat, dest_lon, OptimizeFor):
    api_url = 'https://skay3kwtcg.execute-api.ap-south-1.amazonaws.com/Prod/route/'
    payload = {
        "source_lat": source_lat,
        "source_lon": source_lon,
        "dest_lat": dest_lat,
        "dest_lon": dest_lon,
        "optimize_for": OptimizeFor
    }
    try:
        response = requests.post(api_url, json=payload).json()
        data = json.loads(response['data'][0])
        return data         # dict of  DriveDistance, DistanceUnit, DriveTime, TimeUnit, PathList
    except Exception as e:
        print("errors :", e)
