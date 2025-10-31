from typing import override


class Employee:
    def __init__(self, employee_id, first_name: str, last_name: str, store_id: int, salary: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        # Зарплата тепер приватна
        self.__salary = salary
        self.store_id = store_id
        self.employee_id = employee_id

    def __repr__(self):
        return f'Employee(id={self.employee_id}, name={self.first_name}, salary={self.salary})'

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return (self.employee_id == other.employee_id and
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.salary == other.salary)

    @property
    def salary(self):
        # Геттер читає з приватного __salary
        return self.__salary

    @salary.setter
    def salary(self, salary):
        if salary < 0:
            raise ValueError('Salary cannot be negative')
        # Сеттер пише в приватне __salary
        self.__salary = salary

    @staticmethod
    def validate_name(name):
        cleaned_name = name.strip()
        if len(cleaned_name) < 2:
            return False
        if any(char.isdigit() for char in cleaned_name):
            return False
        return True


class HallWorker(Employee):
    def __init__(self, employee_id, first_name, last_name, store_id, salary, department: str):
        super().__init__(employee_id, first_name, last_name, store_id, salary)
        self.department = department

    @override
    def __repr__(self):
        return f'HallWorker(name={self.first_name}, salary={self.salary}, dep={self.department})'

    def restock_shelves(self, product, quantity):
        print(f"[{self.first_name}]: викладаю {quantity} од. товару '{product}'")


class Cashier(Employee):
    def __init__(self, employee_id, first_name, last_name, store_id, salary, cash_register_id: int):
        super().__init__(employee_id, first_name, last_name, store_id, salary)
        self.cash_register_id = cash_register_id

    @override
    def __repr__(self):
        return f'Cashier(name={self.first_name}, salary={self.salary}, kasa={self.cash_register_id})'

    @override
    def __eq__(self, other):
        if not isinstance(other, Cashier):
            return False
        return super().__eq__(other) and self.cash_register_id == other.cash_register_id

    def process_sale(self, sale_total):
        print(f"[{self.first_name}]: чек на суму {sale_total} грн оброблено.")


class VersatileWorker(Cashier, HallWorker):
    def __init__(self, employee_id, first_name, last_name, store_id, salary, cash_register_id, department: str):
        Employee.__init__(self, employee_id, first_name, last_name, store_id, salary)
        self.cash_register_id = cash_register_id
        self.department = department

    @override
    def __repr__(self):
        return (f"VersatileWorker(name={self.first_name}, salary={self.salary}, "
                f"kasa={self.cash_register_id}, dep={self.department})")

    @override
    def __eq__(self, other):
        if not isinstance(other, VersatileWorker):
            return False
        return super().__eq__(other) and self.department == other.department


class Administrator(VersatileWorker):
    def __init__(self, employee_id, first_name, last_name, store_id, salary, contract_id: int):
        VersatileWorker.__init__(self, employee_id, first_name, last_name, store_id, salary,
                                 cash_register_id=None,
                                 department="Administration")
        self.contract_id = contract_id

    @override
    def __repr__(self):
        return f"Administrator(name={self.first_name}, salary={self.salary}, contract={self.contract_id})"

    @override
    def __eq__(self, other):
        if not isinstance(other, Administrator):
            return False
        return super().__eq__(other) and self.contract_id == other.contract_id

    def set_cash_register(self, cash_register_id):
        self.cash_register_id = cash_register_id
        print(f"[{self.first_name}]: змінив свою касу на {self.cash_register_id}")

    def hire_employee(self, new_name: str):
        if Employee.validate_name(new_name):
            print(f"[{self.first_name}]: наймаю нового працівника '{new_name}'")
            return True
        else:
            print(f"[{self.first_name}]: ім'я '{new_name}' неваліднe!")
            return False



if __name__ == "__main__":

    print("--- 1. Демонстрація Інкапсуляції (Salary Property) ---")
    try:
        emp1 = Employee(101, "Іван", "Петренко", 1, 30000)
        print(f"Початкова зарплата: {emp1.salary}")
        emp1.salary = 35000
        print(f"Нова зарплата: {emp1.salary}")
        print("Спроба встановити негативну зарплату:")
        emp1.salary = -500
    except ValueError as e:
        print(f"  СПІЙМАЛИ ПОМИЛКУ: {e}")

    print("\n--- 2. Демонстрація Статичного методу ---")
    print(f"Чи 'Василь' валідне ім'я? {Employee.validate_name('Василь')}")
    print(f"Чи 'R2D2' валідне ім'я? {Employee.validate_name('R2D2')}")

    print("\n--- 3. Демонстрація Спадковості та унікальних методів ---")
    cashier1 = Cashier(102, "Олена", "Сидоренко", 1, 28000, 5)
    hall_worker1 = HallWorker(103, "Василь", "Іванов", 1, 27000, "Напої")
    admin1 = Administrator(901, "Ірина", "Войтенко", 1, 50000, 12345)

    cashier1.process_sale(150.75)
    hall_worker1.restock_shelves("Молоко", 30)
    admin1.hire_employee("Новий Працівник")

    print("\n[Адмін (успадкував від VersatileWorker -> Cashier) викликає process_sale]:")
    admin1.set_cash_register(3)
    admin1.process_sale(99.99)

    print("\n--- 4. Демонстрація Поліморфізму (через __repr__) ---")
    staff_list = [emp1, cashier1, hall_worker1, admin1]

    print("Друк списку staff_list (Python автоматично викликає __repr__):")
    for staff in staff_list:
        print(f"  - {staff}")