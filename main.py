from defines import *
from colors import bcolors as css

# --- definisci sentimenti di base ---
pain=Urge('hp', _range=range(-10,0), slags=3)
sadness=Urge('&h', _range=range(-5,0))
angry=Urge('&s',_range=range(0,5))
basefeels=[sadness, angry] # list all of them
# --- main ---
me=Human()#train_on_spawn=True, show_logs=True, urges=basefeels)
#me.flux.add(pain)
#me.flux.process()
me.flux.add(pain)
me.flux.process()
me.entire_log()
#me.flux.process()
me.flux.process()
#rissa=Event(me, sadness, angry)
#rissa.activate()
me.entire_log()
