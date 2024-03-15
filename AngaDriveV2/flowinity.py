import requests, uuid
import reflex as rx
from AngaDriveV2.State import State
from AngaDriveV2.DBMS import *

client_secret = "cca650f9-02b2-4772-81aa-02c3c9fa5ed1"

def get_data(token):
    url="https://images.flowinity.com/api/v3/oauth/user"
    params= {
        "Authorization" : token,
        "X-Tpu-App-Id": client_secret
    }
    response=requests.get(url, headers=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

class VerifierState(State):

    def load_verifier_page(self):
        self.load_any_page()
        flowinity_code = self.router.page.params.get("code",None)
        if flowinity_code == None:
            yield rx.window_alert("Looks like an error occured, please try again.")
            yield rx.redirect(f"https://privateuploader.com/oauth/{client_secret}")
        else:
            user_data = get_data(flowinity_code)
            if user_data == None:
                yield rx.window_alert("Looks like an error occured, please try again.")
                yield rx.redirect(f"https://privateuploader.com/oauth/{client_secret}")
            else:
                return rx.window_alert("success")

def verifier():
    return rx.chakra.text("Please wait while AngaDrive gets your data from Flowinity...")