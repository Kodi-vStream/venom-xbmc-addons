from lib.directories import plugin_dir, tests_dir
LOGDEBUG = ''

def translatePath(pathSpecial):
    if not isinstance(pathSpecial, str):
        return str(pathSpecial)
    if pathSpecial.endswith('sites.json'):
        return str(plugin_dir.joinpath('resources','sites.json'))
    else:
        return str(tests_dir.joinpath('tmp', 'vstream.db'))
    
def executeJSONRPC(req):
    return '{"result":{"label":""}}'
