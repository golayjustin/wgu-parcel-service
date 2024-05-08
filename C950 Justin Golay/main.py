#Student Name: Justin Golay     Student ID: 010176782
import csv
import math
import Truck
import datetime

#Create a package class to store relevant information for each package that can later be referenced
class Package():
    def __init__(self, id, address, city, state, zip, deliveryDeadline, mass, specialInstructions, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.mass = mass
        self.specialInstructions = specialInstructions
        self.status = status
        self.departTime = None
        self.deliveryTime = None

    #Define a method to allow the package to be printed as a string for users
    def __str__(self):
        return f'ID:{self.id} | Address:{self.address}, {self.city}, {self.state}, {self.zip} | '\
               f'Mass:{self.mass} | Deadline:{self.deliveryDeadline} | Depart Time:{self.departTime} | '\
               f'Delivery Time:{self.deliveryTime} | Status:{self.status}'

    #Define a function to assist with viewing packages in hash table
    def __repr__(self):
        return str(self)

    #Define a function to calculate package's status that takes input from user
    #Time Complexity O(1)
    def updateStatus(self, userEnteredTime):
        #Compare delivery time and input from user
        if self.deliveryTime < userEnteredTime:
            self.status = "Delivered"
        elif self.departTime < userEnteredTime:
            self.status = "En route"
        else:
            self.status = "At Hub"


#Create a hash table to store packages for later look up
#Hash table is based on hash table provided in WGU resources
class ChainingHashTable:
    #Initialize the hash table with a empty list
    #Then use a loop to append 40 buckets
    # Time Complexity O(N)
    # Space Complexity O(N)
    def __init__(self, buckets=40):
        self.table = []
        for package in range(buckets):
            self.table.append([])

    #Create a method to insert and update items
    # Time Complexity for this method is O(N)
    def insert(self, key, item):
        #Use a simple hash function to identify the correct bucket for insertion
        # Time Complexity O(1)
        bucket = key % len(self.table)
        listOfBuckets = self.table[bucket]

        #Update key if in bucket instead of causing error
        # Time Complexity O(N)
        for keyNumber in listOfBuckets:
            #Print the key number
            if keyNumber[0] == key:
                keyNumber[1] = item
                return True

        #Insert the item at the end of the list if appropriate
        # Time Complexity O(1)
        keyNumber = [key, item]
        listOfBuckets.append(keyNumber)
        return True

    #Create a function to find an item given a key
    # Time Complexity for this method is O(N)
    def search(self, key):
        #Find the bucket list with the item
        # Time Complexity O(1)
        bucket = key % len(self.table)
        listOfBuckets = self.table[bucket]

        #In the correct bucket list, find the key
        # Time Complexity O(N)
        for keyNumber in listOfBuckets:
            #Return the item if found
            if keyNumber[0] == key:
                return keyNumber[1]
        return None


#Create a hash table object from the ChainingHashTable class
hashTable = ChainingHashTable()

#Open the CSV file and use a loop to save each package in a package object
#Then insert the package object into the hash table
#Time Complexity O(N)
#Space Compleixty O(N)
with open('packages.csv') as csvfile:
    packageFile = csv.reader(csvfile)
    for row in packageFile:
        id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        zip = row[4]
        deliveryDeadline = row[5]
        mass = row[6]
        specialInstructions = row[7]
        status = "At Delivery Hub"
        package = Package(id, address, city, state, zip, deliveryDeadline, mass, specialInstructions, status)
        hashTable.insert(id, package)

#Import the addresses and store them in a list for reference
# Time Complexity O(1)
# Space Complexity O(N)
with open("addresses.csv") as newCsvFile:
    addressFile = csv.reader(newCsvFile)
    addressFileList = list(addressFile)

#Import distances and save them in a list for reference
# Time Complexity O(1)
# Space Complexity O(N)
with open("distances.csv") as csvfile:
    distancesFromFile = csv.reader(csvfile)
    distancesFromFileList = list(distancesFromFile)

#Define a function that can find the distance between two locations
# Time Complexity O(1)
def distanceBetweenCities(xValue, yValue):
    #Reference the distances list with indexes
    distanceBetweenCities = distancesFromFileList[xValue][yValue]
    #Switch indexes if first attempt returns an empty string
    if distanceBetweenCities == '':
        distanceBetweenCities = distancesFromFileList[yValue][xValue]
    return float(distanceBetweenCities)

#Define a function to return the index of an address
#This will return the index needed for distanceBetweenCities function
# Time Complexity O(N)
def getAddress(address):
    for row in addressFileList:
        if address in row[2]:
            return int(row[0])

#Define a function utilizing nearest neighbor algorithm
#The function also completes the delivery simulation
# Time Complexity for this function is O(N^2)
def nearestNeighborSearchAlgorithm(truck):
    #Initiate an empty list
    unsortedPackages = []
    #Use a for loop to place each package from the hash table into the empty list
    # Time Complexity O(N)
    # Space Complexity O(N)
    for packageId in truck.packages:
        searchedPackage = hashTable.search(packageId)
        unsortedPackages.append(searchedPackage)
    #clear the packages from each truck so that they can be reloaded in an optimal delivery order
    truck.packages.clear()

    #Use a while loop to reload the trucks and update package information for the simulation
    # Time Complexity O(N^2)
    # Space Compleixty O(1)
    while len(unsortedPackages) > 0:
        #Initiate next address with a large value
        nextAddress = math.inf
        nextPackage = None
        #Use a for loop to search each package and find the nearest neighbor
        for eachPackage in unsortedPackages:
            #Use the getAddress function to find an index for current address and a package
            truckAddress = getAddress(truck.address)
            eachPackageAddress = getAddress(eachPackage.address)
            # Use those indexes to complete distancesBetweenCities method and find the distance between locations
            if distanceBetweenCities(truckAddress, eachPackageAddress) <= nextAddress:
                #Update next address for shortest distance to current location
                nextAddress = distanceBetweenCities(truckAddress, eachPackageAddress)
                nextPackage = eachPackage
        #Reload truck with each package
        truck.packages.append(nextPackage.id)
        #Remove the package loaded onto truck from the unsorted packages list
        unsortedPackages.remove(nextPackage)
        #Update total truck mileage needed to deliver packages
        truck.mileage += nextAddress
        #Update truck's current address
        truck.address = nextPackage.address
        #Update the truck's time
        truck.time += datetime.timedelta(hours=nextAddress/18)
        #Update each package's delivery time
        nextPackage.deliveryTime = truck.time
        #Update each package's departure time based on truck's departure time
        nextPackage.departTime = truck.departTime

#Define a function to return the truck to the hub after its last delivery.
#This is used so that Truck 3 does not leave until Truck 1's driver returns to the hub.
# Time Complexity O(1)
def returnToHub(truck):
    currentAddress = truck.address
    #Use a function to calculate distance between current address and hub
    hubAddress = "4001 South 700 East"
    distanceToHub = distanceBetweenCities(getAddress(truck.address), getAddress(hubAddress))
    #Update truck mileage
    truck.mileage += distanceToHub
    #Update truck's address
    truck.address = hubAddress
    #Update truck's time
    truck.time += datetime.timedelta(hours=distanceToHub / 18)


#Load Truck 1 primarily with packages that have an early morning delivery deadline
truck1 = Truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40, 19], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

#Complete the nearest neighbor algorithm with Truck 1 to simulate deliveries
nearestNeighborSearchAlgorithm(truck1)

#Return Tuck 1 to the hub
returnToHub(truck1)

#Load Truck 2
truck2 = Truck.Truck(16, 18, None, [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 17, 18, 21, 22, 36, 38], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

#Complete the nearest neighbor algorithm with Truck 2 to simulate deliveries
nearestNeighborSearchAlgorithm(truck2)

#Load Truck 3 and set departure time to the same time Truck 1 returns to the hub
truck3 = Truck.Truck(16, 18, None, [23, 24, 26, 27, 28, 9, 32, 33, 35, 39, 25], 0.0, "4001 South 700 East",
                     (truck1.time))

#Complete the nearest neighbor algorithm with Truck 3 to simulate deliveries
nearestNeighborSearchAlgorithm(truck3)

#The main class primarily facilitates user interface to provide the user with queried information
# Time Complexity O(N)
class Main:
    #Calculate the total mileage for all trucks and print this number for the user
    totalMileage = truck1.mileage + truck2.mileage + truck3.mileage
    print("Welcome to Western Governors University Parcel Service")
    print("The total mileage for the delivery of these packages is: " + str(totalMileage) + " miles")

    # The user will be asked to start the process by entering the word "time"
    #Use lower() function to reduce potential errors related to capitalization
    userStart = input("To start please type the word 'Start' (All else will cause the program to quit).").lower()

    # User must enter the correct input or the program will exit
    if userStart == "start":
        try:
            # The user will be asked to enter a specific time
            userTime = input("Please enter a time to search for the status of packages. "
                              "Use the following format, HH:MM:SS")
            #Separate string to be converted to a time
            # Time Complexity O(N)
            (h, m, s) = userTime.split(":")
            #Set separated strings to integers and et time utilizing timedelta
            userEnteredTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # The user will be asked if they want to see the status of all packages or only one
            #Use lower() function to reduce risk of errors due to capitalization
            packageQuantityInput = input("Would you like to look up one package or all? Enter 'one' or 'all')").lower()
            # If the user enters "one" the program will ask for one package ID
            if packageQuantityInput == "one":
                try:
                    #Prompt user to input a package ID number. Incorrect ID numbers will result in exit of program.
                    packageIdInput = input("Enter the numeric package ID")
                    #Search for package in hash table based in input ID
                    package = hashTable.search(int(packageIdInput))
                    #Update package's delivery status before printing package information
                    package.updateStatus(userEnteredTime)
                    print(package)
                #Exit program if given invalid input
                except ValueError:
                    print("Input Error. Program will exit. Please restart program.")
                    exit()
            # If the user types "all" the program will display all package information at once
            elif packageQuantityInput == "all":
                try:
                    #Use a for loop to reference hash table and print each package's information
                    # Time Complexity O(N)
                    for packageId in range(1, 41):
                        package = hashTable.search(packageId)
                        package.updateStatus(userEnteredTime)
                        print(package)
                except ValueError:
                    print("Input Error. Program will exit. Please restart program.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Input Error. Program will exit. Please restart program.")
            exit()
    elif input != "start":
        print("Input Error. Program will exit. Please restart program.")
        exit()