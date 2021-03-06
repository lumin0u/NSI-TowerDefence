import main

# un dictionnaire {classe de la tour: prix} où prix est la liste des coûts des améliorations
# et le premier élément est le prix pour poser la tour
tower_prices = None

# un dictionnaire {classe du mob: récompense}
mobs_rewards = None


def load():
    """
        Chargement des dictionnaires tower_prices et mobs_rewards depuis les ressources
    """
    
    # le json est parfaitement interprétable en python
    prices_json = eval(open("resources/prices.json", mode="r").read())
    
    global tower_prices, mobs_rewards
    
    # les noms simplifiés ("boss", "sniper", ...) sont convertis en leur classe (BossMob, SniperTower, ...)
    tower_prices = {main.TOWERS_NAMES[k]: v for k, v in prices_json["towers"].items()}
    mobs_rewards = {main.MOBS_NAMES[k]: v for k, v in prices_json["mobs_rewards"].items()}


def get_tower_level_prices(tower_type):
    """
        Retourne la liste des prix d'amélioration, **sans** le prix de base de la tour en premier élément
        L'élément d'indice 0 est donc le prix pour passer du niveau 1 au niveau 2, etc
    :param tower_type: classe - le type de la tour
    :return: les prix d'amélioration
    """
    return tower_prices[tower_type][1:]
