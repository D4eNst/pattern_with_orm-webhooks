from data.config import settings

DEBUG = settings.DEBUG

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'sqlalchemy.engine': {
            'handlers': ['default'],
            'level': 'WARNING',  # set INFO to see SQL Alchemy logs (raw queries, execution time, ect)
            'propagate': False
        },
        'uvicorn': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.error': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
