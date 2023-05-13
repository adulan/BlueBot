docker build --pull --rm -f "Dockerfile" -t bluebot:latest "."

docker run -it --env DISCORD_TOKEN="YOUR_TOKEN" --rm --name always_blue.py bluebot:latest