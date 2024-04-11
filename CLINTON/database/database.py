from motor.motor_asyncio import AsyncIOMotorClient

class Database:

    def __init__(self, uri, database_name):
        self.clinton = AsyncIOMotorClient(uri)
        self.abraham = self.clinton[database_name]
        self.warrior = self.abraham.USERS

    async def get_users(self):
        usersz = self.warrior.find({})
        return usersz

    def new_user(self, uid):
        return dict(uid=uid, thumbnail=None)
  
    async def add_user(self, uid):
        user = self.new_user(uid)
        await self.warrior.insert_one(user)

    async def total_users(self):
        count = await self.warrior.count_documents({})
        return count

    async def delete_user(self, uid):
        await self.warrior.delete_many({'uid': int(uid)})

    async def user_exist(self, uid):
        user = await self.warrior.find_one({'uid': int(uid)})
        return True if user else False

    async def get_thumbnail(self, uid):
        user = await self.warrior.find_one({'uid': int(uid)})
        return user.get('thumbnail', None)

    async def set_thumbnail(self, uid, thumbnail):
        await self.warrior.update_one({'uid': uid}, {'$set': {'thumbnail': thumbnail}})
