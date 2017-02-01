import random
import json
import matplotlib.pyplot as plt
 

def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]

    # The output list that contains the gini coefficient for each customer
    ginis=[calculateGini(tables)]

    #for all other customers do
    for cust in range(2, customers+1):
            # rand between 0 and 1
            rand = random.random()
            # Total probability to sit at a table
            prob = 0
            # No table found yet
            table_found = False
            # Iterate over tables
            for table, guests in enumerate(tables):
                # calc probability for actual table an add it to total probability
                prob += guests / (cust)
                # If rand is smaller than the current total prob., customer will sit down at current table
                if rand < prob:
                    # incr. #customers for that table
                    tables[table] += 1
                    # customer has found table
                    table_found = True
                    # no more tables need to be iterated, break out for loop
                    break
            # If table iteration is over and no table was found, open new table
            if not table_found:
                tables.append(1)

            # calculateGini function is called to calculate the gini coefficient for the current customer according to the current available tables
            ginis.append(calculateGini(tables))
  
    return ginis

def calculateGini(tables):
    # m is calculated for each table as the example in the lecture
    tables_m=[]
    for table in tables:
        tables_m.append(table/sum(tables))

    gini=0
    denominator=0

    #formula used => Gini=(sum_over_S(sum_over_S(abs(m1-m2)))/
    #                       2*S*sum(m))
    # nested loop to loop on the list of tables twice and calculate the gini
    for table in tables_m:
        for table2 in tables_m:
            gini+=abs(table-table2)
        denominator+=table


    denominator=2*len(tables)*denominator

    gini=gini/denominator

    return gini
 
restaurants = 1000

ginis1 = generateChineseRestaurant(restaurants)
ginis2 = generateChineseRestaurant(restaurants)
ginis3 = generateChineseRestaurant(restaurants)
ginis4 = generateChineseRestaurant(restaurants)
ginis5 = generateChineseRestaurant(restaurants)


# I changed the colors for better visualization
customers=list(range(1,1001))
plt.plot(customers, ginis1, 'b', customers, ginis2, 'g',customers,ginis3, 'r',customers,ginis4, 'm',customers,ginis5, 'k')
plt.xlabel('Customers')
plt.ylabel('Gini Coefficient')
plt.show()






