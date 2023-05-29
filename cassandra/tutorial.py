from cassandra.cluster import ExecutionProfile, Cluster, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy, RetryPolicy, ConsistencyLevel
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
import datetime


KEYSPACE="store" # The keyspace we are going to use (similar to a database name)
IP = 'localhost' # The address of Cassandra
PORT = 9042 # The port for the connection
USER = "cassandra" 
PASSWORD = "cassandra"


# The execution profile can be specified for each connection. Different applications can use different execution profiles.
profile = ExecutionProfile(
    load_balancing_policy=DCAwareRoundRobinPolicy('datacenter1'), # The load balancing policy for query, in this case, RoundRobin in one datacenter. This can include more datacenters and other policies. 
    retry_policy=RetryPolicy(), # Default retry policy for requests
    consistency_level=ConsistencyLevel.ONE, # The consistency level of our queries. In this case is ONE because there is only one instance, otherwise, it could be QUORUM or LOCAL_QUORUM among others
    serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL, # The consistency of the transactions, in this case, to achieve consistency within the datacenter
    request_timeout=15,
    row_factory=dict_factory # How Cassandra serialises the response, in this case as a dictionary. This is why we will see dictionaries as response when we execute the code
)

authprovider=PlainTextAuthProvider(username=USER, password=PASSWORD) # Plain text authentification, other protocols can by used like SSL.

cluster = Cluster(contact_points=[IP], execution_profiles={EXEC_PROFILE_DEFAULT: profile},auth_provider=authprovider) # The contact points where the connections must be sent to discover the cluster. More than one address can be provided.
session = cluster.connect()



keyspace_query = "CREATE KEYSPACE IF NOT EXISTS "+ KEYSPACE +" WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '2'};" #  We set replication factor 2 within datacenter1. Each datacenter can have a different replication factor.
session.execute(keyspace_query)
session.set_keyspace(KEYSPACE)


compression = {'class':'ZstdCompressor'} # The comporesion algorithm to use
compaction = {'class' : 'SizeTieredCompactionStrategy'} # The compaction strategy to use
table = session.prepare(""" 
    CREATE TABLE IF NOT EXISTS shopping_cart (
        userid text,
        item_count int,
        last_update timestamp,
        PRIMARY KEY (userid))
    WITH COMPRESSION = {'class':'ZstdCompressor'}
    AND COMPACTION  = {'class':'SizeTieredCompactionStrategy'};
""")
session.execute(table)

session.execute("CREATE INDEX IF NOT EXISTS index_last_update ON shopping_cart (last_update);")

insert_statement = session.prepare("INSERT INTO shopping_cart (userid, item_count, last_update) VALUES (?,?,?);")

session.execute(insert_statement,["User1",20,datetime.datetime.now()])
session.execute(insert_statement,["User2",200,datetime.datetime.now()])
session.execute(insert_statement,["User3",30,datetime.datetime.now()])
session.execute(insert_statement,["User4",15,datetime.datetime.now()])

print("Get everything from the collection")
res = session.execute("SELECT * FROM shopping_cart ;")
print(list(res))

print("Get the average")
res = session.execute("SELECT AVG(item_count) AS average_items FROM shopping_cart;")
print(list(res))
      

session.shutdown()
