import os


def get_worker_name(task_request):
	configured_name = os.environ.get('SEASHELL_WORKER_NAME')
	if configured_name:
		return configured_name
	hostname = task_request.hostname
	if hostname:
		return hostname.split('@', 1)[0]
	return 'worker'


def get_node_name():
	return os.environ.get('SEASHELL_NODE_NAME', 'NODE_LOCAL')