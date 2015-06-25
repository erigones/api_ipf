from eszone_ipf.settings import BASE_DIR

# Directory for storing configuration files.
CONF_DIR = ''.join([BASE_DIR, '/conf/'])

# Directory for storing logs.
LOG_DIR = ''.join([BASE_DIR, '/log/'])

# Directory that contains backup configuration files.
BCK_DIR = ''.join([BASE_DIR, '/api_ipf/bck/'])

# Warning in the ippool.conf configuration file
# for a recognition of a user defined ippool and IP blacklist.
CONF_WARNING = '#CONFIGURATION UNDER THIS LINE WILL BE DELETED AT UPDATE'
