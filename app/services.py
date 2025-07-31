from app.models import Deal, Variant


class DealCalculator:
    def get_component_costs_per_component(self, deal: Deal) -> dict:
        # пока без компонентов в процентах
        costs_per_component = {}
        for component in deal.components:
            # print(component.name)
            for variant in deal.variants:
                component_ppi_per_variant = component.get_component_ppi(deal, variant)
                costs_per_component[component.name] = costs_per_component.get(component.name, [])
                costs_per_component[component.name].append(component_ppi_per_variant)
        return costs_per_component

    def calculate_payment(self, deal: Deal, payment_type: str) -> float:
        """
        Рассчитывает итоговую сумму для конкретного типа платежа.
        """
        all_component_costs = self.get_component_costs_per_component(deal)
        total_payment = 0.0

        for component in deal.components:
            # Проверяем, относится ли компонент к нужному типу платежа
            rule = component.metadata.get('payment_types', {}).get(payment_type)
            if not rule:
                continue  # Пропускаем, если компонент не участвует в этом типе платежа

            # Проверяем соответствие размера сделки правилу компонента
            is_large_deal = not deal.is_small
            should_add = (
                    rule == 'all' or
                    (rule == 'small' and deal.is_small) or
                    (rule == 'large' and is_large_deal)
            )

            if should_add:
                total_payment += sum(all_component_costs.get(component.name, 0.0))

        return round(total_payment, 2)