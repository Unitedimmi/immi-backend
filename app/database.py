from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://ayush2211207:koLO50CvMTHHJ1Wg@cluster0.d7fkhvy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client.immigration
