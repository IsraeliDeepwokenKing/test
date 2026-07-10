import discord


async def create_carry_role(guild, carry_id):

    role_name = f"Carry-{carry_id}"

    role = discord.utils.get(
        guild.roles,
        name=role_name
    )

    if role:
        return role


    role = await guild.create_role(
        name=role_name,
        reason="Temporary Deepwoken carry role"
    )

    return role



async def give_carry_role(member, role):

    if role not in member.roles:
        await member.add_roles(role)



async def remove_carry_role(member, role):

    if role in member.roles:
        await member.remove_roles(role)
