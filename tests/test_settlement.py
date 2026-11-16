from src.manager import Manager
from src.models import ApartmentSettlement, Parameters


def test_create_apartment_settlement():
    manager = Manager(Parameters())

    # apartment with bills in this month (760 + 150)
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 1
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_due_pln == -910.0

    # apartment without bills in this month
    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 2)
    assert isinstance(settlement, ApartmentSettlement)
    assert settlement.month == 2
    assert settlement.total_bills_pln == 0.0
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_due_pln == 0.0

    # apartment does not exist
    assert manager.create_apartment_settlement('apart-nonexistent', 2025, 1) is None