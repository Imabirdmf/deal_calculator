from enum import Enum


from app.models import SplitByQuantity, SimpleComponent, Component


class ComponentRegistryEXW(Enum):
    """
        Реестр всех доступных EXW компонентов калькулятора
    """
    FIRSTMILEEXW = SplitByQuantity(
        name = "First Mile",
        scheme = 'EXW',
        base_value = 0.0,
        metadata={
            'payment_types': {
                'MERCHANT': 'all',  # Используется в платеже 'MERCHANT' для всех сделок
                'JPC': 'small',
                'ClientEXW' : 'small'
            }
        }
    )

    VATEXW = SplitByQuantity(
        name = 'VAT',
        scheme = 'EXW',
        base_value = 0.0,
        metadata={
            'payment_types': {
                'MERCHANT': 'all',  # Используется в платеже 'MERCHANT' для всех сделок
                'JPC': 'all',
                'ClientEXW': 'small'
            }
        }
    )

    MERCHANTFEEEXW = SplitByQuantity(
        name = 'Merchant Fee',
        scheme = 'EXW',
        base_value = 0.0,
        metadata={
            'payment_types': {
                'MERCHANT': 'all',  # Используется в платеже 'MERCHANT' для всех сделок
                'JPC': 'all',
                'ClientEXW': 'all'
            }
        }
    )

    SUBSIDYEXW = SplitByQuantity(
        name = 'Subsidy',
        scheme = 'EXW',
        base_value = 0.0,
        metadata={
            'payment_types': {
                'MERCHANT': 'all'  # Используется в платеже 'MERCHANT' для всех сделок
            }
        }
    )

    FINESEXW = SimpleComponent(
        name = 'Additional expenses and fines',
        scheme = 'EXW',
        base_value = 0.0,
        metadata={
            'payment_types': {
                'MERCHANT': 'all',  # Используется в платеже 'MERCHANT' для всех сделок
                'JPC': 'all',
                'ClientEXW': 'all'
            }
        }
    )

    BANKFEEEXW = SplitByQuantity(
        name = 'Bank fee EXW',
        scheme = 'EXW',
        base_value = 0.0
    )

    WAREHOUSEOPS = SplitByQuantity(
        name = 'WarehousingOp',
        scheme='EXW',
        base_value=0.0
    )

    JPCCOMISSION = SplitByQuantity(
        name = 'JPC commission',
        scheme='EXW',
        base_value=0.0,
        metadata={
            'payment_types': {
                'JPC': 'all',
                'ClientEXW': 'all'
            }
        }
    )


def create_component(
        registry_key: ComponentRegistryEXW,
        base_value_override: float | None = None
) -> Component:
    """
    Создает экземпляр компонента из реестра с возможностью переопределить base_value
    """
    template_component = registry_key.value

    new_component_instance = template_component.clone()

    if base_value_override is not None:
        new_component_instance.base_value = base_value_override

    return new_component_instance
