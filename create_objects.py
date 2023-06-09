from models import Tribe, Sigil, Card, session


def create_tribe(name):
    tribe = Tribe(
        name=name
    )
    session.add(tribe)
    session.commit()


def create_sigil(name, description):
    sigil = Sigil(
        name=name,
        description=description
    )
    session.add(sigil)
    session.commit()


def create_card(name, cost, cost_type, power, health, traits, grown_id, image, tribe_names=None, sigil_names=None):
    card = Card(
        name=name,
        cost=cost,
        cost_type=cost_type,
        power=power,
        health=health,
        traits=traits,
        grown_id=grown_id,
        image=image
    )

    if tribe_names:
        tribes = session.query(Tribe).filter(Tribe.name.in_(tribe_names)).all()
        card.tribes.extend(tribes)

    if sigil_names:
        sigils = session.query(Sigil).filter(Sigil.name.in_(sigil_names)).all()
        card.sigils.extend(sigils)

    session.add(card)
    session.commit()


'''
tribes = ['Avian', 'Canine', 'Hooved', 'Reptile', 'Insect', 'Squirrel']
for t in tribes:
    create_tribe(t)

create_sigil("Amorphous", "When a card bearing this sigil is drawn, this sigil is replaced with another sigil at random.")
create_sigil("Ant_Spawner", "When a card bearing this sigil is played, an ant is created in your hand.")
create_sigil("Bees_Within", "Once a card bearing this sigil is struck, a Bee is created in your hand. A Bee is defined as: 1 Power, 1 Health, Airborne.")
create_sigil("Bellist", "When a card bearing this sigil is played, a Chime is created on each empty adjacent space. Chimes have 0 Power and 1 Health.")
create_sigil("Bifurcated Strike", "A card bearing this sigil will strike each opposing space to the left and right of the space across from it.")
create_sigil("Bone_King", "When a card bearing this sigil dies, 4 Bones are awarded instead of 1.")
create_sigil("Burrower", "When an empty space would be struck, a card bearing this sigil will move to that space to receive the strike instead.")
create_sigil("Corpse_Eater", "Corpse Eater is a Sigil which causes a card to be automatically played in the place of the first of the player's cards to perish by combat. The effect requires the card bearing this sigil to be in the player's hand.")
create_sigil("Dam_Builder", "When a card bearing this sigil is played, a Dam is created on each empty adjacent space. A Dam is defined as: 0 Power, 2 Health.")
create_sigil("Fecundity", "When a card bearing this sigil is played, a copy of it is created in your hand.")
create_sigil("Fledgling", "A card bearing this sigil will grow into a more powerful form after 1 turn on the board.")
create_sigil("Guardian", "When an opposing creature is placed opposite to an empty space, a card bearing this sigil will move to that empty space.")
create_sigil("Hefty", "Hefty is a Sigil which allows a card to move in the direction inscribed in the sigil at the end of the owner's turn, pushing any cards in the way in the same direction.")
create_sigil("Hoarder", "When a card bearing this sigil is played, you may search your deck for any card and take it into your hand.")
create_sigil("Leader", "Creatures adjacent to a card bearing this sigil gain 1 Power.")
create_sigil("Loose_Tail", "When a card bearing this sigil would be struck, a Tail is created in its place and a card bearing this sigil moves to the right.")
create_sigil("Mighty_Leap", "A card bearing this sigil will block an opposing creature bearing the Airborne sigil.")
create_sigil("Many_Lives", "When a card bearing this sigil is sacrificed, it does not perish.")
create_sigil("Rabbit_Hole", "When a card bearing this sigil is played, a Rabbit is created in your hand.")
create_sigil("Sharp_Quills", "Sharp Quills is a Sigil which makes the bearer deal 1 point of damage to an attacker of said card.")
create_sigil("Sprinter", "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil.")
create_sigil("Trifurcated_Strike", "A card bearing this sigil will strike each opposing space to the left and right of the spaces across from it as well as the space in front of it.")
create_sigil("Trinket_Bearer", "When a card bearing this sigil is played, you will receive a random item as long as you have less than 3 items.")
create_sigil("Unkillable", "Unkillable is a sigil that causes a card to return to the owner's hand after death.")
create_sigil("Waterborne", "Waterborne is a sigil that allows the creature to be submerged for the enemy's turn, causing the opposing creature to skip over it when attacking. The only consistent ways to kill a Waterborne creature are either by doing overkill damage to it before it spawns or by getting it to attack a creature with Sharp Quills.")
create_sigil("Worthy_Sacrifice", "Cards bearing this sigil count as 3 Blood rather than 1 Blood when sacrificed.")
create_sigil("Airborne", "A card bearing this sigil will strike an opponent directly, even if there is a creature opposing it.")
create_sigil("Touch_of_Death", "When a card bearing this sigil damages another creature, that creature perishes.")
create_sigil("Stinky", "The creature opposing a card bearing this sigil loses 1 Power.")
create_sigil("Frozen_Away", "When a card bearing this sigil perishes, the creature inside is released in its place. If a card that doesn't naturally have Frozen Away somehow gains it, an /Opossum is created by default.")
'''

'''
create_card(
    name='Amalgam',
    cost=2,
    cost_type='blood',
    power=3,
    health=3,
    traits='Ant',
    grown_id=None,
    image='images/Amalgam.webp',
    tribe_names=['Avian', 'Canine', 'Hooved', 'Reptile', 'Insect', 'Squirrel'],
    sigil_names=None
)
'''

'''
create_card(
    name='The_Smoke',
    cost=0,
    cost_type=None,
    power=0,
    health=1,
    traits=None,
    grown_id=None,
    image='images/The_Smoke.webp',
    tribe_names=None,
    sigil_names=['Bone_King', ]
)
'''