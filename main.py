from database import create_tables
from product import add_product, view_products, low_stock_alert, export_inventory_report
from inventory import update_stock, view_transactions
from supplier import add_supplier, view_suppliers
from auth import register_admin, login

def show_menu():
    print("\n========= MINI ERP MENU =========")
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Stock (IN/OUT)")
    print("4. View Transaction History")
    print("5. Low Stock Alert")
    print("6. Export Inventory Report")
    print("7. Add Supplier")
    print("8. View Suppliers")
    print("9. Exit")
    print("=================================")

def main():
    create_tables()
    register_admin()

    if not login():
        return

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            low_stock_alert()
        elif choice == "6":
            export_inventory_report()
        elif choice == "7":
            add_supplier()
        elif choice == "8":
            view_suppliers()
        elif choice == "9":
            print("Exiting ERP System...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()