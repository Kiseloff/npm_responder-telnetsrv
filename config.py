defaults = {
    'PORT': 8023,
    'IDLE_TIMEOUT': 30,
    'RUNTIMELOG': 'telnetsrv_runtime.log',
    'LOGDIR': './logs',
    'VERSION': '2.0.2',
    'API_HOST': 'localhost',
    'API_PORT': 5001,
}

RUNTIMELOG = '/'.join([defaults['LOGDIR'], defaults['RUNTIMELOG']])
