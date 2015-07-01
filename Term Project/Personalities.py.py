
class Personalities(object):
    def __init__(self):
        self.randVal = None
        self.control = 100

    ##Carry out actions based on what randVal is##

class basicP(Personalities):
    
    def __init__(self):
        self.super(basicP, self).__init__()
        self.dialogues = ["Where's my PSL?", "Let's go shopping!",
                        "Which Instagram filter should I choose?", "Carbs? Ew, no.",
                        "My best friend's name is Becca", "OMG, is that Ryan Gosling?!"]
        self.dialogueIndex = None
        
    def selectDialogue(self):
        self.index = random.random(0, len(self.dialogue)-1)
        self.dialogue = self.dialogues[self.index]

class kindP(Personalities):
    
    def __init__(self):
        self.super(kindP, self).__init__()
        self.dialogues = ["You look very nice today", "How is YOUR day doing?",
                          "You're my best friend"]
        self.happiness = 100 #Always *should be unphased by decreasing happiness
        self.appeal = "high"

        
    def selectDialogue(self):
        self.index = random.random(0, len(self.dialogue)-1)
        self.dialogue = self.dialogues[self.index]

class meanP(Personalities):
    
    def __init__(self):
        self.super(meanP, self).__init__()
        self.dialogues = ["You're ugly", "Your shoes look funny",
                          "Your face makes me mad", "I don't wanna"]
        self.appeal = "low"

    def selectDialogue(self):
            self.index = random.random(0, len(self.dialogue)-1)
            self.dialogue = self.dialogues[self.index]
            
class lazyP(Personalities):

    def __init__(self):
        self.super(lazyP, self).__init__()
        self.dialogues = ["I don't feel like it", "You can't make me",
                          "How about you do it instead?",
                          "My best friend's name is Garfield"]

    def selectDialogue(self):
        self.index = random.random(0, len(self.dialogue)-1)
        self.dialogue = self.dialogues[self.index]

class adventerousP(Personalities):
    
    def __init__(self):
        self.super(adventerousP, self).__init__()
        self.dialogues = ["Let's do something today!", "How about that nature?",
                          "Let's go!", "Go Do!"]
        self.wander = False

    def selectDialogue(self):
        self.index = random.random(0, len(self.dialogue)-1)
        self.dialogue = self.dialogues[self.index]

    def Wander(self):
        #wanders somewhere off screen for a given amount of time
        pass

class ambitiousP(Personalities):

    def __init__(self):
        self.super(ambitiousP, self).__init__()
        self.dialogues = ["I wanna be the very best",
                          "Can't is not in my vocabulary",
                          "That sounds awesome!"]
        self.appeal = "high"

    def selectDialogue(self):
        self.index = random.random(0, len(self.dialogue)-1)
        self.dialogue = self.dialogues[self.index]
