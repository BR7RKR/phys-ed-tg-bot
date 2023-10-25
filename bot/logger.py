import logging as logg


def setup_logger():
    log = logg.getLogger(__name__)
    log.setLevel(logg.DEBUG)

    info_handler = logg.FileHandler('_logs/info.log')  # при сборке образа добавить в начало bot/
    info_handler.setLevel(logg.INFO)

    error_handler = logg.FileHandler('_logs/errors.log')  # при сборке образа добавить в начало bot/
    error_handler.setLevel(logg.ERROR)

    formatter = logg.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    log.addHandler(info_handler)
    log.addHandler(error_handler)

    return log


logging = setup_logger()
