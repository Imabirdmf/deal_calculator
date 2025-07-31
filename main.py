from app.models import Variant, Deal
from app.components import ComponentRegistryEXW, create_component
from app.services import DealCalculator

if __name__ == "__main__":

    # --- Создается список вариантов для новой сделки ---

    variants_qty = int(input('Количество вариантов: '))
    deal_variants = [Variant(variant_name=input('Название варианта: '), variant_qty=int(input('Количество варианта: '))) for _ in range(variants_qty)]

    # --- Формируется список компонентов из реестра ---
    components_for_deal = [
        create_component(ComponentRegistryEXW.MERCHANTFEEEXW, 3542.00),
        create_component(ComponentRegistryEXW.FIRSTMILEEXW, 315.67),
        create_component(ComponentRegistryEXW.VATEXW, 177.10),
        create_component(ComponentRegistryEXW.WAREHOUSEOPS, 425.04),
        create_component(ComponentRegistryEXW.JPCCOMISSION, 214.14),
        create_component(ComponentRegistryEXW.SUBSIDYEXW),
        create_component(ComponentRegistryEXW.FINESEXW)
    ]

    # --- Создается сделка с этим списком вариантов и компонентами ---
    small_deal = Deal(
        is_small=True,
        variants=deal_variants,
        components=components_for_deal
    )

    # --- Выполняются расчеты (используем калькулятор) ---
    calculator = DealCalculator()
    merchant_payment_small = calculator.calculate_payment(small_deal, 'MERCHANT')
    jpc_payment_small = calculator.calculate_payment(small_deal, 'JPC')
    client_payment_small = calculator.calculate_payment(small_deal, 'ClientEXW')

    for k, v in calculator.get_component_costs_per_component(small_deal).items():
        print(f'{k}: {v}')

    print()
    print(f"Платеж мерчанту: {merchant_payment_small}\n"
          f"Платеж в JPC: {jpc_payment_small}\n"
          f"EXW price for client: {client_payment_small}"
          )