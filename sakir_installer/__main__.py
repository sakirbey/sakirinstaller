import heroku3
from time import time
import random
import requests
from git import Repo
from sakir_installer import *
import os
import base64
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditPhotoRequest, CreateChannelRequest
from asyncio import get_event_loop
from .language import LANG, COUNTRY, LANGUAGE, TZ
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.live_render import LiveRender
console = Console()

LANG = LANG['MAIN']

def connect (api):
    heroku_conn = heroku3.from_key(api)
    try:
        heroku_conn.apps()
    except:
        hata(LANG['INVALID_KEY'])
        exit(1)
    return heroku_conn

def createApp (connect):
    appname = "sakiribey" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    try:
        connect.create_app(name=appname, stack_id_or_name='container', region_id_or_name="eu")
    except requests.exceptions.HTTPError:
        hata(LANG['MOST_APP'])
        exit(1)
    return appname

def hgit (connect, repo, appname):
    global api
    app = connect.apps()[appname]
    giturl = app.git_url.replace(
            "https://", "https://api:" + api + "@")

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        hata(LANG['ERROR'] + str(e))

    bilgi(LANG['POSTGRE'])
    app.install_addon(plan_id_or_name='062a1cc7-f79f-404c-9f91-135f70175577', config={})
    basarili(LANG['SUCCESS_POSTGRE'])
    return app

async def botlog (String, Api, Hash):
    Client = TelegramClient(StringSession(String), Api, Hash)
    await Client.start()

    KanalId = await Client(CreateChannelRequest(
        title="✨ SAKİRİ GÖTTEN 𝗕𝗼𝘁𝗹𝗼𝗴 ✨",
        about=LANG['AUTO_BOTLOG'],
        megagroup=True
    ))
    KanalId = KanalId.chats[0].id

    Photo = await Client.upload_file(file='MisakiUserBot.jpg')
    await Client(EditPhotoRequest(channel=KanalId, 
        photo=Photo))
    msg = await Client.send_message(KanalId, LANG['DONT_LEAVE'])
    await msg.pin()

    KanalId = str(KanalId)
    if "-100" in KanalId:
        return KanalId
    else:
        return "-100" + KanalId

if __name__ == "__main__":
    logo(LANGUAGE)
    loop = get_event_loop()
    api = soru(LANG['HEROKU_KEY'])
    bilgi(LANG['HEROKU_KEY_LOGIN'])
    heroku = connect(api)
    basarili(LANG['LOGGED'])

    # Telegram #
    stri, aid, ahash = main()
    basarili(LANG['SUCCESS_STRING'])
    baslangic = time()

    # Heroku #
    bilgi(LANG['CREATING_APP'])
    appname = createApp(heroku)
    basarili(LANG['SUCCESS_APP'])
    bilgi(LANG['DOWNLOADING'])

    
     
     #HaydiKardeşim kendi reponu yazamadınmı başka kapıya yok sana auto#
    SyperStringKey = "tobresuiris/"
    GiperStringKey = "yebmedre/"
    InvalidKey = "moc.buhtig//:sptth" 
    str1 = SyperStringKey+GiperStringKey+InvalidKey
    stringlength=len(str1)
    slicedString=str1[stringlength::-1]

    if os.path.isdir("./sakiruserbot/"):
        rm_r("./misakiuserbot/")
    repo = Repo.clone_from(slicedString,"./sakiruserbot/", branch="master")
    basarili(LANG['DOWNLOADED'])
    onemli(f"[bold white]{LANG['DEPLOYING']}")
    app = hgit(heroku, repo, appname)
    config = app.config()

    bilgi(LANG['WRITING_CONFIG'])

    config['ANTI_SPAMBOT'] = 'False'
    config['ANTI_SPAMBOT_SHOUT'] = 'True'
    config['API_HASH'] = ahash
    config['API_KEY'] = str(aid)
    config['BOTLOG'] = "False"
    config['BOTLOG_CHATID'] = "0"
    config['CLEAN_WELCOME'] = "True"
    config['CONSOLE_LOGGER_VERBOSE'] = "False"
    config['COUNTRY'] = COUNTRY
    config['DEFAULT_BIO'] = "✨ @Sakiruserbot ✨ "
    config['DEFAULT_NAME'] = "SAKİRİ GÖTTEN SİRİ KRALDIR"
    config['GALERI_SURE'] = "60"
    config['CHROME_DRIVER'] = "/usr/sbin/chromedriver"
    config['GOOGLE_CHROME_BIN'] = "/usr/sbin/chromium"
    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname
    config['STRING_SESSION'] = stri
    config['HEROKU_MEMEZ'] = "True"
    config['LOGSPAMMER'] = "False"
    config['BL_CHATS'] = "False"
    config['PM_AUTO_BAN'] = "False"
    config['PM_AUTO_BAN_LIMIT'] = "6"
    config['TMP_DOWNLOAD_DIRECTORY'] = "./downloads/"
    config['TZ'] = TZ
    config['TZ_NUMBER'] = "1"
    config['UPSTREAM_REPO_URL'] = "https://github.com/sakirbey/sakiruserbot"
    config['WARN_LIMIT'] = "5"
    config['WARN_MODE'] = "gmute"
    config['LANGUAGE'] = LANGUAGE

    basarili(LANG['SUCCESS_CONFIG'])
    bilgi(LANG['OPENING_DYNO'])

    try:
        app.process_formation()["worker"].scale(1)
    except:
        hata(LANG['ERROR_DYNO'])
        exit(1)

    basarili(LANG['OPENED_DYNO'])
    basarili(LANG['SUCCESS_DEPLOY'])

    console.print(Panel(f"\n[bold green]{LANG['END'].format(round(time() - baslangic))}[/]\n", title="✨ Sakir Userbot ✨", border_style="bold green"), justify="center")

    BotLog = False

    KanalId = loop.run_until_complete(botlog(stri, aid, ahash))
    config['BOTLOG'] = "True"
    config['BOTLOG_CHATID'] = KanalId

    basarili(f"✅ {LANG['AFTERDEPLOY']}")

    console.print(Panel(f"\n[bold yellow]{LANG['LOGOSETTINGS']}[/]\n\n[bold white]🌟 {LANG['SETTINGS']}", expand=True), justify="center")

    BotLog = True

    Sonra = Confirm.ask(f"❓", default=True)
    if Sonra == True:
        Cevap = ""
        while not Cevap == "5":
            if Cevap == "1":
                if BotLog:
                    config['LOGSPAMMER'] = "True"
                    basarili(LANG['SUCCESS_LOG'])

                else:
                    hata(LANG['NEED_BOTLOG'])

            elif Cevap == "2":
                config['OTOMATIK_KATILMA'] = "False"
                basarili(LANG['SUCCESS_SUP'])

            elif Cevap == "3":
                config['PM_AUTO_BAN'] = "True"
                basarili(LANG['SUCCESS_PMAUTO'])

            elif Cevap == "4":
                whatisyourname = str(soru(LANG['WHAT_IS_YOUR_NAME']))
                config['DEFAULT_NAME'] = whatisyourname
                basarili(LANG['SUCCESS_DEFAULTNAME'])
                

            secenek(f"[bold magenta][1][/] 💾 {LANG['NO_LOG']}")
            secenek(f"[bold magenta][2][/] 📣 {LANG['NO_SUP']}")
            secenek(f"[bold magenta][3][/] 💬 {LANG['PMOTO']}")
            secenek(f"[bold magenta][4][/] 🔖 {LANG['DNAME']}")
            secenek(f"[bold magenta][5][/] 💥 {LANG['CLOSE']}")

            lsoru(Panel(f"\n[bold yellow]{LANG['WHAT_YOU_WANT']}\n"))
            Cevap = Prompt.ask(f"❓", choices=["1", "2", "3", "4", "5"], default="5")
