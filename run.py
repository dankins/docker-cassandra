#!/usr/bin/env python

import os
import yaml
import socket

INTERNAL_IP=socket.gethostbyname(socket.gethostname())
CASSANDRA_CONFIG_FILE = os.path.join('/etc/cassandra', 'cassandra.yaml')


# the following are optional, will default to the second parameter in getenv
LISTEN_ADDRESS=os.getenv('LISTEN_ADDRESS',INTERNAL_IP)
CLUSTER_NAME=os.getenv('CLUSTER_NAME',"Cassandra Cluster")
DATA_DIRECTORY=os.getenv('DATA_DIRECTORY', "/cassandra-data")
COMMIT_DIRECTORY=os.getenv('COMMIT_DIRECTORY',"/cassandra-commitlog")
BROADCAST_ADDRESS=os.getenv('BROADCAST_ADDRESS','172.17.42.1')
# THIS IS LIKELY INCORRECT - but it is the gateway address
RPC_ADDRESS=os.getenv('RPC_ADDRESS',LISTEN_ADDRESS)
STORAGE_PORT=os.getenv('STORAGE_PORT',7000)
NATIVE_TRANSPORT_PORT=os.getenv('NATIVE_TRANSPORT_PORT',9042)
RPC_PORT=os.getenv('RPC_PORT',9160)
SEEDS=os.getenv('SEEDS',LISTEN_ADDRESS).split(',')

# open up the config file and load contents as YAML
with open(CASSANDRA_CONFIG_FILE) as f:
        conf = yaml.load(f)

# update configuration yaml
conf.update({
    'cluster_name': CLUSTER_NAME,
    'data_file_directories': [DATA_DIRECTORY],
    'commitlog_directory': COMMIT_DIRECTORY,
    'listen_address': LISTEN_ADDRESS,
    'broadcast_address': BROADCAST_ADDRESS,
    'rpc_address': RPC_ADDRESS,
    'storage_port': STORAGE_PORT,
    'native_transport_port': NATIVE_TRANSPORT_PORT,
    'rpc_port': RPC_PORT
})

conf['seed_provider'][0]['parameters'][0]['seeds'] = \
    ','.join(SEEDS)

# write out the new config
with open(CASSANDRA_CONFIG_FILE, 'w+') as f:
    yaml.dump(conf, f, default_flow_style=False)

# Start Cassandra in the foreground.
os.execl('/usr/sbin/cassandra', 'cassandra', '-f')

