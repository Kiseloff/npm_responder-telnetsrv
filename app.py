import os
from miniboa import TelnetServer
import requests

from helpers import *
from config import *

# defaults or ENVs
PORT = int(os.getenv('APP_TELNETSRV_PORT', defaults['PORT']))
API_HOST = os.getenv('APP_API_HOST', defaults['API_HOST'])
API_PORT = os.getenv('APP_API_PORT', defaults['API_PORT'])

CLIENTS = []
IDLE_TIMEOUT = defaults['IDLE_TIMEOUT']
BASE_URL = 'http://{}:{}'.format(API_HOST, API_PORT)

def my_on_connect(client):
    log(RUNTIMELOG, "[{}]: Open connection".format(client.address))
    CLIENTS.append(client)
    client.send('Please type <check> for checking NPM connectivity to {}  or <quit> for exit:\n'.format(client.address))
    client.send('# ')


def my_on_disconnect(client):
    log(RUNTIMELOG, "[{}]: Close connection".format(client.address))
    CLIENTS.remove(client)


def kick_idle():
    # Who hasn't been typing?
    for client in CLIENTS:
        if client.idle() > IDLE_TIMEOUT:
            log(RUNTIMELOG, "[{}]: Kicking idle client".format(client.address))
            client.active = False


def process_client():
    for client in CLIENTS:
        if client.active and client.cmd_ready:
            # If the client sends command
            cmd_handler(client)


def cmd_handler(client):
    cmd = client.get_command().lower()
    if cmd:
        log(RUNTIMELOG, "[{}]: says '{}'".format(client.address, cmd))

    # cmd = remove_backspaces(cmd)

    # quit = disconnect
    if cmd == 'quit':
        client.active = False
    # check = check NPM connectivity to client
    elif cmd == 'check':
        url = '/api/check?ip={}'.format(client.address)
        resp = api_request("GET", url, client.address)
        print_results(client, cmd, resp)
    elif cmd == 'version':
        print_results(client, cmd)
    elif cmd == 'api':
        url = '/api/version'
        resp = api_request("GET", url, client.address)
        print_results(client, cmd, resp)
    elif cmd == '':
        pass
    else:
        client.send('OOPS, there is no <{}> command. Try again\n'.format(cmd))

    client.send('# ')


def api_request(method, url, clientIP, headers='', base_url=BASE_URL):
    url = base_url + url
    if not headers:
        headers = {'Accept': 'application/json'}
    try:
        resp = requests.request(method=method, url=url, headers=headers)
    except:
        log(RUNTIMELOG, "[{}]: Error: can't make {} {}".format(clientIP, method, url))
        return {'error': 'failed to establish a new connection to API service'}

    log(RUNTIMELOG, "[{}]: {} {} {}".format(clientIP, method, url, resp.status_code))

    if resp.status_code != 200:
        return {'error': '{} {}'.format(resp.status_code, resp.text)}
    return resp.json()


def print_results(client, cmd, results={}):
    hr = '-' * 30 + '\n'

    if 'error' in results.keys():
        client.send('Error: {}\n'.format(results['error']))
        client.send('Please contact the service administrator.\n')
    elif cmd == 'api':
        # client.send('API version is v{}\n'.format(results['version']))
        client.send('API version is v{}\n'.format(results.get('version', '')))
    elif cmd == 'version':
        client.send('NPM responder is v{}\n'.format(defaults["VERSION"]))
    elif cmd == 'check':
        client.send(hr)
        client.send('Check status is {}\n'
            .format(
            'OK' if (type(results['icmp']) is float) and results['ssh'] and (results['snmpv2c'] or results['snmpv3'])
            else 'FAILED'))
        client.send('[{}] ICMP {}\n'
                    .format('+' if (type(results['icmp']) is float)
                            else '-',
                            '-- ' + str(round(results['icmp'], 2)) + ' ms' if (type(results['icmp']) is float)
                            else ''))
        client.send('[{}] SSH connectivity\n'
                    .format('+' if results['ssh'] else '-'))
        client.send('[{}] SNMPv2c connectivity\n'
                    .format('+' if results['snmpv2c'] else '-'))
        client.send('[{}] SNMPv3 connectivity\n'
                    .format('+' if results['snmpv3'] else '-'))
        client.send(hr)


def main():
    # Create LOG dir if it doesn't exist
    if not os.path.exists(defaults['LOGDIR']):
        os.mkdir(defaults['LOGDIR'])

    server = TelnetServer(port=PORT)
    server.on_connect = my_on_connect
    server.on_disconnect = my_on_disconnect

    print(f"Starting server on port {server.port}. CTRL-C to interrupt.")

    while True:
        try:
            server.poll()  # Send, Recv, and look for new connections
            kick_idle()  # Check for idle clients
            process_client()  # Check for client input
        except KeyboardInterrupt:
            server.stop()
            print("Server shutdown.")
            break


if __name__ == "__main__":
    main()
