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
    attack_neutral = False

    def __init__(self):
        self.spell_list = SpellList()

    @staticmethod
    def should_attack(obj):
        target = obj['target']
        ehp = obj['ehp']
        oor = obj['oor']

        if oor:
            return False

        if Bot.attack_neutral:
            return (target == 'neutral' or target == 'enemy') and ehp > 0

        return target == 'enemy'

    def react(self, obj: dict):
        if not self.should_attack(obj):
            return

        return self.process(obj)

    def process(self, obj: dict):
        raise NotImplementedError("Please Implement this method")


class VindictBot(Bot):
    def process(self, obj: dict):
        spells = obj['spells']
        holy = obj['holy']

        s_list = self.spell_list

        s_list.add(spells['u1'], prio=150, cond=holy <= 3, label='Lame de justice')
        s_list.add(spells['u2'], prio=150, cond=holy <= 4, label='Frappe du croisé')
        s_list.add(spells['d1'], prio=300, label='Jugement')
        s_list.add(spells['d2'], prio=200, label='Verdict du templier')
        s_list.add(spells['d3'], prio=200, cond=holy == 0 and not spells['d4']['ready'], label='Trainée de cendres')
        s_list.add(spells['d4'], prio=300, label='Croisade')

        return s_list.prioritize()


class ProtectionBot(Bot):
    def process(self, obj: dict):
        spells = obj['spells']

        s_list = self.spell_list
        # Stuns
        # self.spell_list.add(spells['u1'], prio=100)  # Marteau de la justice (stun 6 secondes)
        # self.launch_asap(spells['d6'], cond=obj['hhp'] < 60)  # Choc martial (stun 8 enemis 2s)

        # si la vie est en dessous de 20%
        s_list.add(spells['d12'], cond=obj['hhp'] < 20, prio=1502, label='Imposition des mains (heal all pvs)')
        s_list.add(spells['u3'], cond=obj['hhp'] < 20 and not spells['d12']['ready'], prio=1500, label='Bouclier divin (invulnérable)')
        s_list.add(spells['u4'], cond=obj['hhp'] < 20 and not spells['d12']['ready'] and not spells['u3']['ready'], prio=1500, label='Bénédiction de protection (invulnérable, mais perds aggro)')

        s_list.add(spells['u2'], cond=obj['hhp'] < 30, prio=1003, label='Gardien des anciens rois (shield 50%, 8s)')
        s_list.add(spells['d11'], cond=obj['hhp'] < 40, prio=1002, label='Lumière du protecteur (heal 30% pvs manquants)')
        s_list.add(spells['d3'], cond=obj['hhp'] < 60, prio=1001, label='Bouclier du vertueux (coup de bouclier, 3 charges)')
        s_list.add(spells['d9'], cond=obj['hhp'] < 80, prio=1000, label='Ardent défenseur (degats -20%, 8s)')

        s_list.add(spells['d8'], cond=obj['ecast'], prio=500, label='Réprimandes (interrupt)')

        s_list.add(spells['d7'], prio=150, label='Main de rétribution')

        s_list.add(spells['d5'], prio=110, label='Consécration')
        s_list.add(spells['d1'], prio=100, label='Bouclier divin du vengeur')
        s_list.add(spells['d2'], prio=100, label='Marteau béni')
        s_list.add(spells['d3'], prio=100, label='Bouclier du vertueux (coup de bouclier, 3 charges)')
        s_list.add(spells['d4'], prio=100, label='Jugement (lancer de marteau)')

        return s_list.prioritize()
