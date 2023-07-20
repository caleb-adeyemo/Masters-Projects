# from experta import *
#
#
# class Ticket(Fact):
#     def __init__(self, origin=None, destination="None"):
#         self.origin = origin
#         self.destination = destination
#
#
# class TicketRules(KnowledgeEngine):
#     @Rule(NOT(Ticket(origin=None), Ticket(destination=None)))
#     def get_origin(self):
#         print("Got here")
#
#
# if __name__ == "__main__":
#     # Create TicketRule object
#     ticket_rule = TicketRules()
#     ticket_rule.reset()
#
#     # Create ticket object
#     ticket = Ticket(origin="Lagos", destination="Abuja")
#     ticket_rule.declare(ticket)
#     ticket_rule.run()


from experta import *
class Person(Fact):
    name = Field(str)
    age = Field(int)

class AgeRules(KnowledgeEngine):
    @Rule(Person(name=MATCH.name, age=P(lambda x: x > 20)))
    def allowed_to_drink(self, name):
        print(f"{name}, you are allowed to drink")

    @Rule(Person(name=MATCH.name, age=P(lambda x: x <= 20)))
    def not_allowed_to_drink(self, name):
        print(f"{name}, you are not allowed to drink")

people = [
    Person(name="Alice", age=18),
    Person(name="Bob", age=25),
    Person(name="Charlie", age=30)
]

engine = AgeRules()
engine.reset()
engine.declare(*people)
engine.run()