from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.callbacks import cb_store, cb_buy
from database import db_session, users, genres, games, usersgames, addresses
from utils.distance import distance


def get_menu(my_games=True, store=True):
    keyboard = InlineKeyboardMarkup()
    bnts = []
    if my_games:
        bnts.append(InlineKeyboardButton('My games', callback_data='my_games'))
    if store:
        bnts.append(InlineKeyboardButton('Store', callback_data=cb_store.new('-1', '1')))
    keyboard.add(*bnts)
    return keyboard


def get_store_menu(user_id, genre_id, page, max_page, this_game_id):
    keyboard = InlineKeyboardMarkup()
    db_sess = db_session.create_session()
    account_id = db_sess.query(users.Users).filter_by(user_id=user_id).first().id
    q_game = db_sess.query(usersgames.UsersGames).filter_by(user_id=account_id,
                                                            game_id=this_game_id).all()
    q_genres = db_sess.query(genres.Genres).all()
    view_genres = [InlineKeyboardButton('All', callback_data=cb_store.new(-1, 1) if genre_id != -1 else 'pass')]
    view_genres += [InlineKeyboardButton(i.title,
                                         callback_data=cb_store.new(i.id, 1) if i.id != genre_id else 'pass')
                    for i in q_genres]
    pagination = []
    if max_page < 7:
        pagination += [InlineKeyboardButton(str(i), callback_data=cb_store.new(genre_id, i)) if i != page
                       else InlineKeyboardButton('[{}]'.format(page), callback_data='pass')
                       for i in range(1, max_page + 1)]
    elif page < 4:
        pagination += [InlineKeyboardButton(str(i), callback_data=cb_store.new(genre_id, i)) if i != page
                       else InlineKeyboardButton('[{}]'.format(page), callback_data='pass')
                       for i in range(1, 6)] + \
                      [InlineKeyboardButton('...', callback_data='pass'),
                       InlineKeyboardButton(str(max_page), callback_data=cb_store.new(genre_id, max_page))]
    elif max_page - page < 3:
        pagination += [InlineKeyboardButton('1', callback_data=cb_store.new(genre_id, 1)),
                       InlineKeyboardButton('...', callback_data='pass')] + \
                      [InlineKeyboardButton(str(i), callback_data=cb_store.new(genre_id, i)) if i != page
                       else InlineKeyboardButton('[{}]'.format(page), callback_data='pass')
                       for i in range(max_page - 4, max_page + 1)]

    else:
        pagination += [InlineKeyboardButton('1', callback_data=cb_store.new(genre_id, 1)),
                       InlineKeyboardButton('...', callback_data='pass') if page - 1 > 3
                       else InlineKeyboardButton('2', callback_data=cb_store.new(genre_id, 2)),
                       InlineKeyboardButton(str(page - 1), callback_data=cb_store.new(genre_id, page - 1)),
                       InlineKeyboardButton('[{}]'.format(page), callback_data='pass'),
                       InlineKeyboardButton(str(page + 1), callback_data=cb_store.new(genre_id, page + 1)),
                       InlineKeyboardButton('...', callback_data='pass') if max_page - page > 3
                       else InlineKeyboardButton(str(page + 2), callback_data=cb_store.new(genre_id, page + 2)),
                       InlineKeyboardButton(str(max_page), callback_data=cb_store.new(genre_id, max_page))]
    btn_library = InlineKeyboardButton('My games', callback_data='my_games')
    if not q_game and this_game_id != -1:
        btn_buy = InlineKeyboardButton('Buy', callback_data=cb_buy.new(this_game_id))
        keyboard.row(btn_buy)
    keyboard.row(*view_genres)
    keyboard.row(*pagination)
    keyboard.row(btn_library)
    return keyboard


def get_pay():
    keyboard = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton('Pay', pay=True)
    btn_cancel = InlineKeyboardButton('Close', callback_data='close')
    keyboard.row(btn_pay)
    keyboard.row(btn_cancel)
    return keyboard


def get_close():
    keyboard = InlineKeyboardMarkup()
    btn_cancel = InlineKeyboardButton('Close', callback_data='close')
    keyboard.row(btn_cancel)
    return keyboard


def get_chose_delivery(lat, lon):
    keyboard = InlineKeyboardMarkup(row_width=1)
    db_sess = db_session.create_session()
    q = db_sess.query(addresses.Addresses).all()
    btns = []
    if q:
        nearest = min(((i.address, distance(lat, lon, i.lat, i.lon)) for i in q), key=lambda x: x[-1])
        btns.append(InlineKeyboardButton('Pick up yourself at the address {}'.format(nearest[0]),
                                         callback_data='pickup'))
    btns.append(InlineKeyboardButton('Order a courier by location', callback_data='courier'))
    btns.append(InlineKeyboardButton('Close', callback_data='close'))
    keyboard.add(*btns)
    return keyboard

