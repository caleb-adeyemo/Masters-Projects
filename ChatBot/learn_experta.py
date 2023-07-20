from experta import *

class Ticket(Fact):
    start = Field(str, None)
    end = Field(str, None)

class Action(Fact):
    action = Field(str)
    pass

class TravelAgent(KnowledgeEngine):
    @DefFacts()
    def set_up(self):

        yield Action(action="greet")


    @Rule(Action(action="greet"))
    def hr(self):
        print("Hello")
        self.declare(Ticket())
        print(engine.facts)



    @Rule(Ticket(start=None))
    def do(self):

        print("Got your start location")



if __name__ == "__main__":
    engine = TravelAgent()
    engine.reset()  # Prepare the engine for the execution.
    engine.run()  # Run it!

# from experta import *
#
# class Greetings(KnowledgeEngine):
#     @DefFacts()
#     def _initial_action(self):
#         yield Fact(action="greet")
#
#     @Rule(Fact(action='greet'), NOT(Fact(name=W())))
#     def ask_name(self):
#         print(engine.facts)
#         self.declare(Fact(name=input("What's your name? ")))
#         print(engine.facts)
#
#     @Rule(Fact(action='greet'), Fact(name=W()))
#     def ask_second_name(self):
#         print(engine.facts)
#         self.declare(Fact(name=input("What's your second name? ")))
#         print(engine.facts)
#
#
#     @Rule(Fact(action='greet'),
#           NOT(Fact(location=W())))
#     def ask_location(self):
#         self.declare(Fact(location=input("Where are you? ")))
#
#     @Rule(Fact(name="caleb"))
#     def caleb(self):
#         print("caleb")
#
#     @Rule(Fact(action='greet'), Fact(name=MATCH.name), Fact(location=MATCH.location))
#     def greet(self, name, location):
#         print("Hi %s! How is the weather in %s?" % (name, location))
#
#
# if __name__ == "__main__":
#     engine = Greetings()
#     engine.reset()  # Prepare the engine for the execution.
#     engine.run()  # Run it!
