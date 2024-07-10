# AngaDriveV2

A remove file and collection hosting web application written in python using the reflex framework

## Tech stack
- Reflex (to transpile the frontend to a Next.js application)
- FastAPI (to quickly and efficiently serve CDN)
- SQLite (because it's relatively portable)
- Cloudflare tunnel api (because airtel doesnt like it when i do port forwarding)

## Hardware requirements
- at least 1GB ram
- a CPU with a clock speed of at least 2.00GHz
- more than 500MB storage for all the dependencies

## Software requirements

- NodeJS v18+
- Python3

## Self Hosting guide (non-docker)

### for Windows (and other DOS based systems)

first, open command prompt copy the repository into your filesystem using

```
git clone https://github.com/Anga205/AngaDriveV2
```
this will create a folder named `AngaDriveV2`, enter it using
```
cd AngaDriveV2
```
now setup a virtual environment, for this you may need `virtualenv` installed beforehand
<details>
<summary>How to install virtualenv using pip</summary>

To install virtualenv using pip, follow these steps:

1. Open your command prompt or terminal.
2. Run the following command to install virtualenv:
    ```
    pip install virtualenv
    ```
3. Wait for the installation to complete. Once it's done, you should see a success message.

</details>

```
py -m venv venv
```

enter the virtual environment:
```
venv\Scripts\activate
```
initialize and reflex:
```
reflex init
reflex run
```

### For Debian based systems:

open bash copy the repository into your filesystem using

```
git clone https://github.com/Anga205/AngaDriveV2
```
this will create a folder named `AngaDriveV2`, enter it using
```
cd AngaDriveV2
```
now you can quick-start the app using the startup script
```
bash debian.sh
```
this will automatically install all dependencies and start up the webapp

### For Arch and Redhat based systems
~~go away nobody thinks you're distro is cool, touch grass~~

To install and run the application on Arch Linux and Redhat-based systems, follow these steps:

1. Open your terminal.

2. Clone the repository into your filesystem using the following command:
    ```
    git clone https://github.com/Anga205/AngaDriveV2
    ```

3. Navigate to the cloned repository by running:
    ```
    cd AngaDriveV2
    ```

4. Install the necessary dependencies by executing the following command:
    ```
    sudo pacman -S python3 nodejs curl python3-venv unzip
    ```

5. Set up a virtual environment by running the following command:
    ```
    python -m venv venv
    ```

6. Activate the virtual environment:
    ```
    source venv/bin/activate
    ```

7. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

8. Initialize and run reflex:
    ```
    reflex init
    reflex run
    ```

    ## License

    This project is licensed under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html). Please see the [LICENSE](LICENSE) file for more details.
