from src.manager import Manager
from src.models import Parameters


def test_get_apartment_costs():
    manager = Manager(Parameters())

    # apartment does not exist
    assert manager.get_apartment_costs('apart-nonexistent', 2025, 1) is None

    # apartment has bills in this month (760 + 150)
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0

    # same year, different month -> no bills
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0

    # same month, different year -> no bills
    assert manager.get_apartment_costs('apart-polanka', 2024, 1) == 0.0