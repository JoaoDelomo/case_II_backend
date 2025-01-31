from pymongo import MongoClient

MONGO_URI = "mongodb+srv://admin:admin@delomo.zxqnf.mongodb.net/?authSource=admin&retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["case_II"]
customers_collection = db["customers"]
collaborators_collection = db["collaborators"]
feedbacks_collection = db["feedback"]
funcionarios_collection = db["funcionarios"]
plans_collection = db["planos"]
ps_collection = db["processo_seletivo"]

