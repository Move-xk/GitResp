from pygal.maps.world import World

wm = World()
wm.title = 'North, Center, and South American'
wm.add('North America', ['ca', 'mx', 'us'])
wm.add('Central America', ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'gf', 'gy', 'pe', 'py', 'sr', 'uy', 've'])
wm.render_to_file('americas.svg')
wm = World()
wm.title = 'North, Center, and South American'
wm.add('North America', ['ca', 'mx', 'us'])
wm.add('Central America', ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'gf', 'gy', 'pe', 'py', 'sr', 'uy', 've'])

wm.render_to_file('americas.svg')