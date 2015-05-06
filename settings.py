from eszone_ipf.settings import BASE_DIR

ALLOWED_COMMANDS = 'ipf, ipfstat, ipnat, ippool, ipmon'
CONF_DIR = ''.join([BASE_DIR, '/conf/']) #/etc/ipf/
LOG_DIR = ''.join([BASE_DIR, '/log/']) #/var/log/