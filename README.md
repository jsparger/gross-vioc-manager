# gross-vioc-manager
Create, start, and stop vioc VMs in a disgusting way

### Requirements:

Requires virtualbox, vagrant and vbguest plugin. Tested with virtualbox 5.1.34 and vagrant 2.1.2.

```
vagrant --version
# Vagrant 2.1.2

vagrant plugin install vagrant-vbguest
```

### Installation:

```
git clone https://github.com/jsparger/gross-vioc-manager.git
cd gross-vioc-manager
git checkout absolute-minimum
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run:

```
export FLASK_APP=gross_vioc_manager
export FLASK_ENV=development
flask run
```

### API:

```
# run vagrant command for a hostname of your choice
# valid GET commands: "status"
# valid POST commands: "destroy", "halt", "reload", "resume", "suspend", "up"
gross/vm/<hostname>/<command>
```

### examples:

Get status of uncreated VM
```
curl -i -X GET localhost:5000/vm/dog/status
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 76
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Wed, 18 Jul 2018 15:06:55 GMT

[
    [
        "vioc",
        "not_created",
        "virtualbox"
    ]
]
```

Create VM
```
curl -i -X POST localhost:5000/vm/dog/up
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 40
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Wed, 18 Jul 2018 15:08:57 GMT

"Calling up on host dog was successful"
```

Get status of new VM
```
curl -i -X GET localhost:5000/vm/dog/status
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 72
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Wed, 18 Jul 2018 15:11:00 GMT

[
    [
        "vioc",
        "running",
        "virtualbox"
    ]
]
```
