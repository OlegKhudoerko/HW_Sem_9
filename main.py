from secret import KEY
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import my_game

count = 0
token = [chr(10060), chr(11093)]


def start(update: Update, context: CallbackContext) -> int:
    global count
    counter = 0
    my_game.reset()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=my_game.draw_board())
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Введите номер в поле 1 .. 9\nПозиция {token[count % 2]}? ")
    return 0


def turn(update: Update, context: CallbackContext) -> int:
    global count
    position = update.message.text
    response = my_game.place_sign(count % 2, position)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response)
    if response == "ok":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=my_game.draw_board())
        count += 1
        if count > 3:
            if my_game.check_win():
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"{my_game.check_win()} - WIN{chr(127942)}{chr(127881)}!")
                my_game.reset()
                counter = 0
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=my_game.draw_board())
        if counter == 8:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Draw game {chr(129318)}{chr(129309)}")
            my_game.reset()
            count = 0
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=my_game.draw_board())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Введите номер в поле 1 .. 9\nПозиция {token[counter % 2]}? ")
    return 0


def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END


def main():
    updater = Updater(KEY)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(Filters.all, turn)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
