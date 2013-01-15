import networkx as nx
import pylab as plt

def node_name(world, model):
	if not world in model['truth']:
		props = '{ }'
	else:
		props = '{%s}' % ' '.join(model['truth'][world])
	return '%s \n%s' %(world, props)

def export_model(model, file_name):
	g = nx.MultiDiGraph()

	for relation in model['relation']:
		g.add_edge(node_name(relation[0], model), node_name(relation[1], model))

	pos = nx.spring_layout(g)

	nx.draw(g, pos, font_size=6, node_shape='s', node_size=600, node_color="#A0CBE2", edge_color='#BB0000', width=1, edge_cmap=plt.cm.Blues)
	plt.savefig(file_name)