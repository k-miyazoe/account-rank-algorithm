class Human:
    def __init__(self, name="tanaka", age=20):
        self.name = name
        self.age = age
    def show(self):
        print(f"My name is {self.name}. My age is {self.age}.")
    hm1 = Human()
    hm1.show()
    hm2 = Human("sato", 21)
    hm2.show()
    hm2 = Human(age=30)
    hm2.show()