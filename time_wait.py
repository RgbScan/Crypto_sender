import time
import random


def random_wait(start, end):
    wait_time = random.randint(start, end)
    print(f'Ждем {wait_time} секунд для антисибильства')
    time.sleep(wait_time)

