# Steps to run the project

1. Start postgres with the below command
   ```
   docker-compose up -d
   ```
2. Install the dependencies
    ```
    pip install -r requirements.txt
    ```
3. Run the migrations
    ```
    prisma migrate deploy
    ```
4. Run the script
    ```
    python main.py
    ```