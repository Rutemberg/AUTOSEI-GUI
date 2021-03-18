import logging
from datetime import datetime
from locale import LC_ALL, setlocale
setlocale(LC_ALL, 'pt_BR.utf-8')


def log(nome_do_arquivo, mensagem, tipo, titulo=False, console=True, modo="a"):
    logger = logging.getLogger(f"{mensagem}")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    if console == False:
        logger.removeHandler(ch)

    fl = logging.FileHandler(
        filename=f"{nome_do_arquivo}.log", encoding='utf-8', mode=modo)
    fl.setLevel(logging.DEBUG)

    if titulo == True:
        formatter = logging.Formatter(fmt='%(name)s\n')
    else:
        data = datetime.now()
        hora = data.strftime('%H')
        minuto = data.strftime('%M')
        segundo = data.strftime('%S')
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt=f'%d/%m/%Y {hora}:{minuto}:{segundo}')

    if console == True:
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    fl.setFormatter(formatter)
    logger.addHandler(fl)

    if tipo == "info":
        logger.info(f"{mensagem}")
    elif tipo == "warn":
        logger.warning(f"{mensagem}")

    logger.removeHandler(fl)
    logger.removeHandler(ch)


