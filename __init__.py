import sys
import threading
from api_ipf.helpers import system_start, system_exit

threading.Thread(target=system_start)
sys.exitfunc = system_exit