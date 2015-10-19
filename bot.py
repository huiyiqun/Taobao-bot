import telebot
import logging
from tbapi import TB_Searcher

logging.basicConfig(level=logging.DEBUG)
telebot.logger.setLevel(logging.DEBUG)
logger = logging.getLogger('tbbot')


def readfile(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

bot = telebot.TeleBot(readfile('token.txt'))


def retrieve_arg(text):
    return text.split(' ', 1).pop()


@bot.message_handler(commands=['tbsearch'])
def search_handler(message):
    arg = retrieve_arg(message.text)
    searcher = TB_Searcher(arg)
    try:
        logger.debug('Key word to search: [{}]'.format(arg))
        bot.reply_to(
            message,
            '\n'.join(
                '{}: {}'.format(title, url)
                for title, url in searcher.list_items())
        )
    except:
        logger.exception('Fail to list items')
        bot.reply_to(message, 'Ooops, 臣妾做不到啊')


@bot.message_handler(commands=['tbprice'])
def price_handler(message):
    arg = retrieve_arg(message.text)
    searcher = TB_Searcher(arg)
    try:
        logger.debug('Key word to search: [{}]'.format(arg))
        bot.reply_to(
            message,
            '最低价：{:.2f}RMB\n最高价：{:.2f}RMB\n平均价：{:.2f}RMB'
            .format(*searcher.price_tuple())
        )
    except:
        logger.exception('Fail to print prices')
        bot.reply_to(message, 'Ooops, 臣妾做不到啊')


if __name__ == '__main__':
    bot.polling(none_stop=True)
