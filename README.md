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
now run the windows startup command
```
start.bat
```

### For Debian/Arch/RedHat based systems:

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
bash start.sh
```
this will automatically install all dependencies and start up the webapp
