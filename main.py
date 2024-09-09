import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageSequence
import os
import random
from discord.object import Object
from discord.webhook.async_ import interaction_response_params


id_do_servidor = ()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

tree = bot.tree

@bot.command(name="polvo")
async def escolher(ctx, *opcoes: str):
    if len(opcoes) < 2 or len(opcoes) > 10:
        await ctx.send('preciso das opções para escolher!')
        return
    try:
        escolha = random.choice(opcoes)
        await ctx.send(f'{escolha}')
    except Exception as e:
        await ctx.send(f'Ocorreu um erro: {e}')

@bot.command(name='gif', help='Converte uma imagem enviada para GIF')
async def converter(ctx):
            # Verifique se a mensagem é uma resposta a outra mensagem
            if ctx.message.reference:
                # Obtenha a mensagem original
                original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                if original_message.attachments:
                    attachment = original_message.attachments[0]
                else:
                    await ctx.send('cade a imagem??!!?')
                    return
            elif ctx.message.attachments:
                attachment = ctx.message.attachments[0]
            else:
                await ctx.send('manda a imagem!!!')
                return

            try:
                # Salvar a imagem temporariamente
                nome_arquivo = f'temp_{attachment.filename}'
                await attachment.save(nome_arquivo)

                # Converter para GIF
                with Image.open(nome_arquivo) as img:
                    frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
                    frames[0].save('converted.gif', save_all=True, append_images=frames[1:], duration=200, loop=0)

                # Enviar o GIF convertido
                await ctx.send(f"{ctx.author.mention}", file=discord.File('converted.gif'))

            except Exception as e:
                await ctx.send(f'Ocorreu um erro: {e}')
            finally:
                # Remover os arquivos temporários
                if os.path.exists(nome_arquivo):
                    os.remove(nome_arquivo)
                if os.path.exists('converted.gif'):
                    os.remove('converted.gif')

bot.run('token do bot')



