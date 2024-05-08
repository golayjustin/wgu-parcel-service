import datetime

#Create a truck class with all required information
class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, departTime):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departTime = departTime
        self.time = departTime

#Create a method that allows truck information to be viewed as a string.
#This is not required for the simulation, but is useful to analyze truck information when developing simulation code
    def __str__(self):
        return f'Capacity <{self.capacity} Speed{self.speed} Load{self.load} Packages{self.packages} ' \
               f'Mileage{self.mileage} Address{self.address} Depart Time{self.departTime} Time{self.time}>'