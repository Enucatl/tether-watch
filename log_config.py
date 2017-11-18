def log_config(verbose):
    levels = [
        'INFO',
        'DEBUG',
    ]
    verbose = min(len(levels) - 1, verbose)
    return dict(
        version = 1,
        disable_existing_loggers = False,
        formatters = {
            'f': {'format':
                  '%(asctime)s %(levelname)-8s %(message)s'
                 }
        },
        handlers = {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': levels[verbose],
            },
        },
        root = {
            'handlers': ['console'],
            'level': levels[verbose],
        },
    )
