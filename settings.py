from eszone_ipf.settings import BASE_DIR

ALLOWED_COMMANDS = ['ipf', 'ipfstat', 'ipnat', 'ippool', 'ipmon', 'svcadm',
                    'scvs']
CONF_DIR = ''.join([BASE_DIR, '/conf/']) #/etc/ipf/
LOG_DIR = ''.join([BASE_DIR, '/log/']) #/var/log/
CONF_WARNING = '#CONFIGURATION UNDER THIS LINE WILL BE DELETED AT UPDATE'