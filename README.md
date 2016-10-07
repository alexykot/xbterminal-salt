# README #


## Installation ##

### install software ###
```
Install salt-master, salt-api 2015.8.3+
Install MongoDB 3.0+
Install git
Install nginx
install gitfs https://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html
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

fileserver_backend:
  - git


gitfs_provider: gitpython
gitfs_base: master

gitfs_remotes:
  - file:///srv/salt/xbterminal-salt/:
    - name: states
    - root: states
    - mountpoint: salt://
    - base: master



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

top_file_merging_strategy: same

reactor:
  - 'xbt/terminal/highstate':
    - salt://_reactors/savepillars.py
  - 'salt/job/*/ret/*':
    - salt://_reactors/savejid.py


ext_pillar:
  - mongo: {collection: xbt_pillars, id_field: _id, fields: [xbt,jid]}

mongo.db: 'salt'
mongo.host: '127.0.0.1'
mongo.port: 27017
```

### Install project ###
clone this repo to file:///srv/salt/xbterminal-salt/

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
