'''
This program defines a class called 'Shoe' which stores information about different shoe products in a warehouse. The program is intended to be 
used by store managers to perform tasks including: searching for products by code, identifying the lowest quantity products to re-stock, 
identifying the highest quantity products and calculating the total value of each stock item (see the descriptions of each function defined
below). 
'''

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity


    # This method returns the cost of the shoe as a float. 
    def get_cost(self):
        float_cost = float(self.cost)
        return(float_cost)
        

    # This method returns the quantity of a shoe as an integer.
    def get_quantity(self):
        int_quantity = int(self.quantity)
        return(int_quantity)


    # This method returns a string representation of the shoe class.
    def __str__(self):

        return(f'''
Country:   {self.country}
Code:      {self.code}
Product:   {self.product}
Cost:      {self.cost}R
Quantity:  {self.quantity}
    ''')

#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


#==========Functions outside the class==============


# This function reads the data from the file inventory.txt and creates shoe objects with this data. The shoe objects are stored in shoe_list.
def read_shoes_data():

    # Open the file inventory.txt and skip the first line of the file as this contains the headings rather than information about a shoe.
    try:
        inventory_file = open('inventory.txt', 'r', encoding='utf-8')     

        line_count = 1

        for line in inventory_file:        

            if line_count > 1:

                line_split = line.strip("\n").split(',')

                # After the first line of the file, create a shoe object and add it to the shoes list.  
                shoe_list.append(Shoe(line_split[0], line_split[1], line_split[2], line_split[3], line_split[4]))

            line_count += 1

        inventory_file.close()

    except FileNotFoundError:
        print("Error: shoes data has not been read as the inventory file cannot be found.")


# This function uses the list of shoes to update the file 'inventory.txt' with any additions or changes. 
def update_inventory():
    
    # Write the headings to the first line of the file. 
    inventory_file = open('inventory.txt', 'w', encoding='utf-8')
    inventory_file.write(f'''Country,Code,Product,Cost,Quantity''')
    inventory_file.close()
    
    # Use a for loop to append the inventory.txt file with each of the shoes in shoe_list.
    inventory_file = open('inventory.txt', 'a', encoding='utf-8')
    
    for shoe in shoe_list:
        inventory_file.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")

    inventory_file.close()


# This function allows the user to capture data about a shoe. 
# The data is used to create a shoe object which is added to shoe_list and updated in the file 'inventory.txt'. 
def capture_shoes():    
    
    capture_country = input("\nPlease enter the country where the shoe is produced: ")

    # Use a while loop to request the shoe code from the user and validate that the input matches the shoe code format e.g. SKU12345
    while True:

        capture_code = input("Please enter the shoe code: ")

        if capture_code.strip()[0:3] == 'SKU' and len(capture_code.strip()) == 8:
            break

        else:
            print("\nInput error: all shoe codes begin with SKU and are 8 characters long. Please try again.")


    capture_product = input("Please enter the product name: ")


    # Use a while loop to request the shoe cost from the user and validate the input.
    while True:

        try:
            capture_cost = float(input("Please enter the cost: "))
            break

        except ValueError:
            print("\nInput error: cost entered should be a decimal number. Please try again.")


    # Use a while loop to request the shoe quantity from the user and validate the input. 
    while True:

        try:
            capture_quantity = int(input("Please enter the quantity in stock: "))

            if capture_quantity >= 0:
                break
            else:
                print("\nInput error: quantity entered should be a positive whole number. Please try again.")

        except ValueError:
            print("\nInput error: quantity entered should be a positive whole number. Please try again.")


    # Create the shoe object and add it to shoe_list.
    shoe_list.append(Shoe(capture_country, capture_code, capture_product, str(capture_cost), str(capture_quantity)))
    
    # Write the updated version of the shoe list to the inventory file. 
    update_inventory()


# This function iterates over the shoes list and uses the __str__ method to display the details of all of the shoes. 
def view_all():   

    for i in range(0, len(shoe_list)):
        print(shoe_list[i].__str__())


# This function finds the shoe object(s) with the lowest quantity and then asks the user whether to re-stock the shoe. 
# If the shoe is re-stocked, the new quantity is updated in shoe_list and in the file inventory.txt. 
def re_stock():   
    
    # Set up a list to store the indices of the lowest quantity shoes in shoe_list (in case there are more than one).
    re_stock_shoes = []

    # Set the first shoe in the list to the lowes_quantity initially.
    lowest_quantity = shoe_list[0].get_quantity()
    lowest_quantity_index = 0

    # Use a for loop to check through the rest of the list for lower quantity shoes.
    for i in range(1, len(shoe_list)):

        if lowest_quantity >= shoe_list[i].get_quantity():
            lowest_quantity = shoe_list[i].get_quantity()
            lowest_quantity_index = i
    
    # Add the lowest quantity shoe index to the list of shoes to re-stock.
    re_stock_shoes.append(lowest_quantity_index)

    # The code above finds the last shoe in the list with the lowest quantity. Check back through the list before this to see if there are other
    # shoes with the lowest quantity in stock. 
    for j in range(0, lowest_quantity_index):

        if shoe_list[j].get_quantity() == lowest_quantity:
            re_stock_shoes.append(j)

    # For each of the lowest quantity shoes identified, give the user the option to re-stock these shoes. 
    for k in range(0, len(re_stock_shoes)):

        re_stock_number = None

        while re_stock_number == None:
        
            # Ensure the user's input is valid.
            try:   
                re_stock_number = int(input(f'''\nThe shoe with the lowest stock count is {shoe_list[re_stock_shoes[k]].product}. There are {lowest_quantity} in stock.
To re-stock this shoe please enter the quantity of shoes to be added to the stock(enter 0 if you do not wish to re-stock): '''))

                if re_stock_number < 0:
                    print("\nInput error: please try again.")
                    re_stock_number = None

                # If the input is valid, update the shoe quantity in shoe_list.
                else:
                    total_stock = shoe_list[re_stock_shoes[k]].get_quantity() + re_stock_number
                    shoe_list[re_stock_shoes[k]].quantity = str(total_stock)   

            except ValueError:
                print("\nInput error: please try again.")

    # Write the updated version of shoe_list to the inventory file. 
    update_inventory()


# This function uses the shoe code to search for a shoe in the list and prints the all of the information about that shoe to the screen. 
def search_shoe():

    # Use a while loop to request a shoe code from the user and ensure the input is valid by checking it matches the code format e.g. SKU12345
    input_check = False

    while input_check == False:   
        
        while True:
            
            input_code = input("\nPlease enter the shoe code to search for a shoe: ")

            if input_code.strip()[0:3] == 'SKU' and len(input_code.strip()) == 8:
                break
            else:
                print("\nShoe codes all begin with SKU and are 8 characters long. Please try again.")

        # When the user has entered a code which has the correct format, check if there is a shoe with that code in shoe_list.
        for i in range(0, len(shoe_list)):

            # If a matching shoe is found, call the print_shoe function to print the shoe information to the screen. 
            if shoe_list[i].code == input_code:
                input_check = True
                print(shoe_list[i].__str__())
        
        # If the shoe code cannot be found, print a message to inform the user.
        if input_check == False:
            print("\nShoe not found.")
            break


# This function uses the formula: value = cost * quantity to calculate the stock value for each product and prints the results to the screen. 
def value_per_item():
    
    print("\n")

    for i in range(0, len(shoe_list)):   

        value = shoe_list[i].get_cost()*shoe_list[i].get_quantity()

        print(f'''Product: {shoe_list[i].product}     
Value: {value}R
''')   


# This function determines which shoe product(s) has the highest quantity of stock and prints that this shoe is for sale. 
def highest_qty():

    # Set the first shoe in the list as the highest quantity shoe initially.
    highest_quantity = shoe_list[0].get_quantity()    
    highest_quantity_shoe = shoe_list[0]
    highest_quantity_index = 0

    # Use a for loop to check through the rest of the list to find the shoes with the highest quantity.
    for i in range(1, len(shoe_list)):

        if highest_quantity <= shoe_list[i].get_quantity():
            highest_quantity = shoe_list[i].get_quantity()
            highest_quantity_shoe = shoe_list[i]
            highest_quantity_index = i

    print(f"\n{highest_quantity_shoe.product} is for sale.")

    # The code above finds the last shoe in the list which has the highest quantity. 
    # Check through the shoes list up until this point again to see whether more than one shoe has the highest quantity. 
    for j in range(0, highest_quantity_index):

        if shoe_list[highest_quantity_index].get_quantity() == shoe_list[j].get_quantity():
            print(f"\n{shoe_list[j].product} is for sale.")

    


#==========Main Menu=============

# Start by calling the read_shoes_data function to read from the inventory.txt file and populate shoes_list.
read_shoes_data() 

# Use a while loop to present the main menu to the user until they select to exit the program.
while True:

    user_selection = input('''
Please select an option from the menu:

    c - Capture shoe data
    rs - Re-stock lowest quantity shoe
    ss - Search shoes
    va - View all shoes
    dv - Display stock value of all shoes
    sh - Sell highest quantity shoe
    e - exit

    : ''').lower().strip()

    # If the user selects to capture shoe data, call the capture_shoes function.
    if user_selection == 'c':
        capture_shoes()

    # If the user selects to re-stock the lowest quantity shoe, call the re-stock function.
    elif user_selection == 'rs':
        re_stock()

    # If the user selects to search shoes, call the search_shoe function.
    elif user_selection == 'ss':
        search_shoe()
    
    # If the user selects to view all shoes, call the view_all function.
    elif user_selection == 'va':
        view_all()

    # If the user selects to display the stock value of all shoes, call the value_per_item function. 
    elif user_selection == 'dv':
        value_per_item()

    # If the user selects to sell the highest quantity shoe, call the highest_qty function. 
    elif user_selection == 'sh':
        highest_qty()

    elif user_selection == 'e':
        exit()

    else:
        print("\nInput error: please try again.")


