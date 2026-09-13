from __future__ import annotations

from collections import defaultdict

RARITY_ORDER = [
    "Mil-Spec",
    "Restricted",
    "Classified",
    "Covert",
    "Contraband",
    "Extraordinary",
    "Legendary",
    "Mythic",
]

# The rarest tier in a case is intentionally very hard to hit.
# 100€ case -> ~0.15%; 5,000€+ case -> ~0.50%.
# More expensive cases increase the chance of the rarest tier without making
# jackpots common enough to destroy the economy.

def _price_factor(case_price: float) -> float:
    low, high = 100.0, 5000.0
    return max(0.0, min(1.0, (float(case_price or 0) - low) / (high - low)))


def _rarity_rank(value: str) -> int:
    try:
        return RARITY_ORDER.index(str(value or "").strip())
    except ValueError:
        return 0


def rarity_distribution(present_rarities: list[str], case_price: float) -> dict[str, float]:
    present = []
    seen = set()
    for rarity in present_rarities:
        if rarity in seen:
            continue
        seen.add(rarity)
        present.append(rarity)
    if not present:
        return {}

    present.sort(key=_rarity_rank)
    top = present[-1]
    factor = _price_factor(case_price)
    top_probability = 0.15 + 0.35 * factor

    if len(present) == 1:
        return {top: 100.0}

    # Relative mass for everything below the rarest tier. Higher priced cases
    # move some mass upward, while keeping the top tier capped around 0.5%.
    weights: dict[str, float] = {top: 0.0}
    top_rank = _rarity_rank(top)
    for rarity in present[:-1]:
        distance = top_rank - _rarity_rank(rarity)
        if distance <= 1:
            weight = 2.0 + 1.5 * factor
        elif distance == 2:
            weight = 5.0 + 3.0 * factor
        elif distance == 3:
            weight = 12.0 + 5.0 * factor
        elif distance == 4:
            weight = 24.0 + 8.0 * factor
        else:
            weight = 60.0 + 12.0 * factor
        weights[rarity] = weight

    remainder = 100.0 - top_probability
    total_lower = sum(weights.values()) or 1.0
    distribution = {top: top_probability}
    for rarity in present[:-1]:
        distribution[rarity] = remainder * (weights[rarity] / total_lower)
    return distribution


def weighted_relations(relations, case_price: float):
    valid = [
        relation for relation in relations
        if relation.item and relation.item.is_active and float(relation.probability or 0) > 0
    ]
    if not valid:
        return []

    rarity_targets = rarity_distribution(
        [str(relation.item.rarity or "") for relation in valid],
        case_price,
    )
    grouped = defaultdict(list)
    for relation in valid:
        grouped[str(relation.item.rarity or "")].append(relation)

    result = []
    for rarity, members in grouped.items():
        target = float(rarity_targets.get(rarity, 0.0))
        base_total = sum(float(item.probability or 0) for item in members) or 1.0
        weighted_members = []
        for relation in members:
            item_value = float(getattr(relation.item, "virtual_value", 0) or 0)
            price = max(float(case_price or 0), 1.0)
            ratio = item_value / price
            # Price-fit curve: expensive cases should lean toward expensive drops,
            # while still keeping every configured item possible.
            value_factor = max(0.22, min(2.65, ratio ** 0.58 if ratio > 0 else 0.22))
            weighted_members.append((relation, float(relation.probability or 0) * value_factor))
        weighted_total = sum(weight for _, weight in weighted_members) or 1.0
        for relation, member_weight in weighted_members:
            within_rarity = member_weight / weighted_total
            result.append((relation, target * within_rarity))
    return result


def choose_case_item(case_items, case_price: float):
    import random
    weighted = weighted_relations(case_items, case_price)
    if not weighted:
        return None
    return random.choices(
        [relation for relation, _ in weighted],
        weights=[weight for _, weight in weighted],
        k=1,
    )[0]
