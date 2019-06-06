# husqvarna-exporter
Basic Prometheus exporter for Husqvarna connect Automowers built to run in Docker or standalone.

## Getting started
In order to run the applications you need an application id from Husqvarna Group. Head over to https://developer.1689.cloud and follow the "Getting started" guide to create an account, create an application and link it to the API's needed. You will need to add "Authentication API" and "Automower Connect API". 

Copy husqvarna-exporter.ini.sample file to husqvarna-exporter.ini and alter the contents to suite your needs. Add the Key from the step above as you app_id.

Second you need to decide if you are running in Docker or not. If not you need to install the contents of the requirements.txt in a virtualenv or globally (you should know how to do this by now...). Otherwise build the docker image as normal.

Now the authentication is an Oauth one so we can keep us logged in using an refresh_token using this token will remove the need to store username/password in a file, you will however need those to create the refresh_token in the first place (this will be the same login as you used to get the Key above). Either run the husqvarna-login.py application to get the refresh_token or add the username/password to you ini file and the docker appliction will log the refresh_token at first run so you can med the configuration and then remove the username/password. 

husqvarna-exporter.py uses two environment variables:
- AM_PORT: port to use for the exporter, default 9109
- AM_CONFIG: full filename for the  .ini file to use for configuration, default 'husqvarna-exporter.ini'

I would sugest you mount the config into your docker image at setup using the -v option. I typically run it like:
```
docker run --restart unless-stopped \
 -p 9109:9109 \
 -v $PWD/husqvarna-exporter.ini:/app/config/husqvarna-exporter.ini \
 --env AM_CONFIG=/app/config/husqvarna-exporter.ini \
 --name husqvarna-exporter
```
