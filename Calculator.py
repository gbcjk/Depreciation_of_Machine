#Depreciation 

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_date_input(prompt):
    while True:
        date_str = input(prompt + " (DD-MM-YYYY): ")
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def calculate_depreciation(machines, end_date, method, rate):
    print("\nDepreciation Calculation:")
    print(f"Method: {'Straight-line' if method == 's' else 'Diminishing balance'}")
    print(f"Rate: {rate*100:.2f}%\n")
    
    for i, machine in enumerate(machines, 1):
        print(f"\nMachine {i} purchased on {machine['purchase_date'].strftime('%d-%b-%Y')}:")
        purchase_date = machine['purchase_date']
        cost = machine['cost']
        book_value = cost
        accum_dep = 0
        sold = False
        
        if 'sale_date' in machine and machine['sale_date'] <= end_date:
            sale_date = machine['sale_date']
            sale_price = machine['sale_price']
            sold = True
        
        current_date = purchase_date
        year_counter = 0
        
        print("{:<12} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
            "Year End", "Original Cost", "Depreciation", "Accumulated Dep", 
            "Book Value", "Remarks"))
        
        while current_date <= end_date and (not sold or current_date <= sale_date):
            year_end = datetime(current_date.year, 3, 31)
            if current_date.year == purchase_date.year and current_date.month > 3:
                year_end = datetime(current_date.year + 1, 3, 31)
            
            # Calculate fraction of year for first and last year
            if current_date == purchase_date:
                days = (year_end - current_date).days
                fraction = days / 365
            elif year_end > min(end_date, sale_date if sold else end_date):
                days = (min(end_date, sale_date if sold else end_date) - datetime(year_end.year - 1, 4, 1)).days
                fraction = days / 365
            else:
                fraction = 1
            
            # Calculate depreciation
            if method == 's':  # Straight-line
                dep = cost * rate * fraction
            else:  # Diminishing balance
                dep = book_value * rate * fraction
            
            # For the year of sale, depreciation is up to sale date
            if sold and year_end > sale_date:
                days = (sale_date - datetime(sale_date.year - 1, 4, 1)).days if sale_date.month >= 4 else (sale_date - datetime(sale_date.year - 1, 1, 1)).days
                fraction = days / 365
                if method == 's':
                    dep = cost * rate * fraction
                else:
                    dep = book_value * rate * fraction
            
            accum_dep += dep
            book_value -= dep
            book_value = max(0, book_value)  # Book value shouldn't go negative
            
            remarks = ""
            if sold and current_date <= sale_date < datetime(year_end.year + 1, 4, 1):
                profit_loss = sale_price - book_value
                remarks = f"Sold for {sale_price:.2f} ({'Profit' if profit_loss >=0 else 'Loss'}: {abs(profit_loss):.2f})"
                sold = False  # To stop further calculations
            
            print("{:<12} {:<15.2f} {:<15.2f} {:<15.2f} {:<15.2f} {:<15}".format(
                year_end.strftime("%d-%b-%Y"),
                cost,
                dep,
                accum_dep,
                book_value,
                remarks
            ))
            
            current_date = datetime(year_end.year + 1, 4, 1)
            year_counter += 1
            
            # For diminishing balance, stop when book value becomes negligible
            if method == 'd' and book_value < cost * 0.01:
                break

def main():
    print("Depreciation Calculator with Sales")
    print("=================================\n")
    
    # Get common inputs
    end_date = get_date_input("Enter the accounting year end date")
    rate = get_float_input("Enter depreciation rate (as percentage, e.g., 15 for 15%): ") / 100
    
    while True:
        method = input("Choose depreciation method (s for straight-line, d for diminishing balance): ").lower()
        if method in ['s', 'd']:
            break
        print("Invalid choice. Please enter 's' or 'd'.")
    
    # Get machine details
    machines = []
    while True:
        print("\nEnter details for machine", len(machines) + 1)
        purchase_date = get_date_input("Enter purchase date")
        cost = get_float_input("Enter machine cost: ")
        installation = get_float_input("Enter installation cost (0 if none): ")
        
        machine = {
            'purchase_date': purchase_date,
            'cost': cost + installation
        }
        
        sell = input("Was this machine sold? (y/n): ").lower()
        if sell == 'y':
            sale_date = get_date_input("Enter sale date")
            sale_price = get_float_input("Enter sale price: ")
            machine['sale_date'] = sale_date
            machine['sale_price'] = sale_price
        
        machines.append(machine)
        
        more = input("Add another machine? (y/n): ").lower()
        if more != 'y':
            break
    
    # Calculate and display depreciation
    calculate_depreciation(machines, end_date, method, rate)

if __name__ == "__main__":
    main()
