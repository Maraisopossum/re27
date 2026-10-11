import json, time, urllib.request, urllib.parse
MIRRORS = ["https://overpass-api.de/api/interpreter"]
UA = {"User-Agent": "FamilyTripPlanner/1.0 (benoitdegove@gmail.com)"}


def op(q, tries=3):
    last = None
    for i in range(tries):
        for m in MIRRORS:
            try:
                req = urllib.request.Request(m, data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
                return json.load(urllib.request.urlopen(req, timeout=100))
            except Exception as e:
                last = e
                time.sleep(2)
    raise last
