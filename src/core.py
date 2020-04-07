from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from conf.settings import TELEGRAM_TOKEN

import random


dados_jogo = {}

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Olá, eu sou o GamesBot! Para jogar Quem Sou Eu? com seus amigos, me adicione ao seu grupo! Caso queira obter mais informações sobre como jogar digite /ajuda'
    )
def criar_quem(bot, update, args):
    f = open("pessoas.txt", "r")
    listapessoas = f.read().split(',')
    dados_jogo[args[0][1:]]=listapessoas[random.randint(0,9)]
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Pessoa gerada com sucesso!' 
    )
def receber_quem(bot, update, args):
    if update.message.from_user.username == args[0][1:]:
        bot.send_message(
            chat_id=update.message.from_user.id,
            text = 'Não trapaceie!'
        )
    else:
        bot.send_message(
            chat_id=update.message.from_user.id,
            text= args[0][1:] + ' é ' + dados_jogo[args[0][1:]]
        )
def adivinhar(bot, update, args):
    pessoa = " ".join(args)
    if pessoa.lower() == dados_jogo[update.message.from_user.username].lower():
        bot.send_message(
        chat_id=update.message.chat_id,
        text='Parabéns, '+update.message.from_user.first_name+'! Você acertou!'
        )
    else:
        bot.send_message(
        chat_id=update.message.chat_id,
        text='Infelizmente, você errou! :( Tente mais uma vez, '+update.message.from_user.first_name+'!'
        )
def ajuda(bot, update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = 'Os comandos para jogar são: \n/criar_personagem @usuário_que_irá_adivinhar: Este comando gera o personagem que usuário marcado será. \n/receber_personagem @usuario: Este comando envia no privado quem o usuário marcado é no jogo.\n/adivinhar Personagem: Este comando é utilizado pela pessoa que está tentando adivinhar quem ela é!\nSugiro um máximo de 10 tentativas, mas vocês decidem!\nPARA RECEBER MINHAS MENSAGENS NO PRIVADO, INICIE UMA CONVERSA COMIGO ANTES'
    )
def unknown(bot, update):
    response_message = "Bip-Bop-Comando desconhecido"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('criar_personagem', criar_quem, pass_args = True)
    )
    dispatcher.add_handler(
        CommandHandler('receber_personagem', receber_quem, pass_args = True)
    )
    dispatcher.add_handler(
        CommandHandler('adivinhar', adivinhar, pass_args = True)
    )
    dispatcher.add_handler(
        CommandHandler('ajuda', ajuda)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()