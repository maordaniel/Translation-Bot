from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from googletrans import Translator
from emoji import emojize
import langid

updater = Updater(token='Token', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    wave = emojize(":wave:", use_aliases=True)
    smiley = emojize(":smiley:", use_aliases=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                         text=f"""Hello {update.message.from_user.first_name} {update.message.from_user.last_name}{wave}
I'm The Translation Bot.
I support English and Hebrew.
Enjoy! {smiley}""")


def echo(update, context):
    translate = Translator().translate
    lang = langid.classify(update.message.text)[0]
    if lang == 'en':
        dest = 'he'
    elif lang == 'he':
        dest = 'en'
    else:
        return context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry I only support English and Hebrew.')
    val = translate(update.message.text, dest=dest).text
    context.bot.send_message(chat_id=update.effective_chat.id, text=val)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))


updater.start_polling()
updater.idle()

