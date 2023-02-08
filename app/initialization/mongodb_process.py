from utils.mongodb import MongoManager
from configs.sysconf  import MONGODB_CONNECT_URL, MONGODB_DB


mongo_cli = MongoManager(MONGODB_CONNECT_URL, MONGODB_DB)