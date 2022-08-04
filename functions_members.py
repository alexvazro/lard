import discord

#returns list of members that have the given role
def get_role_members(role_name, client):

  peopleWithRole = []

  if role_name == '':
    return(role_name)
  else:
    
    guild = client.guilds[0]
    #members = guild.fetch_members()
    role = discord.utils.find(lambda r: r.name == role_name, guild.roles)
    to_print = ""

    #makes sure the role exists
    if role in guild.roles:
      #iterate through all the members from the guild (server)
      #and add those to a list if they have the role
      for user in guild.members:
        if role in user.roles:
          peopleWithRole.append(user)
          to_print = to_print + str(user) + '\n'
      return(peopleWithRole)
    else:
      return(role_name)

