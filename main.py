from typing import override

import yaml
from app.models import Variant, Deal
from app.components import ComponentRegistryEXW, create_component, ComponentRegistryDDP
from app.services import DealCalculator


def run_calculations_from_file(filepath: str):
    """Загружает сделки из YAML-файла и рассчитывает их"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f'Error: file not found in {filepath}')
        return

    # Выполняются расчеты (используем калькулятор)
    calculator = DealCalculator()

    for i, deal_data in enumerate(data, 1):
        print(f"--- Расчет для сделки #{i}: {deal_data['name']} ---")

        # Собираются компоненты из файла
        components = []
        for comp_data in deal_data['components']:
            registry_key = ComponentRegistryEXW[comp_data['key']]
            override_value = comp_data.get('base_value_override')
            components.append(create_component(registry_key, base_value_override=override_value))

        # Собираются варианты
        variants = [Variant(**v) for v in deal_data['variants']]

        # Создается сделка
        deal = Deal(
            is_small=deal_data['is_small'],
            variants=variants,
            components=components
        )

        merchant_payment_small = calculator.calculate_payment(deal, 'MERCHANT')
        jpc_payment_small = calculator.calculate_payment(deal, 'JPC')
        client_payment_small = calculator.calculate_payment(deal, 'ClientEXW')

        for k, v in calculator.get_component_costs_per_component(deal).items():
            print(f'{k}: {v}')

        print()
        print(f"Платеж мерчанту: {merchant_payment_small}\n"
              f"Платеж в JPC: {jpc_payment_small}\n"
              f"EXW price for client: {client_payment_small}"
              )

if __name__ == "__main__":
    run_calculations_from_file('deals.yaml')