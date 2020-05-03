import smartpy as sp

class TezosBettingApp(sp.Contract):
    def __init__(self, track):
        # Race details
        self.init(
            track = track,
            owner = sp.address("tz1-test-address"),
            horses = {}
        )
    
    @sp.entry_point
    def addOwner(self, params):
        self.data.owner = params.owner
    
    @sp.entry_point
    def addHorse(self, params):
        
        # Verifying that the owner of the racing field is adding the horse
        sp.verify(self.data.owner == sp.sender)
        
        # Setting types
        sp.set_type(params.horseId, sp.TInt)
        sp.set_type(params.horseName, sp.TString)
        
        # Adding the horse
        self.data.horses[params.horseId] = params
    
    @sp.entry_point
    def changeTrack(self, params):
        self.data.track = params.track
    
    @sp.add_test(name="Tezos betting app")
    def test():
        
        # A test scenario
        scenario = sp.test_scenario()
        
        # Create HTML output for debugging
        scenario.h1("Tezos betting app")
        
        # The owner of the racing field
        raceOwner = sp.address("tz1-raceOwner-address-1234")
        # raceOwner = sp.test_account("Race owner")
        
        # Initializing the app
        c1 = TezosBettingApp(
            "FAST"
            )
        scenario += c1
        
        # Adding owner
        scenario += c1.addOwner(owner = raceOwner)
        
        # Changing track
        scenario.h2("Changing track")
        scenario += c1.changeTrack(track = "SLOW")
        
        # Adding horses
        scenario.h2("Horses on the field!")

        scenario += c1.addHorse(
                        horseId = 0,
                        horseName = "Pickle Rake"
                    ).run(sender = raceOwner)
        
        scenario += c1.addHorse(
                        horseId = 1,
                        horseName = "Seabiscuit"
                    ).run(sender = raceOwner)
                    
        scenario += c1.addHorse(
                        horseId = 2,
                        horseName = "Blaze"
                    ).run(sender = raceOwner)
        scenario += c1.addHorse(
                        horseId = 3,
                        horseName = "Shadowfax"
                    ).run(sender = raceOwner)