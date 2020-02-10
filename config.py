defaults = {
    'PORT': 8023,
    'IDLE_TIMEOUT': 30,
    'RUNTIMELOG': 'telnet_runtime.log',
    'LOGDIR': './logs',
    'VERSION': '2.0.1',
    'API_HOST': 'localhost',
    'API_PORT': 5001,
}

RUNTIMELOG = '/'.join([defaults['LOGDIR'], defaults['RUNTIMELOG']])
