import crossmod
import json

@crossmod.app.template_filter('parse_removal_config')
def parse_removal_config(removal_config):
    return json.loads(removal_config)