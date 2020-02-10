# npm_responder

##### Test Application

Python 3.7 is recommended

    mkdir npm_responer
    cd ./npm_responer/
    git clone https://github.com/Kiseloff/npm_responder.git .
    
    python3 -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r ./requirements.txt
    
    python ./npm_responder.py [-p <PORT> -c <COMMUNITY> -v] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

##### Build Docker image  

    git clone https://github.com/Kiseloff/npm_responder.git
    cd ./npm_responder
    docker build --no-cache --network=host -t npm_responder:<VERSION> .
    
    # push to hub.docker.com
    docker tag npm_responder:<VERSION> kiseloff/npm_responder:<VERSION>
    docker login
    docker push kiseloff/npm_responder:<VERSION>
    
##### Pull docker image

    docker pull kiseloff/npm_responder:latest
    
##### Show application version

    docker run -it --rm --name npm_responder-app kiseloff/npm_responder:<VERSION> -v

##### Run Docker container
    
    docker run -it -p <PORT>:<PORT> \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-app kiseloff/npm_responder:<VERSION> \
    [-p <PORT> -c <COMMUNITY>] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

##### Run Docker container as a daemon

    docker run -d -p <PORT>:<PORT> \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-app kiseloff/npm_responder:<VERSION> \
    [-p <PORT> -c <COMMUNITY>] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

    <PORT> - application listening port (default 8023)
    <COMMUNITY> - SNMPv2c RO community string (default 'public')
    <USERNAME> - SSH/SNMPv3 username
    <SNMPV3_SECRET> - SNMPv3 secret
    <SSH_SECRET> - SSH secret

##### Change default SNMPv3 secret

    docker pull kiseloff/npm_responder:<VERSION>
    docker run -it --entrypoint python --name npm_responder-passwd kiseloff/npm_responder:<VERSION> passwd.py
    docker commit npm_responder-passwd kiseloff/npm_responder:newpass

    docker run -d -p <PORT>:<PORT> \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --entrypoint python \
    --name npm_responder-app kiseloff/npm_responder:newpass \
    ./npm_responder.py [-p <PORT> -c <COMMUNITY>] -u <USERNAME> --snmpv3-secret <SNMPV3_SECRET> --ssh-secret <SSH_SECRET>

##### Remove docker container and image

    docker rm -f npm_responder-app && docker rmi -f kiseloff/npm_responder:<VERSION>

##### CI/CD
    
[CI/CD Manual](https://www.digitalocean.com/community/tutorials/how-to-configure-a-continuous-integration-testing-environment-with-docker-and-docker-compose-on-ubuntu-14-04#step-3-%E2%80%94-create-the-%E2%80%9Chello-world%E2%80%9D-python-application)
    
    docker-compose -f ./docker-compose.test.yml -p ci build
    docker-compose -f ./docker-compose.test.yml -p ci up -d

    docker logs -f ci_sut_1
    docker wait ci_sut_1

##### Example

    docker run -d -p 8023:8023 \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-app kiseloff/npm_responder:latest \
    -u SOME_USER --snmpv3-secret SOME_SNMP_PASS --ssh-secret SOME_SSH_PASS