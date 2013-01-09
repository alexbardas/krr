models = {}
current_model = None

availableCommands = [
    'EXECUTE COMMANDS FROM',

    'CREATE MODEL', 'REMOVE MODEL', 'LIST MODELS',
    'SHOW MODEL', 'SHOW ALL MODELS', 'EDIT MODEL',
    'SHOW',

    'ADD RELATIONS', 'REMOVE RELATIONS', 'CLEAR RELATIONS',

    'ADD TRUE', 'REMOVE TRUE', 'REMOVE PROPOSITIONS',
    'RENAME PROPOSITION', 'CLEAR TRUTH',

    'ADD WORLDS', 'REMOVE WORLDS', 'RENAME WORLD',
    'CLEAR',

    'LOAD MODELS FROM', 'SAVE MODELS TO'];

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
        for world, prop in model['truth'].items():
            print 'True(%s) = {%s}' % (world, ', '.join(prop))
        print ''

def save_models_to_file(models, fout):
    # Print all models to fout
    print >> fout, len(models.keys())
    for model_name, model in models.items():
        print >> fout, 'MODEL %s' % model_name
        print >> fout, 'WORLDS %s' % ' '.join(model.get('worlds'))
        print >> fout, 'RELATIONS %s' % ' '.join(['(%s, %s)' % (relation[0], relation[1]) for relation in model.get('relation')])
        for world, props in model.get('truth').items():
            print >> fout, 'True %s : %s' % (world, ' '.join(props))

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

            if cmd == 'EXECUTE COMMANDS FROM':
                file_name = command[len(cmd)+1:]
                try:
                    f = open(file_name, 'r')
                    lines = f.readlines()
                    lines = [line.replace('\n', '') for line in lines]
                    for line in lines:
                        execute_cmd(line)
                except IOError:
                    print 'File %s could not be found.' % file_name

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
                            ' model for editing.' % model
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
                if not current_model: print messages['unopen_model']; break
                display_model(current_model['name'])

            # Commands for creating and editing a world
            elif cmd == 'ADD WORLDS':
                if not current_model: print messages['unopen_model']; break
                worlds = command[len(cmd)+1:]
                for world in worlds.split(' '):
                    if world in current_model['worlds']:
                        print 'World %s already exists.' % world
                    else:
                        current_model['worlds'].append(world)
            elif cmd == 'REMOVE WORLDS':
                if not current_model: print messages['unopen_model']; break
                worlds = command[len(cmd)+1:]
                for world in worlds.split(' '):
                    if not world in current_model['worlds']:
                        print 'World %s not found.' % world
                    else:
                        # Remove the world
                        current_model['worlds'].remove(world)
                        if world in current_model['truth']:
                            del current_model['truth'][world]
                        # Remove all accessibility relation pairs that contain the world
                        new_relation = []
                        for relation in current_model['relation']:
                            if not world in relation:
                                new_relation.append(relation)
                        current_model['relation'] = new_relation

            elif cmd == 'RENAME WORLD':
                if not current_model: print messages['unopen_model']; break
                world = command[len(cmd)+1:]
                pos = world.find('TO')
                old_name = world[:pos - 1]
                new_name = world[pos+3:]

                if not old_name in current_model['worlds']:
                    print 'World %s not found.' % old_name
                    break

                if new_name in current_model['worlds']:
                    current_model['worlds'].remove(old_name)
                else:
                    idx = current_model['worlds'].index(old_name)
                    current_model['worlds'][idx] = new_name

                if old_name in current_model['truth']:
                    if not new_name in current_model['truth']:
                        current_model['truth'][new_name] = current_model['truth'][old_name]
                    else:
                        current_model['truth'][new_name] = list(set(current_model['truth'][new_name]) | set (current_model['truth'][old_name]))
                    del current_model['truth'][old_name]

                for relation in current_model['relation']:
                    if relation[0] == old_name:
                        relation[0] = new_name
                    if relation[1] == old_name:
                        relation[1] = new_name

                # remove duplicates from relation list
                new_list = []
                for relation in current_model['relation']:
                    if relation not in new_list:
                        new_list.append(relation)
                current_model['relation'] = new_list

            elif cmd == 'CLEAR':
                if not current_model: print messages['unopen_model']; break
                current_model = new_model(name=current_model['name'])
                models[current_model['name']] = current_model

            # Commands for creating and editin a relation
            elif cmd == 'ADD RELATIONS':
                if not current_model: print messages['unopen_model']; break
                relations = command[len(cmd)+1:]
                worlds = relations.split(' ')
                for idx in range(0, len(worlds), 2):
                    pair = [worlds[idx], worlds[idx+1]]

                    if pair in current_model['relation']:
                        print 'Pair (%s, %s) already exists.' % (pair[0], pair[1])
                        continue
                    else:
                        found = True
                        if not worlds[idx] in current_model['worlds']:
                            print 'World %s not found.' % worlds[idx]
                            found = False
                        if not worlds[idx+1] in current_model['worlds']:
                            print 'World %s not found.' % worlds[idx+1]
                            found = False
                        if not found: continue
                    current_model['relation'].append(pair)

            elif cmd == 'REMOVE RELATIONS':
                if not current_model: print messages['unopen_model']; break
                relations = command[len(cmd)+1:]
                worlds = relations.split(' ')
                for idx in range(0, len(worlds), 2):
                    pair = [worlds[idx], worlds[idx+1]]
                    if not pair in current_model['relation']:
                        print 'Pair (%s, %s) not found.' % (pair[0], pair[1])
                    else:
                        current_model['relation'].remove(pair)

            elif cmd == 'CLEAR RELATIONS':
                if not current_model: print messages['unopen_model']; break
                current_model['relation'] = []

            elif cmd == 'ADD TRUE':
                if not current_model: print messages['unopen_model']; break
                truth = command[len(cmd)+1:]
                props = truth[:truth.find('AT')-1].split(' ')
                worlds = truth[truth.find('AT')+3:].split(' ')

                for world in worlds:
                    if not world in current_model['worlds']:
                        print 'World %s not found.' % world
                        continue
                    for prop in props:
                        if world in current_model['truth'] and prop in current_model['truth'].get(world, []):
                            print 'Proposition %s already true at world %s' % (prop, world)
                        else:
                            if not world in current_model['truth']:
                                current_model['truth'][world] = [prop]
                            else:
                                current_model['truth'][world].append(prop)

            elif cmd == 'REMOVE TRUE':
                if not current_model: print messages['unopen_model']; break
                truth = command[len(cmd)+1:]
                props = truth[:truth.find('AT')-1].split(' ')
                worlds = truth[truth.find('AT')+3:].split(' ')

                for world in worlds:
                    for prop in props:
                        if not world in current_model['worlds']:
                            print 'World %s not found.' % world
                        elif world in current_model['truth'] and not prop in current_model['truth'].get(world, []):
                            print 'Proposition %s was not true at world %s.' % (prop, world)
                        else:
                            current_model['truth'][world].remove(prop)
            elif cmd == 'REMOVE PROPOSITIONS':
                if not current_model: print messages['unopen_model']; break
                props = command[len(cmd)+1:].split(' ')

                for prop in props:
                    for world, world_props in current_model['truth'].items():
                        if prop in world_props:
                            world_props.remove(prop)
            elif cmd == 'RENAME PROPOSITION':
                if not current_model: print messages['unopen_model']; break
                prop = command[len(cmd)+1:]
                pos = prop.find('TO')
                old_name = prop[:pos - 1]
                new_name = prop[pos+3:]

                for world, props in current_model['truth'].items():
                    if old_name in props:
                        props[props.index(old_name)] = new_name
            elif cmd == 'CLEAR TRUTH':
                if not current_model: print messages['unopen_model']; break
                current_model['truth'] = {}

            elif cmd == 'LOAD MODELS FROM':
                file_name = command[len(cmd)+1:]
                try:
                    f = open(file_name, 'r')
                    lines = f.readlines()
                    lines = [line.replace('\n', '') for line in lines]
                    f.close()
                    current_model_bk = current_model
                    no_of_models = int(lines.pop(0))

                    model_name = lines.pop(0)[len('MODEL '):]
                    for idx in range(0, no_of_models):
                        execute_cmd('CREATE MODEL %s FORCE' % model_name)
                        execute_cmd('EDIT MODEL %s' % model_name)

                        worlds = lines.pop(0)[len('WORLDS '):]
                        execute_cmd('ADD WORLDS %s' % worlds)

                        relations = lines.pop(0)[len('RELATIONS '):]
                        relations = relations.replace('(', '').replace(')', '').replace(',', '')
                        execute_cmd('ADD RELATIONS %s' % relations)

                        # Go through all truth assignments until a new model is found
                        found = False
                        while not found and len(lines) > 0:
                            truth = lines.pop(0)
                            if truth.startswith('MODEL'):
                                found = True
                                model_name = truth[len('MODEL '):]
                            else:
                                truth = truth[len('TRUE '):]
                                truth = truth.split(' ')
                                truth.remove(':')
                                execute_cmd('ADD TRUE %s AT %s' % (' '.join(truth[1:]), truth[0]))

                    current_model = current_model_bk
                except IOError:
                    print 'File %s not found.' % file_name

            elif cmd == 'SAVE MODELS TO':
                file_name = command[len(cmd)+1:]
                try:
                    f = open(file_name, 'w')
                    save_models_to_file(models, f)
                except Exception, e:
                    pass
            break

def tests():
    # Insanity tests
    # execute_cmd('CREATE MODEL m1')
    # execute_cmd('CREATE MODEL m2')
    # execute_cmd('REMOVE MODEL m3')
    # execute_cmd('CREATE MODEL m3 FORCE')
    # execute_cmd('CREATE MODEL m1 FORCE')
    # execute_cmd('LIST MODELS')
    # execute_cmd('SHOW MODEL m1')
    # execute_cmd('SHOW ALL MODELS')
    # execute_cmd('EDIT MODEL m4')
    # execute_cmd('EDIT MODEL m1')
    # execute_cmd('ADD WORLDS w1 w2 w3')
    # execute_cmd('REMOVE WORLDS w2')
    # #execute_cmd('CLEAR')

    # execute_cmd('ADD RELATIONS w1 w2 w2 w3 w1 w3')
    # execute_cmd('REMOVE RELATIONS w1 w3')
    # #execute_cmd('CLEAR RELATIONS')
    # execute_cmd('SHOW')

    # execute_cmd('LOAD MODELS FROM baietel.txt')
    execute_cmd('LOAD MODELS FROM input.txt')
    execute_cmd('SAVE MODELS TO baietel.txt')
    #print models

def main():
    command = ''
    while command != 'EXIT':
        command = raw_input('$ ')
        print command
        execute_cmd(command)

if __name__ == '__main__':
    #tests()
    main()