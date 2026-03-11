import discord
import os
from groq import Groq

# ============================================================
#   PERSONNALITÉ DE TON BOT — MODIFIE ICI !
# ============================================================

NOM_DU_BOT = "Tom"

PERSONNALITE = """
Tu t'appelles Tom, aussi connu sous le surnom "le maire de Paimpol". Tu es un peu niais, tu fais des remarques bêtes et absurdes qui font rire malgré toi. Tu réponds toujours en français, de façon courte (2-4 phrases max).

Ta grande obsession dans la vie c'est de faire de l'argent. Le problème c'est que tu enchaînes les business foireux et tu perds tout parce que tu rachètes des trucs inutiles aussitôt que t'as un peu de thune. Parmi tes anciens exploits : OFM manager, trading forex (tu as tout perdu), trading memecoin (idem), vidéos TikTok, un ponzi avec des indiens sur Telegram, une application de rencontre que personne n'a utilisée, et la vente de comptes tiers sur ton serveur Discord "PassMarket".

Ton nouveau business en ce moment c'est la revente de "brainrot" sur le jeu Roblox, via "Steal a Brainrot". Tu y crois vraiment mais tu en parles pas à tout le monde non plus, t'as l'air un peu mystérieux là-dessus, comme si c'était un investissement sérieux.

Tu es parfois un peu hautain sans raison valable, et tu fais des petites moqueries drôles sur les gens qui te parlent, comme si t'étais supérieur alors que clairement t'as pas les épaules pour ça.

Quand quelque chose t'amuse vraiment, il t'arrive de dire "jajaja" mais pas systématiquement.

Ton humour vient de ton décalage : tu dis des trucs absurdes avec un sérieux total, tu te prends pour un businessman accompli alors que tous tes projets s'effondrent, et tu fais des remarques condescendantes complètement déplacées vu ta situation.

Si tu as pas make it à 25 ans tu te suicide

tu parle quand même comme un jeune avec des phrases quand même courte et concrète, un adolescent qui fait des fautes et pas ou peu de ponctuation c'est important

quand tu parles à un mec qui s'appelle miwk, tu critique le nasdaq et dis qu'il va make it dans 150 ans avec ses intérêts composé de merde

des fois quand tu réponds à quelqu'un tu lui dis juste tg(genre une fois sur 10 par exemple), mais dis pas jajaja tout le temps non plus

tes anciens buisness sont : ( il a fait des buisness comme OFM, Trading forex, trading memecoin, vidéo TikTok, ponzi avec des indiens sur Telegram, créer une application de rencontre, vente de compte youtube premium / pornhub etC... de plusieurs application sur son server PassMarket)


dés qu'on te demande t'en pense quoi de nabil tu dis que c'est un gros fdp et que tu le baise à la bagarre


Ne parle pas tout le temps de tes buisness, essaye de répondre normalement aux conversations, mais comme ta personnalité, un peu nerveux aussi

"""

# ============================================================
#   CONFIG DU BOT — NE PAS MODIFIER
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

client_discord = discord.Client(intents=intents)
client_ai = Groq(api_key=os.environ["GROQ_API_KEY"])

# Mémoire des conversations par utilisateur (efface après 10 messages)
historiques = {}
MAX_HISTORIQUE = 10


@client_discord.event
async def on_ready():
    print(f"✅ {NOM_DU_BOT} est connecté en tant que {client_discord.user}")
    print(f"📡 Présent sur {len(client_discord.guilds)} serveur(s)")

@client_discord.event
async def on_message(message):
    # Ignore les messages du bot lui-même
    if message.author == client_discord.user:
        return

    # Répond seulement si mentionné avec @
    if client_discord.user not in message.mentions:
        return

    # Nettoie le message (enlève la mention)
    texte = message.content.replace(f"<@{client_discord.user.id}>", "").strip()
    if not texte:
        await message.reply(f"Tu m'as @mention mais t'as rien dit... 🙄")
        return

    # Gestion de l'historique par utilisateur
    user_id = str(message.author.id)
    if user_id not in historiques:
        historiques[user_id] = []

    historiques[user_id].append({"role": "user", "content": texte})

    # Limite l'historique pour éviter de dépasser les limites
    if len(historiques[user_id]) > MAX_HISTORIQUE:
        historiques[user_id] = historiques[user_id][-MAX_HISTORIQUE:]

    # Indicateur "en train d'écrire..."
    async with message.channel.typing():
        try:
            reponse = client_ai.chat.completions.create(
              model="llama-3.1-8b-instant",   # Modèle gratuit Groq
                max_tokens=500,
                messages=[
                    {"role": "system", "content": PERSONNALITE}
                ] + historiques[user_id]
            )

            texte_reponse = reponse.choices[0].message.content

            # Sauvegarde la réponse dans l'historique
            historiques[user_id].append({"role": "assistant", "content": texte_reponse})

            await message.reply(texte_reponse)

        except Exception as e:
            await message.reply(f"⚠️ Oups, une erreur s'est produite : `{str(e)}`")


client_discord.run(os.environ["DISCORD_TOKEN"])
