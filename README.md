[![Build Status](https://travis-ci.org/alesolda/bluserver.svg?branch=master)](https://travis-ci.org/alesolda/bluserver)
 [![codecov](https://codecov.io/gh/alesolda/bluserver/branch/master/graph/badge.svg)](https://codecov.io/gh/alesolda/bluserver)

# bluserver

Receives operational data through sockets, processes it based on predefined logic,
returns computed results to the sender; manages multiple client connections with
reliable communication and data integrity.

---

This excercise implements a socket server (python) built with the following features:

* python 3.6.6
* support of multiple concurrent client connections using [selectors](https://docs.python.org/3/library/selectors.html)
* number of sub-processes configurable per client
* receive information using sockets
* communication between processes through pipes
* calculations module implemented with [ply](https://github.com/dabeaz/ply)
* [structlog](https://www.structlog.org/en/stable/)
* some demostrative unit tests with [pytest](https://pytest.org/)
* dockerfile with a makefile handler
* package with python [wheel](https://pypi.org/project/wheel/)

## Prerequisites

* python 3.6.6
* [pip](https://pypi.org/project/pip/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
* [docker](https://www.docker.com/)

## Usage

If you already have `docker`, just run:

```bash
make docker-run-server

# only tests
make docker-tests
```

To gracefully terminate the server, from a terminal execute:
```bash
killall bluserver -s SIGINT
```

The default settings for the server are:
* `address`: localhost
* `port`: 1982
* `number-processes`: 2
* `verbose`: false

## Devel flavor installation

For manually installing and running the server you will need to:

```bash
# 1. Create a virtualenv
mkvirtualenv -p python3.6 bluserver

# 2. Activate virtualenv
workon bluserver

# 2. Install requirements
pip install -r requirements.txt

# 3. Install bluserver package
python setup.py develop

# 4. And finally, run the server:
bluserver --verbose
```

To kill the server, simply press `CTR-C`, or from a different terminal execute `killall bluserver -s SIGINT`

## Client

To test the server you have a simple tiny client written in python inside the `bluserver/client/` folder.

To run this client you need to:
```bash
# 1. Activate the previously created virtualenv
workon bluserver

# 2. Execute the client
python client.py
```

All client parameters are in the same scrip:

```python
# Input file which will be sent to the server
INPUT_FILE = './operations.txt'

# Where to write the results
OUTPUT_FILE = './output.txt'

# Where is listening the server
ADDRESS = ('localhost', 1982)
```

## Misc

### Wheel Package

You can build the wheel package for bluserver executing:
```bash
# with docker
make docker-build-wheel

# or using the previously virtualenv
python setup.py bdist_wheel
```

### Syslog

Bluserver is capable of logging to a syslog, for this you will need to install and setup a syslog (for example the `rsyslog` flavor), and then
enable it through the settings file `bluserver/logging.yml`:

change the line `  handlers: []` by `   handlers: [syslog]`

### Logging example
```
[bluserver] 2018-09-24 07:44:10,584: INFO uuid=None pname='server' pid=37 event='Blu Server invoked' cli_args=Namespace(address='0.0.0.0', number_processes='2', port='1982', verbose=True)
[bluserver] 2018-09-24 07:44:10,584: INFO uuid=None pname='server' pid=37 event='Cli arguments parse'
[bluserver.server] 2018-09-24 07:44:10,584: INFO uuid=None pname='server' pid=37 event='Start server'
[bluserver.server] 2018-09-24 07:46:15,559: INFO uuid=None pname='server' pid=37 event='Incoming connection' conn=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.17.0.2', 1982), raddr=('172.17.0.1', 52088)> addr=('172.17.0.1', 52088)
[bluserver.server] 2018-09-24 07:46:15,559: INFO uuid=None pname='server' pid=37 event='Forked process for incoming connection' process='Process-1'
Generating LALR tables
[bluserver.client_manager] 2018-09-24 07:46:15,569: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Manage client started' client=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.17.0.2', 1982), raddr=('172.17.0.1', 52088)>
[bluserver.tools] 2018-09-24 07:46:15,569: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Starting to receive data from client' bytes=8
[bluserver.tools] 2018-09-24 07:46:15,569: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Received data from client' bytes=8
[bluserver.client_manager] 2018-09-24 07:46:15,570: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Client informed data size' bytes=9755144
[bluserver.tools] 2018-09-24 07:46:15,570: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Starting to receive data from client' bytes=9755144
[bluserver.tools] 2018-09-24 07:46:15,672: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Received data from client' bytes=9755144
[bluserver.client_manager] 2018-09-24 07:46:15,707: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='2 processes will be used to parallelize computations'
[bluserver.client_manager] 2018-09-24 07:46:15,707: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Data slice calculated (lines)' slice=slice(0, 150002, None)
[bluserver.client_manager] 2018-09-24 07:46:15,717: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Process created' name='Process-1:1'
[bluserver.client_manager] 2018-09-24 07:46:15,717: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Data slice calculated (lines)' slice=slice(150002, -1, None)
[bluserver.client_manager] 2018-09-24 07:46:15,718: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Process created' name='Process-1:2'
[bluserver.client_manager] 2018-09-24 07:46:15,721: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:1' pid=45 event='Started sub process calculation'
[bluserver.client_manager] 2018-09-24 07:46:15,725: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Process started' name='Process-1:1'
[bluserver.client_manager] 2018-09-24 07:46:15,728: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:2' pid=46 event='Started sub process calculation'
[bluserver.client_manager] 2018-09-24 07:46:15,731: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Process started' name='Process-1:2'
[bluserver.client_manager] 2018-09-24 07:46:15,731: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event="All child's pipe endpoints were closed"
[bluserver.client_manager] 2018-09-24 07:46:16,747: ERROR uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:1' pid=45 event='Could not compute expression' expression='import sys;sys.exit()'
[bluserver.client_manager] 2018-09-24 07:46:16,861: ERROR uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:1' pid=45 event='Could not compute expression' expression='import time;time.sleep(3600)'
[bluserver.client_manager] 2018-09-24 07:46:32,823: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:1' pid=45 event='Pipe calculation results to parent' items=150000
[bluserver.client_manager] 2018-09-24 07:46:32,824: ERROR uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:2' pid=46 event='Could not compute expression' expression='import sys;sys.exit()'
[bluserver.client_manager] 2018-09-24 07:46:32,831: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:1' pid=45 event='Subprocess terminated'
[bluserver.client_manager] 2018-09-24 07:46:32,843: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Received calculations from child'
[bluserver.client_manager] 2018-09-24 07:46:33,027: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:2' pid=46 event='Pipe calculation results to parent' items=150000
[bluserver.client_manager] 2018-09-24 07:46:33,034: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='Process-1:2' pid=46 event='Subprocess terminated'
[bluserver.client_manager] 2018-09-24 07:46:33,044: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Received calculations from child'
[bluserver.client_manager] 2018-09-24 07:46:33,219: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Joined process' process=<Process(Process-1:1, stopped)>
[bluserver.client_manager] 2018-09-24 07:46:33,219: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Joined process' process=<Process(Process-1:2, stopped)>
[bluserver.client_manager] 2018-09-24 07:46:33,220: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Calculations done in 17.500876665115356 seconds'
[bluserver.tools] 2018-09-24 07:46:33,220: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Sent data to client' bytes=8
[bluserver.client_manager] 2018-09-24 07:46:33,220: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Client was informed about result size' bytes=2997510
[bluserver.tools] 2018-09-24 07:46:33,224: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Sent data to client' bytes=2997510
[bluserver.client_manager] 2018-09-24 07:46:33,224: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Results sent to client'
[bluserver.client_manager] 2018-09-24 07:46:33,224: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Client connection gracefully shutdown'
[bluserver.client_manager] 2018-09-24 07:46:33,231: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Client connection closed'
[bluserver.client_manager] 2018-09-24 07:46:33,231: INFO uuid='ea586c26-bfcd-11e8-a089-0242ac110002' pname='manage_client' pid=43 event='Manage client terminated'
[bluserver.server] 2018-09-24 07:47:14,300: INFO uuid=None pname='server' pid=37 event='Incoming connection' conn=<socket.socket fd=7, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.17.0.2', 1982), raddr=('172.17.0.1', 52100)> addr=('172.17.0.1', 52100)
[bluserver.server] 2018-09-24 07:47:14,301: INFO uuid=None pname='server' pid=37 event='Forked process for incoming connection' process='Process-2'
[bluserver.client_manager] 2018-09-24 07:47:14,305: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Manage client started' client=<socket.socket fd=7, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.17.0.2', 1982), raddr=('172.17.0.1', 52100)>
[bluserver.tools] 2018-09-24 07:47:14,306: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Starting to receive data from client' bytes=8
[bluserver.tools] 2018-09-24 07:47:14,306: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Received data from client' bytes=8
[bluserver.client_manager] 2018-09-24 07:47:14,306: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Client informed data size' bytes=9755144
[bluserver.tools] 2018-09-24 07:47:14,306: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Starting to receive data from client' bytes=9755144
[bluserver.tools] 2018-09-24 07:47:14,408: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Received data from client' bytes=9755144
[bluserver.client_manager] 2018-09-24 07:47:14,442: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='2 processes will be used to parallelize computations'
[bluserver.client_manager] 2018-09-24 07:47:14,442: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Data slice calculated (lines)' slice=slice(0, 150002, None)
[bluserver.client_manager] 2018-09-24 07:47:14,452: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Process created' name='Process-2:1'
[bluserver.client_manager] 2018-09-24 07:47:14,452: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Data slice calculated (lines)' slice=slice(150002, -1, None)
[bluserver.client_manager] 2018-09-24 07:47:14,453: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Process created' name='Process-2:2'
[bluserver.client_manager] 2018-09-24 07:47:14,456: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:1' pid=49 event='Started sub process calculation'
[bluserver.client_manager] 2018-09-24 07:47:14,459: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Process started' name='Process-2:1'
[bluserver.client_manager] 2018-09-24 07:47:14,462: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:2' pid=50 event='Started sub process calculation'
[bluserver.client_manager] 2018-09-24 07:47:14,466: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Process started' name='Process-2:2'
[bluserver.client_manager] 2018-09-24 07:47:14,466: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event="All child's pipe endpoints were closed"
[bluserver.client_manager] 2018-09-24 07:47:15,501: ERROR uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:1' pid=49 event='Could not compute expression' expression='import sys;sys.exit()'
[bluserver.client_manager] 2018-09-24 07:47:15,615: ERROR uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:1' pid=49 event='Could not compute expression' expression='import time;time.sleep(3600)'
[bluserver.client_manager] 2018-09-24 07:47:31,336: ERROR uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:2' pid=50 event='Could not compute expression' expression='import sys;sys.exit()'
[bluserver.client_manager] 2018-09-24 07:47:31,351: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:1' pid=49 event='Pipe calculation results to parent' items=150000
[bluserver.client_manager] 2018-09-24 07:47:31,358: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:1' pid=49 event='Subprocess terminated'
[bluserver.client_manager] 2018-09-24 07:47:31,368: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Received calculations from child'
[bluserver.client_manager] 2018-09-24 07:47:31,537: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:2' pid=50 event='Pipe calculation results to parent' items=150000
[bluserver.client_manager] 2018-09-24 07:47:31,544: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='Process-2:2' pid=50 event='Subprocess terminated'
[bluserver.client_manager] 2018-09-24 07:47:31,554: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Received calculations from child'
[bluserver.client_manager] 2018-09-24 07:47:31,734: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Joined process' process=<Process(Process-2:1, stopped)>
[bluserver.client_manager] 2018-09-24 07:47:31,734: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Joined process' process=<Process(Process-2:2, stopped)>
[bluserver.client_manager] 2018-09-24 07:47:31,734: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Calculations done in 17.280538320541382 seconds'
[bluserver.tools] 2018-09-24 07:47:31,734: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Sent data to client' bytes=8
[bluserver.client_manager] 2018-09-24 07:47:31,735: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Client was informed about result size' bytes=2997510
[bluserver.tools] 2018-09-24 07:47:31,738: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Sent data to client' bytes=2997510
[bluserver.client_manager] 2018-09-24 07:47:31,739: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Results sent to client'
[bluserver.client_manager] 2018-09-24 07:47:31,739: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Client connection gracefully shutdown'
[bluserver.client_manager] 2018-09-24 07:47:31,739: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Client connection closed'
[bluserver.client_manager] 2018-09-24 07:47:31,739: INFO uuid='0d5aea22-bfce-11e8-be4a-0242ac110002' pname='manage_client' pid=47 event='Manage client terminated'
```
