import http.client
import platform
import config

def get_system_info():
    system = platform.system()
    release = platform.release()
    architecture = platform.machine()
    return f"{system} {release}; {architecture}"

def send_http_request(protocol: str, url: str, subpath: str):
    if protocol == config.PROTOCOL:
        system_info = get_system_info()
        custom_user_agent = f"{config.NAME}/{config.VERSION} ({system_info})"

        client = http.client.HTTPConnection("104.190.162.141", 1010)
        client.request("GET", f"/{url}/{subpath or ""}", headers={"User-Agent": custom_user_agent})
        response = client.getresponse()

        return { "status": response.status, "body": response.read().decode() }
    else:
        return { "status": 400, "body": "Invalid protocol" }
