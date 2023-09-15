from prisma import Prisma


class FinancialSystem:
    def __init__(self):
        self.individuals = {}

    # Function to add a transaction.
    async def add_transaction(self, from_person, to_person, amount):
        if amount < 0:
            raise Exception("Invalid Transaction")
        db = Prisma()
        await db.connect()

        from_user = await db.user.find_unique(where={'username': from_person})
        to_user = await db.user.find_unique(where={'username': to_person})


        if not from_user :
            await db.user.create(data={'username': from_person, 'balance': 0-amount})
        else :
            await db.user.update(where={'username': from_person},data={'balance': from_user.balance - amount})

        if not to_user :
            await db.user.create(data={'username': to_person, 'balance': amount})
        else :
            await db.user.update(where={'username': to_person},data={'balance': to_user.balance + amount})

        await db.usertransaction.create(data={'from_user': from_person, 'to_user': to_person, 'amount': amount})

        await db.disconnect()

    # Function to query the total debt of an individual.
    async def query_debt(self, person):

        db = Prisma()
        await db.connect()

        user = await db.user.find_unique(where={'username': person})
        
        if not user:
            raise Exception("User not found")
        
        money_received = await db.usertransaction.find_many(where={'from_user': person})
        money_sent = await db.usertransaction.find_many(where={'to_user': person})

        await db.disconnect()

        total_amount_received = sum(list(map(lambda item: item.amount, money_received)))
        total_amount_sent = sum(list(map(lambda item: item.amount, money_sent)))

        return int(total_amount_received)-int(total_amount_sent)


    # Function to query the total money owed to an individual.
    async def query_money_owed(self, person):

        db = Prisma()
        await db.connect()

        user = await db.user.find_unique(where={'username': person})
        
        if not user:
            raise Exception("User not found")
        
        money_received = await db.usertransaction.find_many(where={'from_user': person})
        money_sent = await db.usertransaction.find_many(where={'to_user': person})

        await db.disconnect()

        total_amount_received = sum(list(map(lambda item: item.amount, money_received)))
        total_amount_sent = sum(list(map(lambda item: item.amount, money_sent)))

        return int(total_amount_sent)-int(total_amount_received)

    # Function to identify the person with the most money owed.
    async def query_most_money_owed(self):
        db = Prisma()
        await db.connect()

        users = await db.user.find_many(order={'balance': 'asc'}, take=1)

        await db.disconnect()

        if not len(users):
            raise Exception("No user found")

        return users[0].username

    # Function to identify the person who owes the most money to others.
    async def query_most_debt(self):
        db = Prisma()
        
        await db.connect()

        users = await db.user.find_many(order={'balance': 'desc'}, take=1)

        await db.disconnect()

        if not len(users):
            raise Exception("No user found")

        return users[0].username