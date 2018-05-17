class SpellList:
    def __init__(self):
        self.p_spells = []

    def add(self, spell, cond=True, prio=0, label="?"):
        if spell['ready'] and cond:
            self.p_spells.append({
                'spell': spell,
                'prio': prio,
                'label': label
            })

    def prioritize(self):
        best_spell = None
        for p_spell in self.p_spells:
            if best_spell is None or p_spell['prio'] >= best_spell['prio']:
                best_spell = p_spell
        self.p_spells = []

        return best_spell


class Bot:
    def __init__(self):
        self.spell_list = SpellList()

    @staticmethod
    def should_attack(obj):
        return obj['target'] == 'enemy'

    def process(self):
        raise NotImplementedError("Please Implement method process.")


