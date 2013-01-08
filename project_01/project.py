models = {}
current_model = None

availableCommands = [
    'CREATE MODEL', 'REMOVE MODEL', 'LIST MODELS',
    'SHOW MODEL', 'SHOW ALL MODELS', 'EDIT MODEL',
    'SHOW',
    'ADD RELATIONS', 'REMOVE RELATIONS', 'CLEAR RELATIONS',
    'ADD WORLDS', 'REMOVE WORLDS', 'RENAME WORLD',
    'CLEAR',
    'ADD TRUE', 'REMOVE TRUE', 'REMOVE PROPOSITIONS',
    'RENAME PROPOSITIONS', 'CLEAR TRUTH'];

messages = {
    'unopen_model': 'No model is currently open for editing. Use the EDIT command first.'
}
def display_model(model):
    # Given a model, print it the way it is described in the assignment
    if not model in models:
        print 'Model %s not found.' % model
    else:
        print 'Model %s :' % model
        model = models[model]
        print '  Worlds = {%s}' % ', '.join(model.get('worlds'))
        print '  Relation = {%s}' % ', '.join(['(%s, %s)' % (relation[0], relation[1]) for relation in model.get('relation')])
        print '\n'

def new_model(name=None):
    # Return a clean model
    model = {'worlds': [], 'relation': [], 'truth': {}}
    if name:
        model['name'] = name

    return model

def execute_cmd(command):
    global current_model
    # Execute a given command in a specific context

    for cmd in availableCommands:
        # Commands for manipulating the model dict
        if command.startswith(cmd):
            if cmd == 'CREATE MODEL':
                model = command[len(cmd)+1:]
                if model.endswith(' FORCE'):
                    model = model[:len(model)-6]
                    if model in models:
                        print 'Existing model %s overwritten.' % model
                    models[model] = new_model()

                else:
                    if model in models:
                        print 'Model %s already exists. Use the EDIT command to open this' \
                            'model for editing.' % model
                    else:
                        models[model] = new_model()
            elif cmd == 'REMOVE MODEL':
                model = command[len(cmd)+1:]
                if not model in models:
                    print 'Model %s not found.' % model
                else:
                    del models[model]
            elif cmd == 'LIST MODELS':
                print 'Models : %s' % (' '.join(models.keys()))
            elif cmd == 'SHOW MODEL':
                model = command[len(cmd)+1:]
                display_model(model)
            elif cmd == 'SHOW ALL MODELS':
                for model in models.keys():
                    display_model(model)
            elif cmd == 'EDIT MODEL':
                model = command[len(cmd)+1:]
                if not model in models:
                    print 'Model %s not found.' % model
                else:
                    current_model = models[model]
                    current_model['name'] = model
            elif cmd == 'SHOW':
                if current_model:
                    display_model(current_model['name'])
                else:
                    print messages['unopen_model']

            # Commands for creating and editing a world
            elif cmd == 'ADD WORLDS':
                if not current_model: print messages['unopen_model']
                worlds = command[len(cmd)+1:]
                for world in worlds.split(' '):
                    if world in current_model['worlds']:
                        print 'World %s already exists.' % world
                    else:
                        current_model['worlds'].append(world)
            elif cmd == 'REMOVE WORLDS':
                worlds = command[len(cmd)+1:]
                for world in worlds.split(' '):
                    if not world in current_model['worlds']:
                        print 'World %s not found.' % world
                    else:
                        # Remove the world
                        current_model['worlds'].remove(world)
                        # Remove all accessibility relation pairs that contain the world
                        for relation in current_model['relation']:
                            if world in relation:
                                relation.remove(world)
            elif cmd == 'RENAME WORLD':
                world = command[len(cmd)+1:]
                pos = world.find('TO')
                old_name = world[:pos - 1]
                new_name = world[pos+3:]

                if not old_name in current_model['worlds']:
                    print 'World %s not found.' % old_name
                else:
                    idx = current_model['worlds'].index(old_name)
                    current_model['worlds'][idx] = new_name

                    if new_name in current_model['truth'] and old_name in current_model['truth']:
                        current_model['truth'][new_name] = list(set(current_model['truth'][new_name]) | set (current_model['truth'][old_name]))
                        del current_model['truth'][old_name]

                    for relation in current_model['relation']:
                        if relation[0] == old_name:
                            relation[0] = new_name
                        if relation[1] == old_name:
                            relation[1] == new_name


            elif cmd == 'CLEAR':
                current_model = new_model(name=current_model['name'])
                models[current_model['name']] = current_model

            # Commands for creating and editin a relation
            elif cmd == 'ADD RELATIONS':
                relations = command[len(cmd)+1:]
                worlds = relations.split(' ')
                for idx in range(0, len(worlds), 2):
                    pair = [worlds[idx], worlds[idx+1]]

                    if pair in current_model['relation']:
                        'Pair (%s, %s) already exists.' % (pair[0], pair[1])
                    elif not worlds[idx] in current_model['worlds']:
                        print 'World %s not found.' % worlds[idx]
                    elif not worlds[idx+1] in current_model['worlds']:
                        print 'World %s not found.' % worlds[idx+1]
                    else:
                        current_model['relation'].append(pair)

            elif cmd == 'REMOVE RELATIONS':
                relations = command[len(cmd)+1:]
                worlds = relations.split(' ')
                for idx in range(0, len(worlds), 2):
                    pair = [worlds[idx], worlds[idx+1]]

                    if not pair in current_model['relation']:
                        'Pair (%s, %s) not found.' % (pair[0], pair[1])
                        pair
                    else:
                        current_model['relation'].remove(pair)

            elif cmd == 'CLEAR RELATIONS':
                current_model['relation'] = []

            elif cmd == 'ADD TRUE':
                truth = command[len(cmd)+1:]
                props = truth[:len(truth.find('AT'))-1].split(' ')
                worlds = truth[len(truth.find('AT'))+3:].split(' ')

                for world in worlds:
                    for prop in props:
                        if not world in current_model['worlds']:
                            print 'World %s not found.' % world
                        elif world in current_model['truth'] and prop in current_model['truth'].get(world, []):
                            print 'Proposition %s already true at world %s' % (prop, world)
                        else:
                            if not world in current_model['truth']:
                                current_model['truth'][world] = [prop]
                            else:
                                current_model['truth'][world].append(prop)

            elif cmd == 'REMOVE TRUE':
                truth = command[len(cmd)+1:]
                props = truth[:len(truth.find('AT'))-1].split(' ')
                worlds = truth[len(truth.find('AT'))+3:].split(' ')

                for world in worlds:
                    for prop in props:
                        if not world in current_model['worlds']:
                            print 'World %s not found.' % world
                        elif world in current_model['truth'] and not prop in current_model['truth'].get(world, []):
                            print 'Proposition %s was not true at world %s' % (prop, world)
                        else:
                            current_model['truth'][world].remove(prop)
            elif cmd == 'REMOVE PROPOSITIONS':
                props = command[len(cmd)+1:].split(' ')

                for prop in props:
                    for world, world_props in current_model['truth'].items():
                        if prop in world_props:
                            world_props.remove(prop)
            elif cmd == 'RENAME PROPOSITION':
                prop = command[len(cmd)+1:]
                pos = prop.find('TO')
                old_name = prop[:pos - 1]
                new_name = prop[pos+3:]

                for world, props in current_model['truth'].items():
                    if old_name in props:
                        props[props.index(old_name)] = new_name
            elif cmd == 'CLEAR TRUTH':
                current_model['truth'] = {}
            break

def tests():
    # Insanity tests
    execute_cmd('CREATE MODEL m1')
    execute_cmd('CREATE MODEL m2')
    execute_cmd('REMOVE MODEL m3')
    execute_cmd('CREATE MODEL m3 FORCE')
    execute_cmd('CREATE MODEL m1 FORCE')
    execute_cmd('LIST MODELS')
    execute_cmd('SHOW MODEL m1')
    execute_cmd('SHOW ALL MODELS')
    execute_cmd('EDIT MODEL m4')
    execute_cmd('EDIT MODEL m1')
    execute_cmd('ADD WORLDS w1 w2 w3')
    execute_cmd('REMOVE WORLDS w2')
    #execute_cmd('CLEAR')

    execute_cmd('ADD RELATIONS w1 w2 w2 w3 w1 w3')
    execute_cmd('REMOVE RELATIONS w1 w3')
    #execute_cmd('CLEAR RELATIONS')
    execute_cmd('SHOW')
    #print models

if __name__ == '__main__':
    tests()