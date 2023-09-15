import csv

from prisma import Prisma

class FinancialSystem:
    def __init__(self):
        self.individuals = {}

    # Function to import transactions via csv
    async def import_transaction_from_csv(self, file_path):
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                db = Prisma()
                await db.connect()
                for row in reader:
                    from_user = await db.user.find_unique(where={'username': row[0].strip()})
                    to_user = await db.user.find_unique(where={'username': row[1].strip()})


                    if not from_user :
                        await db.user.create(data={'username': row[0].strip(), 'balance': 0-int(row[2])})
                    else :
                        await db.user.update(where={'username': row[0].strip()},data={'balance': from_user.balance - int(row[2])})

                    if not to_user :
                        await db.user.create(data={'username': row[1].strip(), 'balance': int(row[2])})
                    else :
                        await db.user.update(where={'username': row[1].strip()},data={'balance': to_user.balance + int(row[2])})

                    await db.usertransaction.create(data={'from_user': row[0].strip(), 'to_user': row[1].strip(), 'amount': int(row[2])})
                await db.disconnect()
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


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
        
        await db.disconnect()

        if not user:
            raise Exception("User not found")
        
        if user.balance < 0:
            return 0
        
        return user.balance


    # Function to query the total money owed to an individual.
    async def query_money_owed(self, person):

        db = Prisma()
        await db.connect()

        user = await db.user.find_unique(where={'username': person})

        await db.disconnect()
        
        if not user:
            raise Exception("User not found")
        
        if user.balance > 0: 
            return 0

        return abs(user.balance)

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