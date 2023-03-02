# Odoo ESC/POS printer proxy

## Contents

1. [Usage](#Usage)
    1. [Production](#Production)
    2. [Development](#Development)
1. [Instalation](#Instalation)
1. [Contributors](#Contributors)

## Usage
In order to help with the comunication between ESC/POS printers and Odoo. We've developed a simple flask served server to handle request and printing locally. This server works as a proxy from our odoo instance and the printer, therefore to use this server you'll require:

* Send and/or receive HTTP requests (This is probably done using our odoo instance)
* Printer with ESC/POS standard
* Printer MUST be on the same network

_Reminder: This server is supposed to be working on-premise only. Do not host over the web as comunication with printing devices must be local._

### Commands

The server offers a short variety of functions, wich can be accessed through an API request. To access any function we'll have to use a structure resembling:

`<url>/<function>/<printer_ip>`

Decomposing this structure we have three main elements:

* _Url_: This is how we access our flask server. Usually this is a URL or IP address of the host machine.

* _Function_: Printer handler support some actions as cutting papper, and various printing methods. ([Functions](#Functions))

* _printer_ip_: Printer ipv4 address.

#### Functions

__cut__: Printers supporting cutting functionalities can be requested to cut the papper.

__status__: Gets printer status. This status can only be active/inactive. *Expects simple GET request returns a json with the status.*

__text__: Printing text format data. *Expects POST request with a string on the data response header*

__block__: Printing text format data on blocks. *Expects POST request with a string on the data response header*

__img__: Printing from a binary image file. *Expects POST request with a string of a binary image on the data response header*

### Logging

To be able to handle errors and to keep an eye on what and how something is interacting with our server on installing some log files are configured in order to help achive just that. Accessing log files can be done from:

`PRINTER_PROXY/dist/logs`

There we have 2 separate logs files:

* server.err.log : To log STDERR.
* server.log : To log STDOUT.

_Note: Logging is only supported when running from install.bat file._



## Instalation 

The server is ready to install off the shelf, but understanding the needs of the users may extend this project consist of deployment or development routes of implementation. Source code is on the _main.py_ file located on the root folder of the project. Production package is inside the dist folder on root folder.

### Production

Getting ready with the off the shelf install is really easy. Navigate into the dist folder and locate `install.bat` file. Right-click the file and run as System Administrator (run as administrator). Once the .bat file has been run server should be ready to go.

You can check if the installation went right by doing:
1. Open powershell or CMD

2. Get installed nssm services

`Get-WmiObject win32_service | ?{$_.PathName -like '*nssm*'} | select Name, DisplayName, State, PathName`

3. You should see

![proxyPrinter](./public/verify-install.png)

### Development

This server can be further extended easily. Using the main.py file we can add or remove functionalities from the server, doing so will require an understanding of python and flask apps. A project once modified (main.py) can be compiled and re-installed.

To start development you'll be required to install simple project requirements, on the root folder run:

`pip install -r requirements.txt`

#### Recompiling the code

Code can be recompiled using pyinstaller module. Wich can be obtained from Pypi libraries using:

`pip install -U pyinstaller`

Once pyinstaller is up and running. Compiling our code can be done by using the following command:

`pyinstaller --onefile main.py --hidden-import=win32timezone --clean --uac-admin`

## Contributors

- Christopher Suazo <christophersuazop@gmail.com>
