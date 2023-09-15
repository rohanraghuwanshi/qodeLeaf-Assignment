import os
import asyncio

from FinanceSystem import FinancialSystem

async def main() -> None:

    financial_system = FinancialSystem()
    
    while True:

        os.system('clear')
        
        print("Please type a command from below to execute")
        print('1. To record a transaction: "add_transaction [from] [to] [amount transferred]"')
        print('2. To get the debt of a user: "query_debt [user]"')
        print('3. To get the money owed : "query_money_owed [user]"')
        print('4. To get the most money owed: "query_most_money_owed"')
        print('5. To get the most debt: "query_most_debt"')
        print('6. To quit: "exit"')
            

        try:
            command = input("\nEnter operation: ")
            
            input_list = command.split()
            command = input_list[0]

            print()

            if command == 'add_transaction':
                from_person, to_person, amount = input_list[1], input_list[2], int(input_list[3])
                await financial_system.add_transaction(from_person, to_person, amount)
            elif command == 'query_debt':
                person = input_list[1]
                debt = await financial_system.query_debt(person)
                print(f"{person} owes {debt} money.")
            elif command == 'query_money_owed':
                person = input_list[1]
                money_owed = await financial_system.query_money_owed(person)
                print(f"{person} is owed {money_owed} money.")
            elif command == 'query_most_money_owed':
                person = await financial_system.query_most_money_owed()
                print(f"Person with the most money owed: {person}")
            elif command == 'query_most_debt':
                person = await financial_system.query_most_debt()
                print(f"Person with the most debt: {person}")
            elif command == 'exit':
                break
            else:
                print('Invalid command.')
        except Exception as e:
            print(e.args[0])

        should_continue = input("\nDo you wish to continue? (y/n): ")

        if(should_continue=='n'):
            break


if __name__ == '__main__':
        asyncio.run(main())