from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, TenantSettlement, Transfer

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    def get_apartment_costs(self, apartment_key: str, year: int | None = None,
                            month: int | None = None) -> float | None:
        if apartment_key not in self.apartments:
            return None
        if month is not None and not 1 <= month <= 12:
            raise ValueError(f"Invalid month: {month}")

        total = 0.0
        for bill in self.bills:
            if bill.apartment != apartment_key:
                continue
            if year is not None and bill.settlement_year != year:
                continue
            if month is not None and bill.settlement_month != month:
                continue
            total += bill.amount_pln
        return total

    def create_apartment_settlement(self, apartment_key: str, year: int,
                                    month: int) -> ApartmentSettlement | None:
        total_bills = self.get_apartment_costs(apartment_key, year, month)
        if total_bills is None:
            return None

        total_rent = 0.0  # transfers will be included in a later step

        return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_rent_pln=total_rent,
            total_bills_pln=total_bills,
            total_due_pln=total_rent - total_bills,
        )
    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement) -> list[TenantSettlement]:
        tenant_keys = [key for key, tenant in self.tenants.items()
                       if tenant.apartment == apartment_settlement.apartment]
        count = len(tenant_keys)

        settlements = []
        for key in tenant_keys:
            settlements.append(TenantSettlement(
                tenant=key,
                apartment_settlement=apartment_settlement.apartment,
                year=apartment_settlement.year,
                month=apartment_settlement.month,
                rent_pln=apartment_settlement.total_rent_pln / count,
                bills_pln=apartment_settlement.total_bills_pln / count,
                total_due_pln=apartment_settlement.total_due_pln / count,
                balance_pln=apartment_settlement.total_due_pln / count,  # transfers later
            ))
        return settlements