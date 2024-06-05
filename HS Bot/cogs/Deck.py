import discord, datetime
from discord.ext import commands
from discord import app_commands
from beckendService import getDeckInfo
from config.basicInfo import BasicInfo
# BasicInfo = {
#   "Format": {
#     "standard": "標準",
#     "wild": "開放"
#   }
# }

EmbedColor = {
    "standard": discord.Color.from_rgb(255, 190, 40),
    "wild": discord.Color.from_rgb(185, 100, 15)
}

def genMsgEmbed(deckCode, deckInfo) :
    embed = discord.Embed(
        title = "123",
        description = "tets1111",
        url = "genUrl(deckCode)",
        color = discord.Colour("#FFA225"),
        timestamp = datetime.datetime
    )
    return embed

def genUrl(code):
    url = "https://hearthstone.blizzard.com/zh-tw/deckbuilder?deckcode=" + code
    return url

# 定義名為 Main 的 Cog
class Deck(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 斜線指令
    # name指令顯示名稱，description指令顯示敘述
    # name的名稱，中、英文皆可，但不能使用大寫英文
    # @app_commands.describe(參數名稱 = 參數敘述)
    # 參數: 資料型態，可以限制使用者輸入的內容
    @app_commands.command(name = "deck", description = "輸入套牌代碼以獲得套牌資訊")
    @app_commands.describe(code = "輸入套牌代碼")
    async def deck(self, interaction: discord.Interaction, code: str):
        data = getDeckInfo(code)
        print(BasicInfo.get("Format").get(data["format"]) + " " + data["class"]["name"] + " 牌組")
        embed = discord.Embed(
            title = BasicInfo.get("Format").get(data["format"]) + " " + data["class"]["name"] + " 牌組",
            description = "這是一篇 Discord Embed 的教學文章",
            # url = genUrl(code),
            color = EmbedColor.get(data["format"]),
            timestamp = datetime.datetime.now()
        )
        embed.set_thumbnail(url = BasicInfo.get("Class").get(data["class"]["id"]).get("icon"))
        await interaction.response.send_message(embed = embed)

    # # 前綴指令
    # @commands.command()
    # async def Hello(self, ctx: commands.Context):
    #     await ctx.send("Hello, world!")

    # # 關鍵字觸發
    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     if message.author == self.bot.user:
    #         return
    #     if message.content == "Hello":
    #         await message.channel.send("Hello, world!")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Deck(bot))