from bot.text import rect


def describe(datas):
    spells = datas['spells']

    spells_up = [rect('green') if spells[key]['ready'] else rect('red') for key in spells if 'u' in key]
    spells_down = [rect('green') if spells[key]['ready'] else rect('red') for key in spells if 'd' in key]

    text = '<div>'
    text += '<div style=\"line-height:1.3;\">{}</div>'.format(' '.join(spells_up))
    text += '<div>{}</div>'.format(' '.join(spells_down))
    text += '<table width="180"><tr>'
    text += '<td>Target: {}</td>'.format(datas['target'])
    text += '</tr></table>'
    text += '</div>'

    return text
