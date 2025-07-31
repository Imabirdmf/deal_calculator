from app.models import Variant, Deal, ComponentRegistryEXW, create_component
from app.services import DealCalculator

def test_one_variant():
    deal_variants = [Variant('test_variant1', 1)]
    components_for_deal = [
        create_component(ComponentRegistryEXW.MERCHANTFEEEXW, 3542.00),
        create_component(ComponentRegistryEXW.FIRSTMILEEXW, 315.67),
        create_component(ComponentRegistryEXW.VATEXW, 177.10),
        create_component(ComponentRegistryEXW.WAREHOUSEOPS, 425.04),
        create_component(ComponentRegistryEXW.JPCCOMISSION, 214.14),
        create_component(ComponentRegistryEXW.SUBSIDYEXW),
        create_component(ComponentRegistryEXW.FINESEXW)
    ]
    small_deal = Deal(
        is_small=True,
        variants=deal_variants,
        components=components_for_deal
    )
    calculator = DealCalculator()
    merchant_payment_small = calculator.calculate_payment(small_deal, 'MERCHANT')
    jpc_payment_small = calculator.calculate_payment(small_deal, 'JPC')
    client_payment_small = calculator.calculate_payment(small_deal, 'ClientEXW')

    assert merchant_payment_small == 4034.77
    assert jpc_payment_small == 4248.91
    assert client_payment_small == 4248.91
