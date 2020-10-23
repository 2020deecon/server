import pymongo
from pymongo import MongoClient

conn=MongoClient('localhost',27017)
db=conn['sunrinton']
    