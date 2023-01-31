class Restaurant():

    def __init__(self, restaurant_name, cusisine_type, numbers):
        self.restaurant_name = restaurant_name
        self.cusisine_type = cusisine_type
        self.number_service = numbers

    def describe_restaurant(self):
        print("This restaurant is call " + str(self.restaurant_name))
        print("This restaurant make a " + str(self.cusisine_type))

    def open_restaurant(self):
        print("This restaurant is opeaning!")

    def number_served(self):
        if self.number_service > 0:
            print(str(self.number_service) + " peoples are eatting lunch")
        else:
            print("There no people in the restaurant!")

    def set_number_served(self, update_people):
        self.number_service += update_people


class IceCreamStand(Restaurant):

    def __init__(self, restaurant_name, cusisine_type, numbers):
        super().__init__(restaurant_name, cusisine_type, numbers)
        self.flavors = ['bulebarry', 'strawberry', 'fragantherb']

    def describe_icecreamstand(self):
        for tast in self.flavors:
            print("This restaurant have a " + str(tast) + " icecream!")


# my = Restaurant("Beijing", "DUCK", 45)
# my.describe_restaurant()
# my.open_restaurant()
# my.set_number_served(70)
# my.number_served()

# you = IceCreamStand("Beijing", "DUCK", 45)
# you.describe_icecreamstand()
# you.describe_restaurant()