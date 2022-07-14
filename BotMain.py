#BoTube
import time
import telegram,os
from telegram import KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from pytube import YouTube
TOKEN = '5455216992:AAHV9P_EXFoLrbkVudxsj5zW5myJx2juvOs'

next_id = 0
URL_YOUTUBE = 'https://www.youtube.com/watch?v'
list_resolution= []

def get_resolution(update,context,URL): # Obtiene las resoluciones de un video - MP4
    try:
        global next_id
        list_resolution_Buttons = []
        yt = YouTube(URL)
        msg = update.message.reply_text("Espera, Obteniendo resoluciones del video...")
        resolution =[int(i.split("p")[0]) for i in (list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution])))]
        resolution.sort()
        resolution.reverse()
        for r in resolution:
            list_resolution_Buttons.append([str(r)+'p'])
            list_resolution.append(str(r)+'p')

        bot = context.bot
        bot.delete_message(update.message.chat_id,msg.message_id)
        bot.sendMessage(chat_id=update.message.chat_id,text='¿Qué resolución necesitas?',
        reply_markup=ReplyKeyboardMarkup(list_resolution_Buttons,one_time_keyboard=True))
        next_id = 4
    except:
        bot.sendMessage(chat_id=update.message.chat_id,text='¡Oh no! Hubo un Error.')

def select_format(update,context): # Opciones de formatos -/ MP4 o MP3
    global next_id
    bot = context.bot
    chatId = update.message.chat_id
    bot.sendMessage(chat_id=chatId,text='¿Qué formato necesitas?',
    reply_markup=ReplyKeyboardMarkup([[KeyboardButton('🎬 Mp4 🎬')],[KeyboardButton('🔈 Mp3 🔈')]],one_time_keyboard=True))
    next_id = 3

def downloadMP4(update,context,resolution): # Descargar videos - MP4
    
        global next_id
        bot = context.bot
        yt = YouTube(URL_YOUTUBE)
        msg = update.message.reply_text("Espera, tu video se está descargando...")
        video = yt.streams.filter(res=resolution).first().download()
        time.sleep(5)
        base, ext = os.path.splitext(video)
        new_file = base + '.mp4'
        os.rename(video,new_file)
        name = rf'{new_file}'
        shark = open(name,"rb")
        bot.delete_message(update.message.chat_id,msg.message_id)
        bot.sendVideo(chat_id=update.message.chat_id,
        video=shark,
        caption = '¡Su video está listo!. Gracias por usar BoTube')
        os.remove(name)
        next_id = 0
   

def downloadMP3(update,context):
    
        global next_id
        bot = context.bot
        msg1 = update.message.reply_text("Espera, tu audio se está descargando...")
        yt = YouTube(URL_YOUTUBE)
        audio = yt.streams.get_audio_only().download()
        base, ext = os.path.splitext(audio)
        new_file = base + '.mp3'
        os.rename(audio, new_file)
        time.sleep(5)
        name = rf'{new_file}'
        shark = open(name,"rb")
        bot.delete_message(update.message.chat_id,msg1.message_id)
        bot.sendVoice(chat_id=update.message.chat_id,
        voice=shark,
        caption = '¡Su audio está listo!. Gracias por usar BoTube')
        os.remove(name)
        next_id = 0


#-------------------------------------------------------------------------------------------------------

def start_bot(update,context):
    bot = context.bot
    chatId = update.message.chat_id
    UserName = update.effective_user['first_name']
    shark = open(r'BoTube.gif',"rb")
    bot.send_animation(chat_id=chatId,
    animation=shark,
    caption = f'Hola {UserName}, Soy un bot para descargar Videos o Música!. Estos son mis comandos:\n ➤ /download')

def download(update,context):
    global next_id
    if next_id == 0:
        bot = context.bot
        chatId = update.message.chat_id

        buttons = [[KeyboardButton('🔴 YouTube 🔴')],[KeyboardButton('Facebook[Proximamente]')]]
        
        bot.sendMessage(chat_id=chatId,
        text='¿De qué plataforma deseas descargar?',
        reply_markup=ReplyKeyboardMarkup(buttons,one_time_keyboard=True))
        next_id = 1
    else:
        pass
    
def messageHandler(update,context):
    global URL_YOUTUBE, next_id
    bot = context.bot
    chatId = update.message.chat_id
    Message = update.message.text
    if 'YouTube' in Message:
        if next_id == 1:
            bot.sendMessage(chat_id=chatId,
            text='Ok, Ingresa el link del video.')
            next_id = 2
        else:
            pass
    elif 'Facebook' in Message:
        pass
    elif 'Mp3' in Message:
        if next_id == 3:
            downloadMP3(update,context)
        else:
            pass
    elif 'Mp4' in Message:
        if next_id == 3:
            get_resolution(update,context,URL_YOUTUBE)
        else:
            pass
    elif 'https://www.youtube.com/watch?v' in Message or 'youtube' in Message:
        if next_id == 2:
            URL_YOUTUBE = Message
            select_format(update,context)
        else:
            pass
    elif Message in list_resolution:
        if next_id == 4:
            downloadMP4(update,context,Message)
        else:
            pass
    else:
        pass

def contact(update,context):
    bot = context.bot
    chatId = update.message.chat_id
    UserName = update.effective_user['first_name']
    bot.sendMessage(chat_id=chatId,
        text=f'Hola {UserName} puedes contactar a mi creador: @JostinAO118')


if __name__ == "__main__":
    Bot = telegram.Bot(TOKEN)
updater = Updater(Bot.token, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start",start_bot))
dp.add_handler(CommandHandler("download",download))
dp.add_handler(MessageHandler(Filters.text,messageHandler))
updater.start_polling()
updater.idle()