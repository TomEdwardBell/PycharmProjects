import datetime

#__________________________________________
#TASK 1
#    - Making an estimate
#    - Unique Estimate Number
#    - Total Cost
#    - +20%

parts_and_prices = [
    ["Processor ", {"p3": 100, "p5": 120, "p7": 180}],
    ["Amount of RAM (GB) ", {"16 GB": 75, "32 GB": 150}],
    ["Amount of Storage (TB) ", {"1 TB": 50, "2 TB": 100}],
    ["Screen size (inches) ", {"19 in": 65, "23 in": 120}],
    ["Case ", {"mini": 40, "midi": 70}],
    ["Number of USB ports ", {"2 USB": 10, "4 USB": 20}]
    ]

anotherestimate = "yes"

estimates = []
while anotherestimate == "yes":
        estimateparts = []
        estimatecosts = 0
        for parttype in parts_and_prices: #"Processor" or "Case"
            print ("\nPart type: " + parttype[0]) # Prints "Part type: Processor" or "Part type: Case"

            for part in parttype[1]:
                print("   - Name: "+ part + "  Price: " + str(parttype[1][part]))

            validchoice = False
            while validchoice == False:
                userchoice = input("Which part would you like to order? ")
                try:
                    partname = userchoice
                    partcost = parttype[1][partname]
                    validchoice = True
                except:
                    print ("Not a valid part choice")
            estimateparts.append(partname)
            estimatecosts = estimatecosts + partcost

        print("Estimate Finished")
        print ("Estimate is: " + str(estimateparts))
        estimatecosts = estimatecosts * 1.2
        print ("Estimate costs: "+ str(estimatecosts))
        estimates.append({"parts":estimateparts,
                          "cost": estimatecosts})

        anotherestimate = input("Would you like to make another estimate (yes / no): ")

#_________________________________________
#TASK 2
#    - Place an order
#    - Stock Checking
#    - Update Stock levels
#    - Add
#        - Customer's details
#        - Date
#    - Print two copies of the order
#        - One for customer
#        - One for shop

parts_and_stock = {"p3": 100, "p5": 100, "p7":100,
                  "16 GB":100, "32 GB": 100,
                  "1 TB": 100, "2 TB": 100,
                  "19 in": 100, "23 in": 100,
                  "mini": 100, "midi": 100,
                  "2 USB": 100, "4 USB": 100}

orders = []
#estimates = [ # Decided by Task one These are samples
#    {"parts":["p3", "32 GB", "2 TB", "19 in", "mini", "2 USB"], "cost":558},
#    {"parts":["p3", "32 GB", "2 TB", "19 in", "mini", "4 USB"], "cost":570},
#    {"parts":["p3", "32 GB", "2 TB", "19 in", "midi", "2 USB"], "cost":594},
#    {"parts":["p7", "32 GB", "2 TB", "19 in", "mini", "2 USB"], "cost":654}
#]

for estimate in estimates:
    all_in_stock = True
    for item in estimate["parts"]:
        if parts_and_stock[item] < 1:
            all_in_stock = False

    if all_in_stock == False:
        print("Sorry, not all items in stock")

    if all_in_stock == True:
        for item in estimate["parts"]:
            parts_and_stock[item] = parts_and_stock[item] - 1
        current_order = dict(estimate)
        current_order["date"] = datetime.date.today()
        current_order["number"] = len(orders) + 1
        current_order["details"] = "Bob"
        orders.append(current_order)


#_______________________________________
#TASK 3
#    - End Of Day Summary
#    - Number of orders made
#    - Total number of each component sold
#    - Value of the orders

#orders = [] # Each item in the list is a dictionary, with "parts", "cost", "date", and "details"
todays_orders = []
total_money = 0

for order in orders:   # Makes today's order
    if order["date"] == datetime.date.today():
        todays_orders.append(order)

print("Number of orders made: ", len(todays_orders))

parts_and_count = {"p3": 0, "p5": 0, "p7":0,
                  "16 GB":0, "32 GB": 0,
                  "1 TB": 0, "2 TB": 0,
                  "19 in": 0, "23 in": 0,
                  "mini": 0, "midi": 0,
                  "2 USB": 0, "4 USB": 0}

print("**************")
for order in todays_orders:
    print("-------------")
    for info in order:
        print(info + ": " +str(order[info])) #e.g. "cost: 300" or "date: 2018-03-31"

    for part in order["parts"]:
        parts_and_count[part] = parts_and_count[part] + 1

    total_money = total_money + order["cost"]

print("**************")

for part in parts_and_count:
    print ("Number of " + part + " sold today: " + str(parts_and_count[part]))


print("**************")
print ("Total money made: £" + str(total_money))