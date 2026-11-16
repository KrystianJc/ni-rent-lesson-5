from src.manager import Manager
from src.models import ApartmentSettlement, Parameters, TenantSettlement

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

def test_create_tenant_settlements():
    manager = Manager(Parameters())
    # bills for apart-polanka in 01/2025: 760 + 150 = 910
    apartment_settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)

    # 2 tenants -> costs split in half
    del manager.tenants['tenant-3']
    settlements = manager.create_tenant_settlements(apartment_settlement)
    assert len(settlements) == 2
    assert [s.tenant for s in settlements] == ['tenant-1', 'tenant-2']
    for s in settlements:
        assert isinstance(s, TenantSettlement)
        assert s.apartment_settlement == 'apart-polanka'
        assert s.year == 2025
        assert s.month == 1
        assert s.bills_pln == 455.0
        assert s.total_due_pln == -455.0

    # 1 tenant -> pays everything
    del manager.tenants['tenant-2']
    settlements = manager.create_tenant_settlements(apartment_settlement)
    assert len(settlements) == 1
    assert settlements[0].tenant == 'tenant-1'
    assert settlements[0].bills_pln == 910.0
    assert settlements[0].total_due_pln == -910.0

    # no tenants -> no settlements
    del manager.tenants['tenant-1']
    settlements = manager.create_tenant_settlements(apartment_settlement)
    assert settlements == []