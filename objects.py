class Tribe:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Tribe - {self.name}'


class Sigil:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'Sigil - {self.name}'

    def info(self):
        print(f'Sigil - {self.name}: {self.description}')


class CostType:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class Card:
    def __init__(self, name, tribes, sigils, cost, cost_type, power, health, traits):
        self.name = name
        self.tribes = tribes
        self.sigils = sigils
        self.cost = cost * cost_type.name
        self.power = power
        self.health = health
        self.traits = traits
        self.grow = None

    def __repr__(self):
        return f'Card - {self.name}'

    def grow(self, card):
        self.grow = card

    def info(self):
        print(f'Card - {self.name}: {self.cost} {"⚔️" * self.power} {"♥️" * self.health}; {self.tribes if self.tribes else "No Tribe"}; {self.sigils if self.sigils else "No Sigils"}; {self.traits if self.traits else "No Traits"}')


# Creating Tribes
Canine = Tribe('Canine')
Hooved = Tribe('Hooved')
Insect = Tribe('Insect')

# Creating Sigils
Airborne = Sigil('Airborne', 'A card bearing this sigil will '
                             'strike an opponent directly, even if there is a creature opposing it.')
Sprinter = Sigil('Sprinter', "At the end of the owner's turn, "
                             "a card bearing this sigil will move in the direction inscribed in the sigil.")
Fledgling = Sigil('Fledgling', 'A card bearing this sigil will '
                               'grow into a more powerful form after 1 turn on the board.')
TouchOfDeath = Sigil('Touch Of Death', 'When a card bearing this '
                                       'sigil damages another creature, that creature perishes.')

# Creating Cost Types
Sacrifice = CostType('🩸')
Bones = CostType('🦴')
Empty = CostType(' ')


# Creating Cards
Bee = Card('Bee', Insect, Airborne, 0, Empty, 1, 1, None)
LongElk = Card('Long Elk', Hooved, [Sprinter, TouchOfDeath], 4, Bones, 1, 2, 'Kills Survivors')
Rabbit = Card('Rabbit', None, None, 0, Empty, 0, 1, None)
Wolf = Card('Wolf', Canine, None, 2, Sacrifice, 3, 2, None)
