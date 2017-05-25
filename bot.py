import logging
from tbapi import TB_Searcher
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('tbbot')

help_msg = '''
/tbsearch <keywords> - Search over taobao.com and return list of items.
/tbprice <keywords> - Search over taobao.com and return price.
/tbuprice <keywords> - Search over taobao.com and return price of per unit.
/help - print this message.
'''


def readfile(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def search_handler(bot, update, args):
    arg = ' '.join(args)
    if not arg:
        return help_handler(bot, update)
    searcher = TB_Searcher(arg)
    try:
        logger.debug('Key word to search: [{}]'.format(arg))
        update.message.reply_text(
            '\n'.join(
                '{}: {}'.format(title, url)
                for title, url in searcher.list_items()))
    except:
        logger.exception('Fail to list items')
        update.message.reply_text('Ooops, 臣妾做不到啊')


def price_handler(bot, update, args):
    arg = ' '.join(args)
    if not arg:
        return help_handler(message)
    searcher = TB_Searcher(arg)
    try:
        logger.debug('Key word to search: [{}]'.format(arg))
        update.message.reply_text(
            '最低：￥{:.2f}/最高：￥{:.2f}/平均：￥{:.2f}'
            .format(*searcher.price_tuple())
        )
    except:
        logger.exception('Fail to print prices')
        update.message.reply_text('Ooops, 臣妾做不到啊')


def unit_price_handler(bot, update, args):
    arg = ' '.join(args)
    if not arg:
        return help_handler(message)
    searcher = TB_Searcher(arg)
    try:
        logger.debug('Key word to search: [{}]'.format(arg))
        update.message.reply_text(
            '（每斤）最低：￥{:.2f}/最高：￥{:.2f}/平均：￥{:.2f}'
            .format(*searcher.unit_price_tuple())
        )
    except:
        logger.exception('Fail to print unit prices')
        update.message.reply_text('Ooops, 臣妾做不到啊（去掉u试试看）')


def help_handler(bot, update):
    update.message.reply_text(help_msg)


updater = Updater(readfile('token.txt'))

updater.dispatcher.add_handler(CommandHandler('tbsearch', search_handler, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('tbprice', price_handler, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('tbuprice', unit_price_handler, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('help', help_handler))


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
