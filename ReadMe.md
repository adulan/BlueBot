docker build --pull --rm -f "Dockerfile" -t bluebot:latest "."

docker run -it --env DISCORD_TOKEN="YOUR_TOKEN" --env GUILD_ID="YOUR_ID" --env POLL_CHANNEL_ID="ID_FOR_CHANNEL" --rm --name always_blue.py bluebot:latest