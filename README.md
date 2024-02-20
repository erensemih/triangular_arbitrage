## Setting Up Environment Variables

This project consists of 3 services, each requiring its own environment configuration. To set up your environment:

1. For each service, copy the `.env.example` file to a new file named `.env` within the same directory.
    - `cp analyse/.env.example analyse/.env`
    - `cp collect_ticker_data/.env.example collect_ticker_data/.env`
    - `cp trading/.env.example trading/.env`
  

2. Run the command below
   "docker-compose up --build"
