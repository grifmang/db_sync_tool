# db_sync_tool 

# Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Usage](#usage)

### description
A python tool to sync data from local to remote postgresql database
server

### dependencies
python == 2.7
#### required python packages
    configparser==3.5.0
    paramiko==2.1.1
    psycopg2==2.6.2
    pytest==3.0.6
    python-crontab==2.1.1
    requests==2.13.0
    tornado==4.4.2
    virtualenv==15.1.0


#### other dependencies
  - a fully functional postgresql server (on both local and remote)
  - corseco-dashboard application deployed on both local and remote with all migrations done.


## deployment
after successfully deploying corseco-dashboard on both remote and local with database migrated with all 
required schema and tables.
  - create a virtual environment with virtualenvwrapper tool (provided it is already installed) and activate
    it and the run following command in the project top level directory.

```sh
pip freeze -r requirements.txt

```
  - copy the ssh public key of local machine on remote machine at .ssh/authorized_keys.
  - create an entry of the remote server's ssh connection parameters in REMOTE_SERVER_CREDENTIAL variable at 
  'components/conf/settings.py'

```python
# REMOTE SERVER CREDENTIALS
REMOTE_SERVER_CREDENTIAL = {
    "my_lubuntu_vm": {
        "host": "192.168.1.33",
        "port": 22,
        "username": "luvm",
    },
    "remote_vps": {
        "host": "128.199.241.163",
        "port": 22,
        "username": "root",
    }
}

```

  - initialize the PASS_PHRASE variable at 'components/conf/settings.py' with local machine's ssh private 
    key pass phrase (if pass phrase is set) 

```python
# local machine ssh private key pass phrase
PASS_PHRASE = "your pass phrase"

```
  - now run the following command with virtual environment with all dependencies activated.

```sh
python setup_configuration.py
```


## usage
since all the cron jobs and daemons are set by setup_configuration.py script, therfore we don't need to
run any special command, just make new entries in local database and wait for max 5 minutes for the db_dump_exporter
running through the cron job.
