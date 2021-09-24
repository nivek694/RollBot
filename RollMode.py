import random
from abc import ABC, abstractmethod
class Mode:

    
    '''The dice system to be used by the bot'''
    @staticmethod
    @abstractmethod
    def roll(message) ->str:
        pass

    '''Makses the class roll using this system'''
    @staticmethod
    @abstractmethod
    def setMode():
        pass

    '''Returns the name of the mode'''
    @staticmethod
    @abstractmethod
    def toString()-> str:
        pass

'''Class for operating in Shadowrun'''
class ShadowrunMode(Mode):
    '''Rolls a given number of dice and returns the dice roll. Gives the number of rolls of 5 or above if given with no postscipt or with "no edge".
    Gives the number of rolls of 4 or above if given the postscript "edge".'''
    @staticmethod
    def roll(message)-> str:
        #print("rolled")
        msg = message.content.replace("!roll", "")
        #print(msg)
        total = 0
        threshold = 5
        output = ""
        thisRoll = 0
        glitch = 0
        glitchMessage = ""
        msg = msg.replace("no edge", "")
        if(msg.find("edge") != -1):
            msg = msg.replace("edge", "")
            #print("edge replaced")
            threshold = 4
        #print(msg)
        if(msg.strip().isdigit()):
            for i in range(int(msg)):
                thisRoll = random.randint(1, 6)
                output += str(thisRoll) + ','
                if thisRoll >= threshold:
                    total += 1
                if thisRoll == 1:
                    glitch += 1

        else:
            return "Error: Please enter the number of dice for shadowrun mode"

        if glitch >= int(msg) / 2:
            glitchMessage = "\n Glitch"
            
        return "*Rolls* \n" + output.rstrip(',') + '\nTotal: ' + str(total)+ glitchMessage

    '''Makses the class roll using this system'''
    @staticmethod
    def setMode():
        return ShadowrunMode()
    @staticmethod
    def toString() -> str:
        return "shadowrun"

'''Class for operating in Dnd'''
class dndMode(Mode):
    '''Outputs a string of a roll of a given number of dice, can be expanded to handle different systems'''
    @staticmethod
    def roll(message) -> str:
        #Remove !roll from the message
        msg = message.content.replace("!roll", "")
        #print(msg)
        bonus = 0
        #Handle bonus
        if(msg.find('+') != -1):
            part = msg.rpartition('+')
            bonus = int(part[2])
            msg = part[0]
        #Handle penelty
        if(msg.find('-') != -1):
            part = msg.rpartition('-')
            bonus = int(part[1] + part[2].strip())
            msg = part[0]
        #Handle throwing multable dice
        if(msg.find('d') != -1):
            #Handle finding number of dice and type of die
            diceList = msg.rpartition('d');

            numberOfDice = diceList[0]
            dieSize = diceList[2]
            return "*Rolls* \n" + dndMode.rollOutput(numberOfDice, dieSize, bonus)
        
        elif(msg.strip().isdigit()): #Handle one die on its own
            return "*Rolls* \n" + dndMode.rollOutput(1, msg, bonus)
        else: #Handle input with no die.
            return "Error: Please input either a number on its own or 2 numbers in the form xdy."
        

    '''
    Output is the rolls of the dice, seperated by commas, and the total ammount rolled
    '''
    @staticmethod
    def rollOutput(numberOfDice, dieSize, bonus):
        total = bonus
        output = ""
        thisRoll = 0
        if(str(numberOfDice).replace(" ", "") == ""): #default to throwing one die
            numberOfDice = 1
        for i in range(int(numberOfDice)): #throw numberOfDice dice
            thisRoll = random.randint(1, int(dieSize))
            output += str(thisRoll) + ','
            total += thisRoll
        bonusText = ""
        if(bonus != 0): #Add bonus
            bonusText = " + " + str(bonus)
        return output.rstrip(',') + bonusText + '\nTotal: ' + str(total)

    '''Retuns an instance of dndMode'''
    @staticmethod
    def setMode():
        return dndMode()

    '''Returns the id of the mode'''
    @staticmethod
    def toString():
        return "dnd"

'''Class for operating Monster of the Week'''
class MotwMode(Mode):
    @staticmethod
    def roll(message)-> str:
        msg = message.content.replace("!roll", "")
        negative = False
        if(msg.find("+") != -1):
            msg.replace("+","")
        if(msg.strip() == ""):
            msg = 0
        total = int(msg)

        output = ""
        thisRoll = 0
        for i in range(2):
            thisRoll = random.randint(1, 6)
            output += str(thisRoll) + ','
            total += thisRoll
        rollResult = "*Rolls* \n" + output.rstrip(',') + '\nTotal: ' + str(total) + "\nResult: "
        if(total < 7):
            rollResult += "Failure"
        elif(total < 10):
            rollResult += "7-9"
        elif(total < 12):
            rollResult += "10+"
        else:
            rollResult += "12+"
        return rollResult
    @staticmethod
    def setMode():
        return MotwMode()
    @staticmethod
    def toString() -> str:
        return "motw"
            
'''Class for operating FATE'''       
class FateMode(Mode):
    @staticmethod
    def roll(message)-> str:
        #roll
        msg = message.content.replace("!roll", "")
        negative = False
        if(msg.find("+") != -1):
            msg.replace("+","")
        if(msg.strip() == ""):
            msg = "0"
        total = int(msg)
        output = ""
        thisRoll = 0

        for i in range(4):
            thisRoll = random.randint(-1,1)
            if(thisRoll == 1):
                output += "+, "
            elif(thisRoll == 0):
                output += "[ ], "
            else:
                output += "-, "
            total += thisRoll
        return ":game_die:*Rolls*:game_die: \n" + output.rstrip(',') + '\nTotal: ' + str(total)

    @staticmethod
    def setMode():
        return FateMode()
    @staticmethod
    def toString()-> str:
        return "fate"

'''Class for operating in Mutants and Masterminds'''
class MnMMode(Mode):
    '''The dice system to be used by the bot'''
    @staticmethod
    def roll(message)-> str:
        #Rolls take the form of <number> vs <number>, where the first number is the agressors roll and the second is the defenders dc, or <number>, where 
        # <number> is the agressors roll

        #Remove !roll from the message
        msg = message.content.replace("!roll", "")
        rand = random.randint(1,20)
        #rand = 20 #For testing event of nat 20
        #Handle nat 20
        degrees = 1 if rand == 20 else 0
        if(msg.rfind("vs") != -1):
            #process with DC. Provide digrees of sucsess

            results = str(msg).partition("vs")
            roll = int(results[0]) + rand
            #print(results[2])
            dc = int(results[2])
            if (roll >= dc):
                #roll wins
                degrees += int((roll - dc) / 5) + 1

                return "*Rolls*\nDie Roll: " + str(rand) + "\nTotal: " + str(roll) + "\n" + str(degrees) + " degrees of succsess"
            else:
                if(rand == 20):
                    degrees = -1
                degrees += int((dc - roll) / 5) + 1
                if(degrees == 0):
                    return "*Rolls*\nDie Roll: " + str(rand) + "\nTotal: " + str(roll) + "\n" + str(1) + " degree of succsess"
                else:
                    return "*Rolls*\n" + "Die Roll: " + str(rand) + "\nTotal: " + str(roll) + "\n" + str(degrees) + " degree(s) of failure"
                    


        else:
            #Just process roll
            if (str(msg).strip() == ""):
                msg = 0
            bonus = int(msg)
            return "*Rolls*\nDie Roll: " + str(rand)  + "\n Total: "+ str(rand + bonus)

    '''Makses the class roll using this system'''
    @staticmethod
    def setMode():
        return MnMMode()

    '''Returns the name of the mode'''
    @staticmethod
    def toString()-> str:
        return "mnm"


class CofdMode(Mode):
    @staticmethod
    def rollDie() -> int:
        return random.randint(1,10)


    @staticmethod
    def cofdRoll(pool :int, again : int, rote  : bool) -> str:
        sucsess = 0
        output = ""
        nextIsExtra = False
        thisIsExtra = False
        if(rote):
            #Handle rote action
            fails = 0
            temp = 0
            for i in range(pool):
                temp = 1
                first = True
                while(temp > 0):
                    roll = CofdMode.rollDie()
                    if(not first):
                        output += "("
                    output += str(roll)
                    if(not first):
                        output += ")"
                    if(roll > 7):
                        sucsess += 1
                    elif(first):
                        fails += 1
                    if(roll >= again):
                        temp += 1
                    output += ", "
                    first = False
                    temp -= 1
            output += "\nRerolls: "
            for i in range(fails):
                temp = 1
                first = True
                while(temp > 0):
                    roll = CofdMode.rollDie()
                    if(not first):
                        output += "("
                    output += str(roll)
                    if(not first):
                        output += ")"
                    if(roll > 7):
                        sucsess += 1
                    if(roll >= again):
                       temp += 1
                    output += ", "
                    first = False
                    temp -= 1
        else:
            #Handle normal roll
            while(pool > 0):
                thisIsExtra = nextIsExtra
                nextIsExtra = False
                if(thisIsExtra):
                    output += "("
                roll = CofdMode.rollDie()
                output += str(roll)
                if(roll >= again):
                    pool += 1
                    nextIsExtra = True

                if(roll > 7):
                    sucsess += 1
                if(thisIsExtra):
                    output += ")"
                output += ", "
                pool -= 1
        output += "\n sucsesses = " + str(sucsess)

        return output
    '''The dice system to be used by the bot'''
    @staticmethod
    def roll(message : str) ->str:
        msg = message.content.replace("!roll", "")
        again = 10
        rote = False
        if(msg.find("again") != -1):
            if(msg.find("9-again") != -1):
                again = 9
                msg = msg.replace("9-again", "")
            elif(msg.find("8-again") != -1):
                again = 8
                msg = msg.replace("8-again", "")
            elif(msg.find("no-again") != -1):
                again = 11
                msg = msg.replace("no-again", "")
        if(msg.find("rote") != -1):
            rote = True;
            msg = msg.replace("rote", "")
        print(msg)
        if(msg.strip().isdigit()):
            pool = int(msg)
            return CofdMode.cofdRoll(pool, again, rote)
        else:
            return "Error: Roll invaled"

    '''Makses the class roll using this system'''
    @staticmethod
    def setMode():
        return CofdMode()

    '''Returns the name of the mode'''
    @staticmethod
    def toString()-> str:
        return "cofd"