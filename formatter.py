def rect(color):
    return '<span style=\"background-color:{}; color:{};\">...</span>'.format(color, color)


def paladin(datas):
    spells = datas['spells']

    spells_up = [rect('green') if spells[key]['ready'] else rect('red') for key in spells if 'u' in key]
    spells_down = [rect('green') if spells[key]['ready'] else rect('red') for key in spells if 'd' in key]

    text = '<div>'
    text += '<div style=\"line-height:1.3;\">{}</div>'.format(' '.join(spells_up))
    text += '<div>{}</div>'.format(' '.join(spells_down))
    text += '<table width="180"><tr>'
    text += '<td>Target: {}</td>'.format(datas['target'])
    text += '<td>Out of range: {}</td>'.format('yes' if datas['oor'] else 'no')
    text += '</tr><tr>'
    text += '<td>Hero: {}%</td>'.format(int(datas['hhp']))
    text += '<td>Enemy: {}%</td>'.format(int(datas['ehp']))
    text += '</tr><tr>'
    text += '<td>Casting: {}</td>'.format('yes' if datas['ecast'] else 'no')
    text += '<td>Holy power: {}</td>'.format(datas['holy'])
    text += '</tr></table>'
    text += '</div>'

    return text
