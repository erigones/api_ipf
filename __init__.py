import threading
from api_ipf.helpers import system_start

threading.Thread(target=system_start).start()