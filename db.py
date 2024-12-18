from os import environ
from pymongo import MongoClient

# env varible
MONGO_URL=environ.get('MONGODB_URL')

# handle mongo connection
client = MongoClient(
	MONGO_URL,
    tls=True,
	tlsAllowInvalidCertificates=True
)

db = client.contactsApp 