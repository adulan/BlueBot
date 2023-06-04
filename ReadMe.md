# Blue Bot

Blue bot is made for discord and conducts polls to determine a Blue of the Week and prints a color swatch for any hex code posted that is a shade of blue.

## Discord Permissions

To function fully, Blue Bot requires the ```SERVER MEMBERS INTENT``` and ```MESSAGE CONTENT INTENT``` Priviliged Gateway Intents

It also requires the following Bot Permissions

```Send Mesages```

```Manage Mesages```

```Embed Links```

```Use External Emojis```

```Add Reactions```

```Read Messages/View Channels```


## Run Locally

docker build --pull --rm -f "Dockerfile" -t bluebot:latest "."

docker run -it \
--env DISCORD_TOKEN="YOUR_TOKEN" \
--env GUILD_ID="YOUR_SERVER_ID" \
--env POLL_CHANNEL_ID="ID_FOR_CHANNEL" \
--env BOTW="#0011AA" \
--rm --name always_blue.py bluebot:latest

### Environment Variables
| Name | Required | Description |
| --- | --- |--- |
| DISCORD_TOKEN | Required | Discord > Applications > Bot > Token |
| GUILD_ID | Required | Discord Server ID |
| POLL_CHANNEL_ID | Required | ID of the Server Channel to post the BotW Poll in
| BOTW | Optional | Initialize a Blue of the Week Hex value


## Install from package

```$ docker pull ghcr.io/adulan/bluebot:latest```

Update environment variables in docker-compose.yml

```$ docker compose up -d```