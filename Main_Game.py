def clr(noun):
    for X in range(15):
        print("")
    return ""
clr("t")

def get_input():
    command = raw_input(": ").split()
    try:
        verb_word = command[0].lower()
    except:
        while True:
            print("Invalid command!")
            command = raw_input(": ").split()
            try:
                verb_word = command[0]
                break
            except:
                continue
    print ""
    if verb_word in verb_dict:
        verb = verb_dict[verb_word]
    else:
        print("Unknown verb {}.").format(verb_word)
        return
    
    if len(command) == 2:
        noun_word = command[1]
        print(verb(noun_word))
    elif len(command) == 3:
        noun_word = command[1] + " " + command[2]
        print(verb(noun_word))
    else:
        print(verb("nothing"))

class GameSys:
    turn = False
    lootarget = "None"
    parrysuc = False
DGame = GameSys()


class Weapon:
    weapons = {}
    obj_name = ""
    desc = ""
    damage = 1
    speed = 1
    
    def __init__(self):
        
        Weapon.weapons[self.obj_name] = self
        
    def get_desc(self):
        print self.obj_name, "\n", self.desc, "\n", "Damage: {}".format(self.damage), "\n", "Speed: {}".format(self.speed)
        return ""
        
        
class RustBlade(Weapon):
    obj_name = "Rusty Blade"
    desc = "A sword from the depths of the Dungeon."
    damage = 2
    speed = 1
    
    
class ShortSwd(Weapon):
    obj_name = "Shortsword"
    desc = "A short, silver blade."
    damage = 3
    speed = 1
    

rustyblade = RustBlade()
shortswd = ShortSwd()


class GameObj:
    obj_name = ""
    desc = ""
    objects = {}
    health = 1
    damage = 0
    inv = []
    wepslot = []
    gold = 0
    stun = 0
    parry = 0
    
    def __init__(self, name):
        self.name = name    
        
        GameObj.objects[self.obj_name] = self
        if self.wepslot != []:
            self.damage += self.wepslot[0].damage
    def get_desc(self):
        return self.name + "\n" + self.desc
        
class Enemy(GameObj):
    damage = 1
    aware = 0
    
    
    def attack(self):
        if self.health <= 0 or self.aware == 0:
            return
        else:
            if self.stun == 1:
                self.stun = 0
                print self.obj_name, "has recovered!"
                return
            
            elif jt.block == 1:
                GameObj.objects['Knight'].health -= int(self.damage/2)
                actdam = int(self.damage/2)
                self.stun = 1
            
            else:
                GameObj.objects['Knight'].health -= self.damage
                actdam = self.damage
            print self.obj_name + " attacks you for {} damage!".format(actdam)
            if self.stun != 0:
                print self.obj_name, "is stunned!"
        if GameObj.objects['Knight'].health == 0:
            print self.obj_name + " killed you. Game Over."
            exit()


class Imp(Enemy):
    obj_name = "Imp"
    desc = "A foul creature."
    health = 6
    wepslot = [rustyblade]
    inv = ["Scimitar", shortswd]
    gold = 28
    def get_desc(self):
        if self.health >= 3:
            healthline = ""
        elif self.health == 2:
            healthline = "It has a wound on its arm."
        elif self.health == 1:
            healthline = "You think one more strike will finish it!"
        elif self.health <= 0:
            healthline = "It is dead."
        if self.aware == 0:
            awareline = "It hasn't noticed you yet."
        else:
            awareline = "It knows where you are."
        print self.name + "\n" + self.desc
        if self.health < 3:
            print healthline
        if self.wepslot != []:
            print "It is holding a {}.".format(self.wepslot[0].obj_name)
        if self.health > 0:
            return awareline
        else:
            return ""
            
            
class Player(GameObj):
    obj_name = "Knight"
    desc = "A world-reknowned dungeon cleanser."
    health = 15
    block = 0
    wepslot = [shortswd]
    inv = []
    def get_desc(self):
        print self.obj_name
        print self.desc
        print self.health, "health left."
        return ""


itemlist = ["Gold", "Scimitar", "Rusty Sword"
"Shortsword"]


jt = Player("Jt")
gob = Imp("Max")

def say(noun):
    return("You said {}").format(noun)
    
def printverbs(noun):
    for key in verb_dict:
        print(key)
    return ""

def examine(noun):
    if noun == "nothing" or noun == "room":
        keylist = (GameObj.objects).keys()
        for item in range(len(GameObj.objects)):
            print keylist[item]
        return ""
    elif noun in GameObj.objects or noun in Weapon.weapons:
        if noun in GameObj.objects:
            return GameObj.objects[noun].get_desc()
        else:
            return Weapon.weapons[noun].get_desc()
    else:
        return "There is no {} here.".format(noun)

def hit(noun):
    if noun == 'Knight':
        return "You decide not to."

    elif noun in GameObj.objects:
        thing = GameObj.objects[noun]
        if thing.health <= 0:
            return "It's already dead."
        else:
            DGame.turn = True
            if jt.wepslot != []:
                actdam = 1
                actdam += jt.wepslot[0].damage
            thing.health -= actdam
            if thing.health <= 0:
                return "You killed the {}".format(thing.obj_name) + "\n"
            else:
                if thing.aware == 0:
                    thing.aware = 1
                    thing.stun = 1
                
                return "You hit the {}!".format(thing.obj_name) + "\n"
    elif noun == "nothing":
        return "You hit nothing. Congrats."
    else:
        return "There is no {} here.".format(noun)

def block(noun):
    DGame.turn = True
    jt.block = 1
    return "You prepare to block..."
    
    
def loot(noun):
    if noun == "Knight" or noun == "self":
        GameSys.lootarget = "self"
        print "You have {} gold.".format(jt.gold)
        for item in jt.inv:
            if isinstance(item, (dict)) == True:
                for k in item:
                    print item[k], k
            elif isinstance(item, (Weapon, GameObj)) == True:
                print item.obj_name
            else:
                print item
        print "You are holding a {}.".format(jt.wepslot[0].obj_name)
        return ""
    elif noun in GameObj.objects:
        noun = GameObj.objects[noun]
        GameSys.lootarget = noun
        if noun.health > 0:
            return "You can't loot a live {}!".format(noun.obj_name)
        else:
            print "It has {} gold.".format(noun.gold)
            for item in noun.inv:
                if isinstance(item, dict):
                    for k in item:
                        print item[k], k
                elif isinstance(item, Weapon):
                    print item.obj_name
                else:
                    print item
            if isinstance(noun, Enemy) == True and noun.wepslot == []:
                return "It's hands are empty."
            elif isinstance(noun, Enemy) == True:
                return "It is holding a {}".format(noun.wepslot[0].obj_name)
    else:
        return "There is no {} here.".format(noun)

def pickup(noun):
    if GameSys.lootarget is "self":
        GameSys.lootarget = jt
        return "You can't take things from yourself."
    elif GameSys.lootarget == "None":
        return "You have to loot something first!"
    elif noun in Weapon.weapons:
        noun = Weapon.weapons[noun]
        if noun == GameSys.lootarget.wepslot[0]:
            if GameSys.lootarget.health <= 0:
                jt.inv.append(noun)
                del GameSys.lootarget.wepslot[0]
                return "You picked up a {}".format(noun.obj_name)
        else:
            if noun in GameSys.lootarget.inv:
                GameSys.lootarget.inv.remove(noun)
                jt.inv.append(noun)
                return "You picked up a {}".format(noun.obj_name)
            else:
                return "There is not a {}".format(noun.obj_name)
    elif noun == "Gold" or noun == "gold":
        if GameSys.lootarget.health <= 0:
            looted = GameSys.lootarget.gold
            jt.gold += GameSys.lootarget.gold
            GameSys.lootarget.gold = 0
            return "You picked up {} gold!".format(looted)
    elif isinstance(noun, str):
        if noun in GameSys.lootarget.inv:
            GameSys.lootarget.inv.remove(noun)
            jt.inv.append(noun)
            return "You picked up a {}".format(noun)
    else:
        return "{} doesn't have {}.".format(GameSys.lootarget.obj_name, noun)


def equip(noun):
    if noun in Weapon.weapons:
        noun = Weapon.weapons[noun]
        if isinstance(noun, Weapon):
            oldwep = jt.wepslot[0]
            jt.wepslot.remove(oldwep)
            jt.inv.append(oldwep)
            newwep = noun
            jt.inv.remove(newwep)
            jt.wepslot.append(newwep)
            return "You equipped the {}.".format(newwep.obj_name)
    else:
        return "You don't have a {}.".format(noun)



verb_dict = {"say" : say, "help" : printverbs,
"examine" : examine, "hit" : hit, "clear" : clr,
"block" : block, "loot" : loot, "pickup" : pickup,
"equip" : equip}

#Game:



while True:
    print ""
    jt.block = 0
    
    get_input()
    
    
    if DGame.turn == True:
        gamelist = GameObj.objects.values()
        for g in gamelist:
            if isinstance(g, Enemy) == True:
                g.attack()
                
    DGame.turn = False

    


