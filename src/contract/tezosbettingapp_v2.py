import smartpy as sp
import random

class TezosBettingApp(sp.Contract):
    def __init__(self, track, hashedSecret):
        # Race details
        self.init(
            # The race track
            track = track,
            # The owner
            owner = sp.none,
            # Horses on the track
            horses = {},
            # Bets placed
            bets = {},
            # Hashed secret to verify owner
            hashedSecret = hashedSecret,
            winnerHorse = 0,
            winningPool = sp.tez(0)
        )
        
    @sp.entry_point
    def changeTrack(self, params):
        
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)

        # set the owner
        self.data.track = params.track
    
    @sp.entry_point
    def addOwner(self, params):
        
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
        
        # set the owner
        self.data.owner = sp.some(sp.sender)
        
    @sp.entry_point
    def addHorse(self, params):
        
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
        
        # Setting types
        sp.set_type(params.horseId, sp.TInt)
        sp.set_type(params.horseName, sp.TString)
       
        # Adding the horse
        self.data.horses[params.horseId] = {
            "horseName": params.horseName
        }
    
    @sp.entry_point
    def placeBet(self, params):
        
        # Setting types
        sp.set_type(params.betHorseId, sp.TInt)
        
        # store the bets details
        # Note: one bet per participant
        self.data.bets[sp.sender] = {
            params.betHorseId: sp.amount
        }
    
    @sp.entry_point
    def runRace(self, params):
        
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
        
        # select a winner
        winnerHorse = 1
        self.data.winnerHorse = winnerHorse
        
        # compute pool of the winning horse
        sp.for bet in self.data.bets.values():
            self.data.winningPool += bet.get(winnerHorse, sp.tez(0))
        
        # Distribute the winning 
        sp.for item in self.data.bets.items():
            winningBetAmount = item.value.get(self.data.winnerHorse, sp.tez(0))
            sp.if winningBetAmount != sp.tez(0):
                # split the pool
                toSend = sp.split_tokens(sp.balance, winningBetAmount, self.data.winningPool)
                sp.send(item.key, toSend)

    @sp.add_test(name="Tezos betting app")
    def test():

        # A test scenario
        scenario = sp.test_scenario()
        
        # The hashed secret
        # input has to be valid hexadecimal
        hashedSecret = sp.blake2b(b'426c616168')
        
        # Create HTML output for debugging
        scenario.h1("Tezos betting app")
        
        # The test owner of the racing field
        raceOwner = sp.address("tz1-raceOwner-address-1234")
        
        # Initializing the app
        app = TezosBettingApp("FAST", hashedSecret)
        
        
        # Add the app to the scenario
        scenario += app
        
        # Adding owner
        
        scenario += app.addOwner(secret = b'426c616168').run(sender = raceOwner)
        
        scenario += app.changeTrack(secret = b'426c616168', track="SLOW")
        
        # Adding horses
        scenario.h2("Horses on the field!")
        
        scenario += app.addHorse(
                        secret = b'426c616168',
                        horseId = 0,
                        horseName = "Pickle Rake"
                    ).run(sender = raceOwner)
        
        scenario += app.addHorse(
                        secret = b'426c616168',
                        horseId = 1,
                        horseName = "Seabiscuit"
                    ).run(sender = raceOwner)
                   
        scenario += app.addHorse(
                        secret = b'426c616168',
                        horseId = 2,
                        horseName = "Blaze"
                    ).run(sender = raceOwner)

        scenario += app.addHorse(
                        secret = b'426c616168',
                        horseId = 3,
                        horseName = "Shadowfax"
                    ).run(sender = raceOwner)
        
        # Placing bets
        scenario.h2("Placing bets")
        
        participantOne = sp.address("tz1-participantOne-address-1234")
        
        participantTwo = sp.address("tz1-participantTwo-address-1234")
        
        scenario += app.placeBet(betHorseId = 2).run(
                            sender = participantOne, 
                            amount = sp.tez(3)
                        )
        scenario += app.placeBet(betHorseId = 1).run(
                            sender = participantTwo, 
                            amount = sp.tez(5)
                        )
                        
        # Run the race
        scenario.h2("Run the race")
        scenario += app.runRace(secret = b'426c616168').run(sender = raceOwner)