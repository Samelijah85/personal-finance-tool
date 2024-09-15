from pymongo import MongoClient

from ..core.config import settings

client = MongoClient(settings.MONGO_REMOTE_URI)

db = client.pfmt

user_collection = db.users
transaction_collection = db.transactions
budget_collection = db.budgets
