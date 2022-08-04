import discord
from better_profanity import profanity
import lists
import functions_db
import functions_members
import shop_


def main_on_message(client, prev_mess):
    @client.event
    async def on_message(message):
        if (message.author == client.user):
            return

        msg = message.content

        name = str(message.author)
        #adds 1 to the users total counter
        functions_db.add_to_db(name, "grand", client)

        if (message.author == "DISBOARD#2760"):
            await message.channel.send("coolio")

        if profanity.contains_profanity(msg):

            name = str(message.author)
            functions_db.add_to_db(name, "counter", client)
            return

        #Shows you your N* of insults said
        if msg == '!counter':
            print_string = functions_db.word_counter(str(message.author))
            await message.channel.send(print_string)
            return

        #Shows you your points
        if msg == '!points':
            print_string, x = functions_db.grand_counter(str(message.author))
            await message.channel.send(print_string)
            return

        #Fixed the format in the db (adds counter:1 to members who dont have it)
        if msg == '!fixdb':
            functions_db.hard_fix(client)
            await message.channel.send("done")
            print("db fixed")
            return

        #Bot tells you something random... ...not my idea
        if msg == "!attention":
            phrase = lists.get_attention()
            await message.channel.send(phrase)
            return

        #Shows random monkey gif from giphy
        if msg == "!monke":
          url = functions_db.get_gif2()
          await message.channel.send(url)

        #Bot agrees with you
        if (msg == "Right?") or (msg == "right?"):
            await message.channel.send("yup")
            return

        #SHOWS TOP 3 MEMEBRS WHO'VE SWORN THE MOST
        if msg == "!top":
            string1, string2, string3 = functions_db.get_top("counter")

            embedVar = discord.Embed(title="LEADERBOARD", color=0xFCE500)
            embedVar.add_field(name="‎", value=string1, inline=False)
            embedVar.add_field(name="‎", value=string2, inline=False)
            embedVar.add_field(name="‎", value=string3, inline=False)

            await message.channel.send(embed=embedVar)
            return

        #SHOWS TOP 3 MEMBERS WITH THE MOST POINTS
        if msg == "!top points":
            string1, string2, string3 = functions_db.get_top("grand")

            embedVar = discord.Embed(title="LEADERBOARD", color=0xFCE500)
            embedVar.add_field(name="‎", value=string1, inline=False)
            embedVar.add_field(name="‎", value=string2, inline=False)
            embedVar.add_field(name="‎", value=string3, inline=False)

            await message.channel.send(embed=embedVar)
            return

        #SHOWS WHAT YOU CAN BUY WITH POINTS
        if msg == "!shop":
            shop = lists.get_shop()
            embedVar = discord.Embed(title="Shop", color=0xCC3388)
            for item, emoji in shop.items():
                embedVar.add_field(name=emoji, value=item, inline=False)
            await message.channel.send(embed=embedVar)
            return

        if msg.startswith("!buy"):
            if len(msg) == 4:
                await message.channel.send("You forgot to choose!")
                return
            else:
                print("ok")
                item = msg[5:]
                to_print = shop_.main_shop(str(message.author), item, client)
                await message.channel.send(to_print)

        if msg.startswith("!collection"):
            value1, value2, value3 = functions_db.show_collection(
                str(message.author))
            title = str(message.author)[:-5] + "'s " + "collection"
            embedVar = discord.Embed(title=title, color=0x98FFEF)
            embedVar.add_field(name="Times you got purred",
                               value=value1,
                               inline=False)
            embedVar.add_field(name="Kittens groomed",
                               value=value2,
                               inline=False)
            embedVar.add_field(name="Women molested",
                               value=value3,
                               inline=False)

            await message.channel.send(embed=embedVar)

        #SHOWS ALL THE MEMBERS IN A ROLES eg: "!roles admin team"
        if msg.startswith("!roles"):
            role = msg[7:]
            print(role)
            members = functions_members.get_role_members(role, client)
            if members == role:
                await message.channel.send("A valid role must be given")
            else:
                string_to_print = ""
                for member in members:
                    string_to_print = string_to_print + str(member) + '\n'

                title = "Users with the " + role + " role"
                embedVar = discord.Embed(title=title, color=0xA0D0EF)
                embedVar.add_field(name='‎',
                                   value=string_to_print,
                                   inline=False)
                await message.channel.send(embed=embedVar)
                return

        if msg == "!help":

            embedVar = discord.Embed(title="COMMAND LIST", color=0xA0D0EF)
            embedVar.add_field(name="!help",
                               value="Shows all commands available",
                               inline=False)
            embedVar.add_field(name="!attention",
                               value="For all you attention seeking whores",
                               inline=False)
            embedVar.add_field(
                name="!buy",
                value="Buy something from the !shop  \n  EG: !buy Kitten",
                inline=False)
            embedVar.add_field(
                name="!collection",
                value="Shows your collection the items you've bought",
                inline=False)
            embedVar.add_field(
                name="!counter",
                value="Displays how many bad words you have said",
                inline=False)
            embedVar.add_field(name="!monke",
                               value="Treats you with a random monkey gif",
                               inline=False)
            embedVar.add_field(name="!points",
                               value="Shows how many points you have" + '\n' +
                               "1 message = 1 point",
                               inline=False)
            embedVar.add_field(
                name="!roles",
                value=
                "This displays all the admin members \n EG: !roles admin team",
                inline=False)
            embedVar.add_field(
                name="!shop",
                value="View the things you can buy with your points",
                inline=False)
            embedVar.add_field(
                name="!top",
                value="Shows the top 3 of people who've sworn the most",
                inline=False)
            embedVar.add_field(
                name="!top points",
                value="Shows the top 3 of people who have the most points",
                inline=False)
            await message.channel.send(embed=embedVar)
            return

            #DELETE FROM CHANNEL IF NOT IN PROPER FORMAT
            if (message.channel.id == 944362633820270593) and (
                (msg[0] != "#") or (len(msg) != 7)):
                await message.delete()

            if message.channel.id == 947448160941400134:
                l = len(msg)
                if (msg[l - 2:] != "||") or (msg[:2] != "||") or (len(msg) <=
                                                                  4):
                    await message.delete()

            prev_mess1 = msg
