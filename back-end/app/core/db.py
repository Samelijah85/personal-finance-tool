from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pfmt

user_collection = db.users
transaction_collection = db.transactions
budget_collection = db.budgets
