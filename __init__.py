from wn import WordNet
from wn.constants import wordnet_30_dir
import time

print("""                                                                                
 __  .__   __.  _______  _______ .______      .__   __.   ______   
|  | |  \ |  | |   ____||   ____||   _  \     |  \ |  |  /  __  \  
|  | |   \|  | |  |__   |  |__   |  |_)  |    |   \|  | |  |  |  | 
|  | |  . `  | |   __|  |   __|  |      /     |  . `  | |  |  |  | 
|  | |  |\   | |  |     |  |____ |  |\  \----.|  |\   | |  `--'  | 
|__| |__| \__| |__|     |_______|| _| `._____||__| \__|  \______/                                                          
""")

wn_tick = time.perf_counter()
__builtins__['wn'] = WordNet(wordnet_30_dir)
wn_tock = time.perf_counter()
print(f"Loaded WordNet 3.0 model in {wn_tock - wn_tick:0.4f} seconds")