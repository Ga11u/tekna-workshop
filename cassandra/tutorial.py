from cassandra.cluster import ExecutionProfile, Cluster, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy, RetryPolicy, ConsistencyLevel
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
import datetime


KEYSPACE="store"
IP = 'localhost'
PORT = 9042
USER = "cassandra"
PASSWORD = "cassandra"



profile = ExecutionProfile(
    load_balancing_policy=DCAwareRoundRobinPolicy('datacenter1'),
    retry_policy=RetryPolicy(),
    consistency_level=ConsistencyLevel.ONE,
    serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
    request_timeout=15,
    row_factory=dict_factory
)

authprovider=PlainTextAuthProvider(username=USER, password=PASSWORD)

cluster = Cluster(contact_points=[IP], execution_profiles={EXEC_PROFILE_DEFAULT: profile},auth_provider=authprovider)
session = cluster.connect()



keyspace_query = "CREATE KEYSPACE IF NOT EXISTS "+ KEYSPACE +" WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '2'};"
session.execute(keyspace_query)
session.set_keyspace(KEYSPACE)


compression = {'class':'ZstdCompressor'}
compaction = {'class' : 'SizeTieredCompactionStrategy'}
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
