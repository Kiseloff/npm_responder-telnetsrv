# NPM responder telnetsrv

    docker build --no-cache --network=host -t kiseloff/npm_responder-telnetsrv:latest .
    
    docker run -d -p 8023:8023 \
    --env APP_API_HOST=172.17.0.3 \
    --env APP_API_PORT=5002 \
    -v ~/npm_responder_logs:/usr/src/app/logs \
    --name npm_responder-telnetsrv-app kiseloff/npm_responder-telnetsrv:latest