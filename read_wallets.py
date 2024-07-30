import json
from web3 import Web3
from eth_account import Account

import time_wait


# Загрузка данных из JSON файла
with open('wallets.json', 'r') as file:
    data = json.load(file)

networks = data['networks']  # Словарь с URL сетей
accounts = data['accounts']  # Список учетных записей

# Включение неаудированных функций HD Wallet
Account.enable_unaudited_hdwallet_features()


# Создание приватного ключа из мнемонической фразы
def create_private_key(mnemonic):
    account = Account.from_mnemonic(mnemonic)
    return account.key.hex()


# Функция для отправки транзакций
def send_transaction(
        network_url,
        network_id,
        from_address,
        private_key,
        to_address,
        gas_limit,
        reserve=10000000000):
    web3 = Web3(Web3.HTTPProvider(network_url))
    balance = web3.eth.get_balance(from_address)
    gas_price = web3.eth.gas_price

    # Формирование транзакции
    tx = {
        'nonce': web3.eth.get_transaction_count(from_address),
        'to': to_address,
        'value': 0,  # Начальное значение для оценки газа
        'gasPrice': gas_price,
        'chainId': network_id,
        'gas': gas_limit
    }

    # Расчет стоимости транзакции (tx cost)
    tx_cost = gas_price * gas_limit

    # Проверка на достаточность средств для покрытия стоимости газа
    if balance <= tx_cost:
        return f"Недостаточно газа для транзакции: balance {balance}, tx cost {tx_cost}"

    # Расчет максимально возможного значения транзакции с дополнительным запасом
    max_value = balance - tx_cost - reserve  # Уменьшаем на резерв для обеспечения достаточного запаса

    # Обновление значения транзакции
    tx['value'] = max_value

    # Подписание и отправка транзакции
    attempt_chain = 0
    while attempt_chain < 5:
        try:
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return tx_hash.hex()
        except Exception as e:
            tx['value'] -= 1000000000000
            attempt_chain += 1
            print(f"Ошибка при отправке транзакции: {e}")


with open('wallets_to.json', 'r') as w_to:
    dict_address_to = json.load(w_to)


for acc_key, acc_value in accounts.items():
    print(f"Аккаунт {acc_key}")

    for network_name, network_data in networks.items():
            reserve = 10000000000  # По умолчанию увеличенный резерв
            gas_limit = 30000
            if network_name in ["Base", "Optimism", "Binance Smart Chain"]:
                reserve = 20000000000  # Увеличиваем резерв еще больше для проблемных сетей

            if network_name in "Arbitrum":
                gas_limit = 100000

            attempt = 1
            max_attempts = 5  # Максимальное количество попыток

            while attempt <= max_attempts:
                try:
                    result = send_transaction(
                        network_data["url"],
                        network_data["chainId"],
                        Web3.to_checksum_address(acc_value['address']),
                        create_private_key(acc_value['private_key']),
                        Web3.to_checksum_address(dict_address_to[acc_key]),
                        gas_limit=gas_limit,  # Используем увеличенный лимит газа
                        reserve=reserve
                    )
                    print(f"Транзакция в сети {network_name}: {result}")
                    break  # Если транзакция успешна, выходим из цикла
                except Exception as e:
                    print(f"Ошибка при работе с сетью {network_name} (попытка {attempt}): {e}")
                    reserve += 50000000000  # Увеличиваем резерв на 5,000,000,000 wei
                    gas_limit += 20000
                    attempt += 1

            if attempt > max_attempts:
                print(f"Не удалось выполнить транзакцию в сети {network_name} после {max_attempts} попыток")

            print('Ожидание между сетями внутри акка')
            time_wait.random_wait(1, 5)
    print('Ожидание между акками')
    time_wait.random_wait(10, 30)
    print('-------------------------------------------')
