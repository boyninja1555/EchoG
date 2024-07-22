import http.client
import platform

def get_system_info():
    system = platform.system()
    release = platform.release()
    architecture = platform.machine()
    return f"{system} {release}; {architecture}"

def send_http_request(protocol, url, subpath):
    if protocol == "echob":
        system_info = get_system_info()
        custom_user_agent = f"EchoB/1.0 ({system_info})"

        client = http.client.HTTPConnection("104.190.162.141", 1010)
        client.request("GET", f"/{url}/{subpath or ""}", headers={"User-Agent": custom_user_agent})
        response = client.getresponse()

        return { "status": response.status, "body": response.read().decode() }
