import youtube_dl, backend, discord, re
from dotenv import dotenv_values, load_dotenv

environment = dotenv_values(".env")
print("Connecting to MySQL Database...")
bkend = backend.Backend(
    environment["SQL_USER"],
    environment["SQL_PASSWORD"],
    environment["SQL_HOST"],
    environment["SQL_DATABASE"],
    environment["CONTENT_OUTPUT_DIR"],
    environment["CDN_HOSTNAME"]
)

client = discord.Client()

def find_urls(string):
    return re.findall(r'(https?://[^\s]+)', string)

def remove_embeds_from_content(embeds, content):
    for i in embeds:
        content = content.replace(i, "")
    
    return content

@client.event
async def on_ready():
    print(f'{client.user.name} Ready')

@client.event
async def on_message(message : discord.Message):
    if (message.author == client.user):
        return 
    
    #print(dir(message))

    if client.user not in message.mentions:
        # Bot has not been mentioned so the message can be disregaurded
        return
    
    print(message.reference)
    if (message.reference != None):
        message.reference.fail_if_not_exists = True
        msg = discord.utils.get(await message.channel.history(limit=100).flatten(), id=message.reference.to_message_reference_dict()["message_id"])
        print("Message replied to:", msg.content)
        process_urls = find_urls(msg.content)

        print(process_urls, msg.content)
    
    elif (len(find_urls(message.content)) != 0):
        process_urls = find_urls(message.content)
    
    else:
        return
    
    print(process_urls, message.content)

    if (len(process_urls) != 0):
        sent_message = await message.channel.send("Please wait...")
    
    final_message = ""
    for url in process_urls:
        send_message_embed = discord.Embed()
        send_message_embed.title = "Downloading..."
        send_message_embed.add_field(name="Status", value=f"Downloading {url}...", inline=True)

        await sent_message.edit(embed=send_message_embed)

        final_message += bkend.add_video(url) + "\n"
    
    if (len(process_urls) != 0):
        final_message = final_message.strip()

        if (".mkv" in final_message):
            final_message += "\n One (or more) of these videos is an MKV file. Sadly, my server does not have enough power to convert this video for you. Though, there are many online tools that can help you :)"

        await sent_message.delete()
        await message.channel.send(final_message)


client.run(environment["DISCORD_TOKEN"])