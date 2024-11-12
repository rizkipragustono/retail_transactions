# Retail Transactions
ETL data pipeline from PostgreSQL database to Snowflake data warehouse using Apache Airflow.
## Setup
Start by cloning the repository.

Run this command on the terminal to download a Docker image for Apache Airflow from Docker Hub.
<br>`docker pull apache/airflow`<br><br>

Create a `.env` file in the current directory to make sure that the Airflow container has the correct user and group IDs to avoid file permission conflicts when mounting volumes 
(e.g., if you're using local directories to store DAGs or logs). When running Docker containers with this environment file, the user and group inside the container will match those on the host system.
<br>`echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`<br><br>

Generate a fernet key and replace `YOUR_SECRET_KEY_HERE` in the `docker-compose.yaml` file with the generated key.
<br>`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`<br><br>

For first-time setup, initialize the database and create the default user.
<br>`docker-compose up airflow-init`<br><br>

Start the remaining services.
<br>`docker-compose up -d`<br><br>

Open up `https://localhost:8080` on the web browser to open Apache Airflow UI, on the **Admin** tab then go to **Connections**, and add the PostgreSQL and Snowflake Connection here.<br>

Stop and remove all services.
<br>`docker-compose down`<br><br>
