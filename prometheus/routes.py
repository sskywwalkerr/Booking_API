import time
from random import random

from fastapi_versioning import version
from fastapi import APIRouter

router_prom = APIRouter()


@router_prom.get('get_error')
@version(1)
def get_error():
    """Функция для теста Prometheus + Grafana"""
    if random() > 0.5:
        raise ZeroDivisionError
    else:
        raise KeyError


@router_prom.get('/time_consumer')
@version(1)
def time_consumer():
    """Функция для теста Prometheus + Grafana"""
    time.sleep(random() * 5)
    return 'Тест завершен'


@router_prom.get('/memory_consumer')
@version(1)
def memory_consumer():
    """Функция для теста Prometheus + Grafana"""
    _ = [i for i in range(30_000_000)]
    return 'Тест завершен'
