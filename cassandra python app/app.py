from cassandra.cluster import Cluster

cluster = Cluster(['cassandra-0.cassandra.default.svc.cluster.local'])
session = cluster.connect()

rows = session.execute('SELECT keyspace_name FROM system_schema.keyspaces')
print("Available keyspaces:")
for row in rows:
    print(f" - {row.keyspace_name}")
