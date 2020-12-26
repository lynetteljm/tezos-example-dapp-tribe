import smartpy as sp
import time
 
class TezosSymptomChecker(sp.Contract):
    def __init__(self, hashedSecret, covidStatus):
        # Race details
        self.init(
            # background of user
            Background = {},
            # The owner is the user
            owner = sp.none,
            # records of symptom tests
            Records = {},
            # Hashed secret to verify owner
            hashedSecret = hashedSecret,
            #current COVID-19 status 
            covidStatus =covidStatus,
            score=0
 
        )
 
    @sp.entry_point
    def addOwner(self, params):
 
        sp.set_type(params.ConfirmedCase,sp.TString)
 
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
        sp.verify(params.ConfirmedCase=="No",message="Please isolate yourself and stay strong")
 
        # set the owner
        self.data.owner = sp.some(sp.sender)
 
    @sp.entry_point
    def changeStatus(self, params):
         # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
 
        # set the owner
        self.data.covidStatus = params.covidStatus
 
    @sp.entry_point
    def addBackground(self, params):
 
        sp.set_type(params.Age,sp.TString)
        sp.set_type(params.PostalCode,sp.TString)
        sp.set_type(params.ChronicDisease,sp.TString)
        sp.set_type(params.CommExposure,sp.TString)
 
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
 
        # set the background
        self.data.Background[sp.sender]={
            "Age":params.Age,
            "Postal Code":params.PostalCode,
            "Any Chronic Disease":params.ChronicDisease,
            "Student/living in communal setting":params.CommExposure
        }
 
    @sp.entry_point
    def addSympTest(self, params):
 
        # verify the secret to ensure that
        # the owner of the contract calls it
        sp.verify(sp.blake2b(params.secret) == self.data.hashedSecret)
 
        # Setting types
        sp.set_type(params.Time,sp.TInt)
        sp.set_type(params.Cough,sp.TString)
        sp.set_type(params.DiffBreathing, sp.TString)
        sp.set_type(params.Fever,sp.TString)
        sp.set_type(params.LossTasteSmell,sp.TString)
        sp.set_type(params.Diarrhoea,sp.TString)
        sp.set_type(params.Bodyache,sp.TString)
        sp.set_type(params.RunnyNose,sp.TString)
        sp.set_type(params.Sorethroat,sp.TString)
        sp.set_type(params.OverseasConfirmed,sp.TString)
        sp.set_type(params.Duration,sp.TString)
 
        # Adding the test results
        self.data.Records[params.Time] = {
            "Contact with Confirmed Case/Overseas in previous 14 days": params.OverseasConfirmed,
             "Cough": params.Cough, 
             "Difficulty Breathing":params.DiffBreathing,
            "Fever > 37.5 degrees":params.Fever,
            "Loss of Taste/Smell":params.LossTasteSmell,
            "Diarrhoea":params.Diarrhoea,
            "Bodyache":params.Bodyache,
            "Runny Nose":params.RunnyNose,
            "Sore Throat":params.Sorethroat,
            "Duration of symptoms in Days":params.Duration,
            "Evaluated Risk":""
        }
 
        #calculate risk
        sp.for item in self.data.Records[params.Time].items():
            sp.if item.key=="Bodyache":
                sp.if item.value=="Yes":
                    self.data.score += 3
            sp.if item.key=="Difficulty Breathing":
                sp.if item.value=="Yes":
                    self.data.score += 3
            sp.if item.key=="Fever > 37.5 degrees":
                sp.if item.value=="Yes":
                    self.data.score += 2
            sp.if item.key=="Cough":
                sp.if item.value=="Yes":
                    self.data.score += 2
            sp.if item.key=="Loss of Taste/Smell":
                sp.if item.value=="Yes":
                    self.data.score += 1
            sp.if item.key=="Diarrhoea":
                sp.if item.value=="Yes":
                    self.data.score += 1
            sp.if item.key=="Runny Nose":
                sp.if item.value=="Yes":
                    self.data.score += 1
            sp.if item.key=="Sore Throat":
                sp.if item.value=="Yes":
                    self.data.score+=1
            sp.if item.key=="Contact with Confirmed Case/Overseas in previous 14 days":
                sp.if item.value=="Yes":
                     self.data.score*=2
            sp.if item.key=="Duration of symptoms in Days":
                sp.if item.key!= "0-4 days":
                    self.data.score*=2
 
        sp.if self.data.Background[sp.sender]['Any Chronic Disease']=="Yes":
            self.data.score*=2
        sp.if self.data.Background[sp.sender]["Student/living in communal setting"]=="Yes":
            self.data.score*=2
        sp.if self.data.Background[sp.sender]["Age"]=="65 or older":
            self.data.score*=2
 
        sp.if self.data.score>=7:
            self.data.Records[params.Time]["Evaluated Risk"]="High"
        sp.else:
            sp.if self.data.score>0:
                self.data.Records[params.Time]["Evaluated Risk"]="Medium"
            sp.else:        
                self.data.Records[params.Time]["Evaluated Risk"]="Low"
 
 
    @sp.add_test(name="Tezos COVID-19 Symptom Checking app")
    def test():
 
        # A test scenario
        scenario = sp.test_scenario()
 
        # The hashed secret
        # input has to be valid hexadecimal
        hashedSecret = sp.blake2b(b'426c616168')
 
        # Create HTML output for debugging
        scenario.h1("COVID-19 Symptom Checker app")
 
        # The test owner who uses the app
        recordsOwner = sp.address("tz1N6VKpVbvXZ17UKm6RH8wJDvo5EWbCgMQB")
 
        # Initializing the app
        app = TezosSymptomChecker(hashedSecret, "Negative")
 
 
        # Add the app to the scenario
        scenario += app
 
        scenario.h2("User added to system")
        # Adding owner
        scenario +=app.addOwner(
            secret = b'426c616168',
            ConfirmedCase="No"
            ).run(sender = recordsOwner)
 
        # User sets background
        scenario.h2("User sets personal background")
 
        scenario += app.addBackground(
                        secret = b'426c616168',
                        Age = '15',
                        PostalCode = "510122",
                        ChronicDisease="No",
                        CommExposure="Yes"
                    ).run(sender = recordsOwner)
        # Changes to user's background
        scenario.h2("User changes personal background")
        scenario += app.addBackground(
                        secret = b'426c616168',
                        Age = '13-16',
                        PostalCode = "510122",
                        ChronicDisease="Yes",
                        CommExposure="Yes"
                    ).run(sender = recordsOwner)
 
        # Changes to user's background
        scenario.h2("User changes COVID status")
        scenario += app.changeStatus(
            secret = b'426c616168',
            covidStatus = "Positive"
            )
 
        scenario += app.changeStatus(
            secret = b'426c616168',
            covidStatus = "Negative"
            )
 
         # User takes symptom test
        scenario.h2("Checking of Symptoms")
        timeNow = int(time.time())
 
        scenario += app.addSympTest(
                        secret = b'426c616168',
                        OverseasConfirmed="No",
                        Cough="No",
                        DiffBreathing="No",
                        Time=timeNow,
                        Fever="Yes",
                        LossTasteSmell="No",
                        Diarrhoea="Yes",
                        Bodyache="No",
                        RunnyNose="Yes",
                        Sorethroat="No",
                        Duration="5-7 days"
                    ).run(sender = recordsOwner)