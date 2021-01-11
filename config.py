"""Bu modül, uygulamayı veritabanına bağlanacak şekilde yapılandırmak içindir."""

from pymongo import MongoClient

# CONNECTION_STRING = "mongodb+srv://hakan:hakanuzal22.@cluster0.ink0b.mongodb.net/dispatchdb?retryWrites=true&w=majority"

DEBUG = True
client = MongoClient('mongodb+srv://hakanuzal:hakanuzal22.@cluster0.ic1qs.mongodb.net/dispatchdb?retryWrites=true&w=majority',maxPoolSize=50, connect=False)

