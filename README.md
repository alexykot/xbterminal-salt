# README #


## Installation ##

### install software ###
```
Install salt-master, salt-api 2015.8.3+
Install MongoDB 3.0+
Install git
Install nginx
```

### Create salt-master directory structure ###
```
#!bash
mkdir /srv/salt/states/{base,stage,dev}
mkdir /srv/salt/reactor
mkdir /srv/salt/formulas
```

### Configure salt-master ###
Example /etc/salt/master
```
#!yaml
rest_cherrypy:
  port: 8000
  host: 127.0.0.1
  disable_ssl: True
  thread_pool: 10
  collect_stats: True

external_auth:
  pam:
    salt-xbt-dev:
      - pkg.*
      - test.*
      - '@wheel'
      - '@jobs'
      - 'state.*'
      - system.*
      - grains.*

token_expire: 3600

log_level_logfile: debug

file_roots:
  base:
    - /srv/salt/states/base/
  dev:
    - /srv/salt/states/dev/
  stage:
    - /srv/salt/states/stage/

top_file_merging_strategy: same

reactor:
  - 'xbt/terminal/highstate':
    - /srv/salt/reactor/xbt/terminal/savepillars.py
  - 'salt/job/*/ret/*':
    - /srv/salt/reactor/salt/job/ret/savejid.py

ext_pillar:
  - mongo: {collection: xbt_pillars, id_field: _id, fields: [xbt,jid]}

mongo.db: 'salt'
mongo.host: '127.0.0.1'
mongo.port: 27017
```

### Configure states tops systems ##

Set in /srv/salt/states/{base,stage,dev}/top.sls
Change env name

```
#!yaml
base:
  '*':
    - xbterminal-firmware
```

### Install  xbterminal-salt ###
Symlink xbterminal-fimware folder from formualas to  /srv/salt/states/{base,stage,dev}xbterminal-firmware

```
#!bash
cd /srv/salt/states/base
ln -s ../../formulas/xbterminal-firmware/xbterminal-firmware
```

### Install grains ###

```
#!bash
mkdir /srv/salt/states/base/_grains
cd /srv/salt/states/base/_grains
ln -s ../../formulas/xbterminal-firmware/_grains/xbt.py
```

### Instal Reactors ###
Reactor does not care about env's

```
#!bash
mkdir -p /srv/salt/reactor/xbt/terminal/
mkdir -p /srv/salt/reactor/salt/job/ret/
cd /srv/salt/reactor/xbt/terminal/
ln -s  ../../../formulas/xbterminal-firmware/reactors/savepillars.py 
ln -s ../../../formulas/xbterminal-firmware/reactors/savejid.py
```

### Configre nginx ###

Configure nginx
```
server {
  listen 443 ssl;
  ....
  location / { 	proxy_pass http://127.0.0.1:8000/;   }
}
```

### restart and enable all services ###

Startup sequence
```
mongodb
salt-master
salt-api
nginx
```


### check  api is working ###
adduser salt-xbt-dev
set password

### ###
```
#!bash
curl -sSk https://localhost:8000/login \
     -H 'Accept: application/x-yaml' \
     -d username=salt-xbt-dev \
     -d password=eeaa71eaad089e98bd0fc713f9878cc2 \
     -d eauth=pam
```
