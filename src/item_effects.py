import random

def roll_dice(sides: int) -> int:
    """Roll a dice with the given number of sides."""
    return random.randint(1, sides)

def apply_item_effect(item, target, team=None, enemies=None, coins=0):
    effect = item.get("on use", "")

    # Gros Michel Banana
    if effect == "1 in 12 chance to unlock Legendary banana (It not doing anything now)":
        if random.randint(1, 12) == 1:
            return f"{target.Name} unlocked Legendary banana!"
        else:
            return f"{target.Name} did not unlock Legendary banana."

    # Healing Potion
    elif effect == "Recover 1d8 HP":
        heal_amount = roll_dice(8)
        target.HP = min(target.HP + heal_amount, 100)
        return f"{target.Name} healed for {heal_amount} HP!"

    # Jimbo
    elif effect == "Next hit, add 4 damage":
        target.STR += 4
        return f"{target.Name} added 4 damage to the next hit!"

    # Chocolate Cornet
    elif effect == "Increase ACC by 1":
        target.ACC += 1
        return f"{target.Name} increased ACC by 1!"
    
    # Apple Juice
    elif effect == "Recover 2d8 HP":
        heal_amount = roll_dice(8) + roll_dice(8)
        target.HP = min(target.HP + heal_amount, 100)
        return f"{target.Name} healed for {heal_amount} HP!"

    # Coconut
    elif effect == "Recover 1d8 HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = roll_dice(8)
        for member in team:
            member.HP = min(member.HP + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"
    
    # Watermelon
    elif effect == "Recover 2d6 HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = roll_dice(6) + roll_dice(6)
        for member in team:
            member.HP = min(member.HP + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"

    # Ice Cream
    elif effect == "Recover 20 Mana":
        target.MP = target.MP + 20
        return f"{target.Name} restored 20 Mana!"
    
    # A Broken Toaster
    elif effect == "Deal 1d12 damage to a random enemy":
        if not target:
            return "No target enemy provided for the effect!"
        
        damage = roll_dice(12)
        target.HP = target.HP - damage
        return f"{target.Name} weakened for {damage} HP!"
    
    # Hamburger
    elif effect == "Fully recover HP":
        target.HP = 100
        return f"{target.Name} fully recovered HP!"
    
    # Cupcake
    elif effect == "Recover 50 Mana":
        target.MP = target.MP + 50
        return f"{target.Name} restored 50 Mana!"
    
    # Midas Bomb
    elif effect == "Deals 3d6 damage to an enemy. If it died, gain 2d4*10 coins":
        damage = roll_dice(6) + roll_dice(6) + roll_dice(6)
        target.HP = target.HP - damage
        if target.HP <= 0:
            coins += (roll_dice(4) + roll_dice(4)) * 10
            return f"{target.Name} died! You gain {coins} coins!"

    # Emerald Splash
    elif effect == "Deals 4d12 damage to enemies. Has 1 in 6 chance to deal on yourself":
        damage = roll_dice(12) + roll_dice(12) + roll_dice(12) + roll_dice(12)
        if random.randint(1, 6) == 1:
            target.HP = target.HP - damage
            return f"{target.Name} damaged themselves for {damage} HP!"
        else:
            if not enemies:
                return "No enemies provided for the effect!"

            for enemy in enemies:
                enemy.HP = enemy.HP - damage
            return f"{target.Name} damaged enemies for {damage} HP!"

    # John's Bible
    elif effect == "Next incoming hit deals 0 damage":
        return f"{target.Name} is immune to the next hit! (not really)"

    # Endless Eight
    elif effect == "Deals 8d8 damage to an enemy. Has 1 in 8 chance to deal additional 8d8.":
        damage = roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8)
        if random.randint(1, 8) == 1:
            damage += roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8)
            target.HP = target.HP - damage
            return f"{target.Name} damaged for {damage} HP! with 1 in 8 chance"
        else:
            target.HP = target.HP - damage
            return f"{target.Name} damaged for {damage} HP!"
        
    # Pizza
    elif effect == "Fully recover HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = 100
        for member in team:
            member.HP = min(member.HP + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"

    else:
        return f"The item '{item.Name}' has no effect!"
