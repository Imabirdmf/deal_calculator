import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import decimal
from functools import reduce


@dataclass
class Variant:
    variant_name: str
    variant_qty: int
    # variant_price: float
    # variant_weight: float
    # variant_volume: float


class Component(ABC):

    def __init__(self,
                 name: str,
                 scheme: str,
                 base_value: float = 0.0,
                 metadata: dict | None = None
                 ):
        self.name = name
        self.scheme = scheme
        self.base_value = base_value
        self.metadata = metadata or {}

    @abstractmethod
    def get_component_ppi(self, deal: 'Deal', variant: 'Variant') -> float:
        pass

    def clone(self) -> 'Component':
        """
        Создает и возвращает полную независимую копию этого компонента.
        """
        return copy.deepcopy(self)


class SimpleComponent(Component):
    def get_component_ppi(self, deal: 'Deal', variant: 'Variant') -> float:
        return self.base_value / deal.deal_qty * variant.variant_qty


class SplitByQuantity(Component):
    """
        Компонент, стоимость которого делится на количество товаров и их вариантов,
        а затем округляется
    """

    # @staticmethod
    # Округление, как roundup в Экселе
    # def roundup(x, digits=0):
    #     q = decimal.Decimal('1e-' + str(digits))  # шаг округления
    #     d = decimal.Decimal(str(x))
    #     if x >= 0:
    #         return float(d.quantize(q, rounding=decimal.ROUND_CEILING))
    #     else:
    #         return float(d.quantize(q, rounding=decimal.ROUND_FLOOR))

    def get_component_ppi(self, deal: 'Deal', variant: 'Variant'):
        if not variant.variant_qty:
            return 0.0
        # Расчет стоимости с делением и округлением повариантно
        variant_cost = ((self.base_value * (variant.variant_qty / deal.deal_qty)) / variant.variant_qty) * variant.variant_qty
        # print(self.base_value, 'variant.variant_qty / deal.deal_qty = ', variant.variant_qty / deal.deal_qty)
        # print(f'variant_cost {variant.variant_name} =', variant_cost)
        variant_rounded_cost = round(variant_cost, 2)
        # print(variant_rounded_cost)
        return variant_rounded_cost  # Стоимость компонента за вариант, округленная вверх до 2х знаков


class SplitByVolume(Component):
    pass

class SplitByWeight(Component):
    pass


class Deal:
    def __init__(self, variants: list, components: list, is_small: bool = True, ):
        self.is_small = is_small
        self.variants = variants
        self.components = components
        self.deal_qty = sum(v.variant_qty for v in self.variants)
        # self.merchant_fee = sum(v.variant_qty * v.variant_price for v in self.variants)


