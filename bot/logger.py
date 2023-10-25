import logging as logg


def setup_logger():
    log = logg.getLogger(__name__)
    log.setLevel(logg.DEBUG)

    # Создание обработчика для уровня INFO
    info_handler = logg.FileHandler('_logs/info.log')
    info_handler.setLevel(logg.INFO)

    # Создание обработчика для ошибок с уровнями выше WARNING
    error_handler = logg.FileHandler('_logs/errors.log')
    error_handler.setLevel(logg.ERROR)

    # Создание форматтера для логов
    formatter = logg.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Привязка обработчика и форматтера к логгеру
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    log.addHandler(info_handler)
    log.addHandler(error_handler)

    return log


logging = setup_logger()
