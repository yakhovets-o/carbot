def get_logg_conf() -> dict:
    return {
        "version": 1,
        'disable_existing_loggers': False,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "logger_conf/loggers.log",
                "encoding": "utf-8",
                "mode": "w",
                "level": "INFO"

            },
            "streamHandler": {
                "formatter": "myFormatter",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "level": "INFO"

            },

        },
        "loggers": {
            "": {
                "handlers": [
                    "fileHandler",
                    "streamHandler"
                ],
                "level": "INFO"

            }
        },
        "formatters": {
            "myFormatter": {
                "format": "%(asctime)s : %(name)s : %(levelname)s  > %(message)s",
                "datefmt": "%d %b %y %H:%M:%S"
            }
        }
    }
