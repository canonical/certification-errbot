import base64
import requests


class C3ApiAgent:
    base_url = "https://certification.canonical.com"
    token_ep = "/oauth2/token/"
    switches_ep = "/api/v2/switches/?datacentre__name="
    hostdata_ep = "/api/v2/hostdata/"
    machine_ep = "/api/v2/machines/"
    network_details_ep = (
        "/api/v2/network-details/?pagination=limitoffset&limit=0&hostdata__datacentre__"
    )
    physicalmachinesview_ep = "/api/v2/physicalmachinesview/"

    def __init__(self, clientid: str, secret: str):
        self.token = None
        self.login(clientid, secret)

    def login(self, client_id: str, secret: str):
        """login with client id and secret to get token"""
        credential = base64.b64encode(
            "{0}:{1}".format(client_id, secret).encode("utf-8")
        ).decode("utf-8")

        response = requests.post(
            f"{C3ApiAgent.base_url}{C3ApiAgent.token_ep}",
            auth=(client_id, secret),
            data={"grant_type": "client_credentials", "scope": "read write"},
        )
        if not response.ok:
            raise RuntimeError("Failed to log in to C3")

        self.token = response.json()["access_token"]

    def get_machine(self, cid: str):
        url = f"{C3ApiAgent.base_url}{C3ApiAgent.machine_ep}{cid}/"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if not response.ok:
            raise RuntimeError(f"Failed to get {cid}, {response.status_code}")
        return response.json()

    def get_physicalmachinesview(self, cid: str):
        url = f"{C3ApiAgent.base_url}{C3ApiAgent.physicalmachinesview_ep}{cid}/"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if not response.ok:
            raise RuntimeError(f"Failed to get {cid}, {response.status_code}")
        return response.json()
