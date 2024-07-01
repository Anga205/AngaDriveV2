import reflex as rx
from AngaDriveV2.common import server_config

if server_config['api_url']=="http://localhost:8000":
    config = rx.Config(
        app_name="AngaDriveV2",
    )
elif server_config['deploy_url']=="http://localhost:3000":
    config = rx.Config(
        app_name="AngaDriveV2",
        api_url=server_config['api_url'],
    )
else:
    config = rx.Config(
        app_name="AngaDriveV2",
        api_url=server_config['api_url'],
        deploy_url=server_config['deploy_url'],
    )