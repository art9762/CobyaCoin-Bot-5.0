import telebot
import config as cf
import support as sp
import time as tm
import random as r
import TableLib as db
import os
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')

bot = telebot.TeleBot(cf.tocken)

# переменные и всякое такое



burse = []
price = 0
coin = 0
nft_n = ""
nft_p = 0
usern = ''
pr = ''
sc = ''
history = []
coins_am = []
coins_am = db.getMas('coins_amount.txt')
print(coins_am)
h = db.getCols("history.txt")
for i in h:
    history.append(int(i[0]))
print(history)
x = ["0"]
y = ["0"]
sp.update()
#print(tm.ctime(1694548849))
center_bank_leaves = int(db.getMas('center')[0][0])
center_bank_coins = int(db.getMas('center')[1][0])
name = ''
course = int(db.getMas('course')[len(db.getMas('course'))-1][0])
transactions = int(db.getMas('course')[len(db.getMas('course'))-1][1])
videocards_course = int(db.getMas('course')[len(db.getMas('course'))-1][2])
timer = 0

admins = ["@IL76pd", "@societykolyan", "@unlucky_POvelitel" , '@Dan9kov']
ban = ['@Hv2_0' , '@user1864926' , '@unknown_user63594', '@NEGRA0956']
promocodeL = ["K9x7", "R2g6", "T3d8", "M4h5", "L6y2", "J1p9", "F5a2", "N8z1", "D7b3", "G2s4", "#KamilaChiter"]
promocodeC = ["Q4x8", "P7g3", "R2d6", "S3h8", "M5l4", "L6f2", "K1p9", "J5a2", "F8z1", "N7b3", "D2s4"]
    
def sum_of_last_10_elements(arr):
    if len(arr) <= 10:
        return sum(arr)
    else:
        return sum(arr[-10:])
    
def auction_update():
    try:
        auc = db.getMas("auction.txt")
        users = db.getMas('users.txt')
        auc2 = []
        for i in range(len(auc)):
            seller = db.find_string(users, auc[i][0])
            if auc[i][5] != 'none':
                buyer = db.find_string(users, auc[i][5])
                if int(round(tm.time()))-int(auc[i][4]) > 10*60*60:
                    seller_cb = int(users[seller][2])+int(auc[i][2])
                    buyer_cb = int(users[buyer][2])-int(auc[i][2])

                    users[seller][2] = seller_cb
                    users[buyer][2]=buyer_cb
                    
                    bot.send_message(users[buyer][3], f"Вы успешно приобрели {auc[i][1]}")
                    bot.send_message(users[seller][3], f"{auc[i][5]} приобрел ваш товар в аукционе за {auc[i][2]}")

                    db.wrTo(users, 'users.txt')
                    
                else:
                    auc2.append(auc[i])
            else:
                auc2.append(auc[i])
        
        auc = auc2
        db.wrTo(auc, 'auction.txt')
    except Exception as e:
        print(e, "auc_update")
        pass

    
def center_bank():
    auction_update()
    try:
        global course
        global center_bank_leaves
        global center_bank_coins
        global transactions
        ce = db.getMas("center")
        us = db.getMas("users.txt")
        burse = db.getMas("burse.txt")
        
        if center_bank_coins < 2000:
            center_bank_leaves -= course*(2000-center_bank_coins)
            center_bank_coins += 2000-center_bank_coins
        leng = len(burse)
        sc = 0
        burse2 = []
        for sc in range(len(burse)):
            if not(int(round(tm.time())) - int(burse[sc][3]) > 172800):
                burse2.append(burse[sc])

        burse = burse2
        
                
            
        
        if len(burse) > 51:
            while len(burse) > 51:
                ch = r.randint(1, len(burse)-1)
                seller = db.find_string(us, burse[int(ch)][0])
                if int(burse[int(ch)][1]) < center_bank_leaves:
                    sel_coin = int(us[seller][2])-int(burse[int(ch)][1])
                    sel_leave = int(us[seller][1])+int(burse[int(ch)][2])
                    us[seller][1] = str(sel_leave)
                    us[seller][2] = str(sel_coin)

                    center_bank_leaves -= int(burse[int(ch)][2])
                    center_bank_coins += int(burse[int(ch)][1])
                    
                    ce[0][0] = str(center_bank_leaves)
                    ce[1][0] = str(center_bank_coins)

                    db.wrTo(ce,"center")

                    transactions += 1
                    history.append(int(burse[int(ch)][2])//int(burse[int(ch)][1]))
                    db.addMass([str(int(burse[int(ch)][2])//int(burse[int(ch)][1]))], "history.txt")
                    c = sum_of_last_10_elements(history)
                    course = c//transactions
                    abv = int(burse[int(ch)][2])
                    #print("adasdasdas")
                    bot.send_message(us[seller][3], f"Ваше объявление было куплено Центробанком! \nВы получили {abv} коинов")
                    del burse[int(ch)]
                else:
                    break

        db.wrTo(us, 'users.txt')
            
        db.wrTo(burse, 'burse.txt')
    except Exception as e:
        print(e)
        pass


def update_page(page=0):
    ITEMS_PER_PAGE = 10
    burse = db.getMas("burse.txt")
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    if start_index >= len(burse):
        start_index = 0
    if end_index >= len(burse):
        end_index = len(burse)

    out = ''

    if len(burse) > 0:
        for i in range(start_index, end_index):
            out += str(i+1) + '. ' + burse[i][0] + ' (' + str(round((tm.time()-int(burse[i][3]))/3600)) + 'ч' +') продаёт ' + burse[i][1] + ' CBC за ' + burse[i][2] + ' к.л.'+ '\n' + '\n'
        return out
    else:
        return "Биржа пуста("
    
def split_list_into_chunks(lst, chunk_size=20):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
    
center_bank()

    




# команда старт

@bot.message_handler(commands=['start'])
def main(message):
    center_bank()
    global name
    global ban
    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton('Купить Кобякоины', callback_data = 'buy'))
    #bot.send_message(message.chat.id, "Привет братишка, ты находишься в системе обмена криптовалютой посвящённой Кобякову Великому. \nДля работы необходимо зарегестрироваться", reply_markup=markup)
    try:
        name = '@'+message.from_user.username
    except:
        pass
    users = db.getMas('users.txt')
    us = ['@'+str(message.from_user.username), "50000", "15", str(message.chat.id)]

    if db.find_string(users, name) == None and not('@'+str(message.from_user.username) in ban):
        db.addMass(us, "users.txt")
    if not('@'+str(message.from_user.username) in ban):
        bot.send_message(message.chat.id, f'Приветствую, {name}, ты находишься в системе обмена криптовалютой посвящённой Кобякову Великому')
        bot.send_message(message.chat.id, 'Подпишись на t.me/cobya_coin там будут новости проекта')
        bot.send_message(message.chat.id, 'Команда /sell - создание трейда(объявления) о продаже валюты\nКоманда /buy - покупка валюты. Команда выводит список предложений, доступных для покупки\nКоманда /balance - выводит ваш счёт и текущий курс валюты\nКоманда /nft_sell - продать NFT\nКоманда /nft_buy - купить NFT\nКоманда /nft_del - удалить NFT\nКоманда /trans - перевод валюты другому пользователю\nКоманда /maining - создать/улучшить майнинг ферму. При вызове функции полученые деньги уходят на баланс\nКоманда /del - удаление трейда с биржи\nКоманда /info - выводит статистические данные\nКоманда /cb - Центробанк, скупает у вас кобякоины за 70% от текущего курса\nКоманда /cb_coins - Центробанк, скупает у вас кобякоины за 70% от текущего курса\nКоманда /leg - легенды о Кобякове Великом\nКоманда /report - сообщить о проблеме')
    else:
        bot.send_message(message.chat.id, f'Приветствую, {name}, ты был забанен админом, радуйся!')
        bot.send_message(message.chat.id, 'Подпишись на t.me/cobya_coin , там будут новости проекта')

# продажа


@bot.message_handler(commands=['sell'])
def main(message: telebot.types.Message):
    center_bank()  
    bot.send_message(message.chat.id, 'Введи число коинов (целое число)')
    bot.register_next_step_handler(message, coins)


def coins(message):
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    global course
    coin = message.text.strip()
    print(coin)
    try:
        if coin.isdigit():
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+str(message.from_user.username))
            if int(coin) > int(us[user][2]) or int(coin) <= 0:
                bot.send_message(message.chat.id, "На твоём счету недостаточно средств для совершения транзакции, нажми /sell и введи другую сумму")
                tm.sleep(0.2)
                bot.send_message(message.chat.id, f"Твой счёт составляет {us[user][1]} кленовых листьев, {us[user][2]} Кобякоинов")
            else:
                bot.send_message(message.chat.id, f"Введи цену, текущий курс составляет {course}, рекомендуемая цена {course*int(coin)}")
                bot.register_next_step_handler(message, prise, args=coin)
        else:
            bot.send_message(message.chat.id, "Операция отменена")
    except Exception as e:
        bot.send_message(message.chat.id, f"Что-то пошло не так, нажми команду еще раз {e}")
        print('выбор количества коинов на продажу')
        pass

def prise(message, args):
    usern = '@'+ str(message.from_user.username)
    coin = args
    price = message.text.strip()
    print(price)
    try:
        if price.isdigit() and int(price) < 10000:

            if int(price) > 0:
            #users  = db.getMas('users.txt')
                markup = telebot.types.InlineKeyboardMarkup()
                btn1 = telebot.types.InlineKeyboardButton("Разместить трейд", callback_data='bs_sell '+str(coin)+' '+str(price)+' '+str(usern))
                btn2 = telebot.types.InlineKeyboardButton("Продать другу", callback_data='us_sell '+str(coin)+' '+str(price)+' '+str(usern))
                btn3 = telebot.types.InlineKeyboardButton("  Отмена  ", callback_data='otmena '+str(coin)+' '+str(price)+' '+str(usern))
                markup.add(btn1, btn2)
                markup.row(btn3)
                bot.send_message(message.chat.id, "   Выбери способ продажи   ", reply_markup=markup)

        else:
            bot.send_message(message.chat.id, "Операция отменена")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, нажми команду еще раз")
        print('Выбор цены')
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    
    colvo = 0
    data = call.data.split()
    usern = data[3]
    coin = int(data[1])
    price = int(data[2])
    message = call.message
    if str(price).isdigit() and int(price) < 50000:
        try:
            if data[0] == 'bs_sell':
                burse = db.getMas("burse.txt")
            
                for i in burse:
                    if i[0] == usern:
                        print("ass")
                        colvo += 1
                if colvo < 8:
                    db.addMass([usern, coin, price, int(round(tm.time()))], "burse.txt")
                    bot.send_message(message.chat.id, "Ваше объявление опубликовано на бирже")
                else:
                    bot.send_message(message.chat.id, "Хватит рушить бота!")
            elif data[0] == 'us_sell':
                bot.send_message(message.chat.id, "Выберите пользователя")
                us = db.getMas('users.txt')
                out = ''
                for i in range(1, len(us)):
                    out += str(i) + '.  ' + us[i][0] + '\n'
                bot.send_message(message.chat.id, out)
                
                bot.register_next_step_handler(message, choise, arg1=coin, arg2=price, arg3=usern)
            elif data[0] == 'otmena':
                print('otmena')
                bot.send_message(message.chat.id, "Операция отменена")
        except Exception as e:
            bot.send_message(message.chat.id, f"Что-то пошло не так, нажми команду еще раз\n{e}")
            print('Выбор способа продажи')
            pass
    else:
        bot.send_message(message.chat.id, "Операция отменена")
def choise(message, arg1, arg2, arg3):
    try:
        coin = arg1
        price = arg2
        usern = arg3
        ch = message.text.strip()
        us = db.getMas('users.txt')
        tread = [us[int(ch)][0], usern, str(coin), str(price)]
        db.addMass(tread, 'us_b.txt')
        bot.send_message(message.chat.id, "Ваше предложение появится у друга если он захочет купить валюту")
        bot.send_message(us[int(ch)][3], f"Вам поступило личное предложение от @{message.from_user.username}")
    except:
        bot.send_message(message.chat.id, "Говнокод колянчика снова не работает, нажми команду еще раз")
        print('Выбор друга')
        pass 
    




# покупка


@bot.message_handler(commands=['buy'])
def burse_main(message, page=0, messageid=0, messagetxt=''):
    try:
        center_bank()
        usb = db.getMas('us_b.txt')
        burse = db.getMas("burse.txt")
        out = ''
        markup_burse = telebot.types.ReplyKeyboardMarkup()
        markup_burse.add(telebot.types.KeyboardButton("Вперёд"))
        markup_burse.add(telebot.types.KeyboardButton("Назад"))
        if messageid == 0:
            if len(burse) != 1:
                out = update_page(page)
                message_s = bot.send_message(message.chat.id, out)
                messageid=message_s.message_id
                messagetxt = message_s.text+'\n'+'\n'
                
            else:
                bot.send_message(message.chat.id, "Биржа пуста(")
            buyer = db.find_string(usb,'@'+str(message.from_user.username))
            if buyer != None:
                bot.send_message(message.chat.id, f"{usb[buyer][1]} хочет продать вам {usb[buyer][2]} коин за {usb[buyer][3]} к.л.")
            else:
                bot.send_message(message.chat.id, "У вас нет личных предложений)]")
            bot.send_message(message.chat.id, "Для выбора трейда с биржи напишите его номер в чат, для выбора личного трейда (второе сообщение) напишите -1", reply_markup=markup_burse)
        else:
            out = update_page(page)

            if out != messagetxt:
                
                bot.edit_message_text(chat_id=message.chat.id, text=out, message_id=messageid)
            else:
                pass
            

        bot.register_next_step_handler(message, chos, page=page, messageid=messageid, messagetxt=messagetxt)
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так, нажми команду еще раз")
        print(f'Покупка до выбора, {e}')
        pass

def chos(message, messageid, messagetxt, page=0):
    global timer
    global transactions
    global course
    global history
    ch = message.text.strip()
    global center_bank_leaves

    if ch.isdigit() or ch == '-1':
        
        try:
            burse = db.getMas("burse.txt")

            # если я покупатель
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+str(message.from_user.username))
            usb = db.getMas('us_b.txt')
            buyer = db.find_string(us,'@'+str(message.from_user.username))
            ce = db.getMas("center")

            

            if ch != '-1':
                ch = str(int(ch)-1)
                
                if '@'+str(message.from_user.username) != burse[int(ch)][0]:

                    seller = db.find_string(us, burse[int(ch)][0])
                    if seller != None:
                        if int(us[user][1]) < int(burse[int(ch)][2]) or user == None:
                            bot.send_message(message.chat.id, "Транзакция отклонена, недостаточно средств")
                        else:
                            
                            coin = int(us[user][2])+int(burse[int(ch)][1])
                            leave = int(us[user][1])-int(burse[int(ch)][2])
                            
                            sel_coin = int(us[seller][2])-int(burse[int(ch)][1])
                            sel_leave = int(us[seller][1])+int(int(burse[int(ch)][2])*0.9)
                            center_bank_leaves += int(int(burse[int(ch)][2])*0.1)
                            
                            us[user][1] = str(leave)
                            us[user][2] = str(coin)
                            us[seller][1] = str(sel_leave)
                            us[seller][2] = str(sel_coin)
                            
                            ce[0][0] = str(center_bank_leaves)
                            ce[1][0] = str(center_bank_coins)

                            db.wrTo(ce,"center")

                            transactions += 1
                            history.append(int(burse[int(ch)][2])//int(burse[int(ch)][1]))
                            db.addMass([str(int(burse[int(ch)][2])//int(burse[int(ch)][1]))], "history.txt")
                            c = sum_of_last_10_elements(history)
                            
                            course = c//10

                            #infodb.getMas('course')
                            #cr[0][0] = str(course)
                            timer += 1
                            cr = [str(course), str(transactions), str(videocards_course)]
                            db.addMass(cr, 'course')
                            
                            bot.send_message(us[seller][3], f"Ваше объявление было куплено! Покупатель: {us[buyer][0]}")
                            
                            db.wrTo(us, 'users.txt')
                            del burse[int(ch)]
                            db.wrTo(burse, 'burse.txt')

                            bot.send_message(message.chat.id, "Транзакция проведена успешно")
                    else:
                        bot.send_message(message.chat.id, "Что-то пошло не так")

            elif ch == '-1':
                    seller = db.find_string(us, usb[buyer][1])
                    if seller != None:
                        if int(us[user][1]) < int(usb[buyer][3]):
                            bot.send_message(message.chat.id, "Транзакция отклонена, недостаточно средств")
                        else:
                            coin = int(us[user][2])+int(usb[buyer][2])
                            leave = int(us[user][1])-int(usb[buyer][3])

                            #print("a1")

                            sel_coin = int(us[seller][2])-int(usb[buyer][2])
                            sel_leave = int(us[seller][1])+int(int(usb[buyer][3])*0.9)
                            center_bank_leaves += int(int(usb[buyer][3])*0.1)

                            #print("a2")
                            ce[0][0] = str(center_bank_leaves)
                            ce[1][0] = str(center_bank_coins)

                            db.wrTo(ce,"center")

                            us[user][1] = str(leave)
                            us[user][2] = str(coin)
                            us[seller][1] = str(sel_leave)
                            us[seller][2] = str(sel_coin)

                            #print('a3')

                            transactions += 1
                            history.append(int(usb[buyer][3])//int(usb[buyer][2]))
                            db.addMass([str(int(usb[buyer][3])//int(usb[buyer][2]))], "history.txt")
                            c = sum_of_last_10_elements(history)

                            #print('a4')
                            
                            course = c//10
                            #cr = db.getMas('course')
                            #cr[0][0] = str(course)
                            #db.wrTo(cr, 'course')
                            timer += 1
                            cr = [str(course), str(transactions), str(videocards_course)]
                            db.addMass(cr, 'course')

                            bot.send_message(us[seller][3], "Ваше личное предложение было куплено!")

                            db.wrTo(us, 'users.txt')
                            del usb[buyer]
                            db.wrTo(usb, 'us_b.txt')

                        bot.send_message(message.chat.id, "Транзакция проведена успешно")
                    else:
                        bot.send_message(message.chat.id, "Что-то пошло не так")
        except Exception as e:
            bot.send_message(message.chat.id, "Что-то пошло не так, нажми команду еще раз")
            print(f'Покупка, {e}')
            pass
    elif ch == "Вперёд":
        bot.delete_message(message.chat.id, message.id)
        page+=1
        burse_main(message, page, messageid=messageid, messagetxt=messagetxt)
    elif ch =="Назад":
        bot.delete_message(message.chat.id, message.id)
        if page != 0:
            page-=1
            burse_main(message, page, messageid=messageid, messagetxt=messagetxt)
        else:
            #bot.send_message(message.chat.id, "Дальше некуда") 
            
            bot.register_next_step_handler(message, chos, page=page, messageid=messageid, messagetxt=messagetxt)

    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, нажми команду /buy еще раз")







@bot.message_handler(commands=['balance'])
def main(message):
    center_bank()
    global course
    global transactions
    global center_bank_coins
    global center_bank_leaves
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    
    try:
        if user != None:
            if int(us[user][2]) < 0:
                us[user][1] = str(int(us[user][1]) - abs(int(us[user][2]))*course)
                us[user][2] = '0'
                db.wrTo(us, 'users.txt')
           
            
            bot.send_message(message.chat.id, f"На твоём счету {us[user][1]} кленовых листьев, {us[user][2]} Кобякоинов")
            tm.sleep(0.1)
            bot.send_message(message.chat.id,f"Текущий курс Кобякоина составляет {course}")
        else:
            bot.send_message(message.chat.id, "Погоди, я тебя в списке не видел, пройди регистрацию --> /start")


        
    except:
        bot.send_message(message.chat.id, "Что то пошло не так")


@bot.message_handler(commands=['trans'])
def main(message):
    bot.send_message(message.chat.id, "Выберите пользователя")
    us = db.getMas('users.txt')
    out = ''
    for i in range(1, len(us)):
        out += str(i) + '.  ' + us[i][0] + '\n'
    bot.send_message(message.chat.id, out)
            
    bot.register_next_step_handler(message, par)

def par(message):
    global pr
    pr = message.text.strip()
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    print(user)
    if pr.isdigit() and pr!=str(user):
        bot.send_message(message.chat.id, "Введи размер перевода")
        bot.register_next_step_handler(message, val)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так, нажми команду /trans еще раз")

def val(message):
    global sc
    sc = message.text.strip()
    #print(int(sc), int(pr))
    if sc.isdigit():
        markup1 = telebot.types.ReplyKeyboardMarkup()
        bt1 = telebot.types.KeyboardButton("Кленовые листья")
        bt2 = telebot.types.KeyboardButton("Кобякоины")
        markup1.row(bt1)
        markup1.row(bt2)
        bot.send_message(message.chat.id, "   Выбери валюту для перевода (нажмите на кнопку с клевером)   ", reply_markup=markup1)
        bot.register_next_step_handler(message, on_click)
    else:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так, нажми команду /trans еще раз")

def on_click(message):
    global pr
    global sc
    us_l = 0
    us_c = 0
    pr_l = 0
    pr_c = 0
    if message.text == "Кленовые листья":
        try:
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+str(message.from_user.username))
            pr_l = int(us[int(pr)][1]) + int(sc)
            us_l = int(us[user][1]) - int(sc)

            if int(sc) <= int(us[user][1]):
                us[int(pr)][1] = str(pr_l)
                us[user][1] = str(us_l)
                
                bot.send_message(message.chat.id, 'Перевод осуществлён успешно')
                bot.send_message(us[int(pr)][3], 'Вам перевели некоторую сумму, проверьте баланс')
            else:
                bot.send_message(message.chat.id, 'Недостаточно средств для совершения перевода')

            db.wrTo(us, 'users.txt')
        except:
            bot.send_message(message.chat.id, 'Чёт сервера не справляются, попробуй что ли еще')
            print('Перевод кл')
            pass
    elif message.text == "Кобякоины":
        try:
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+str(message.from_user.username))
            pr_c = int(us[int(pr)][2]) + int(sc)
            us_c = int(us[user][2]) - int(sc)
            
            if int(sc) <= int(us[user][2]):
                us[int(pr)][2] = str(pr_c)
                us[user][2] = str(us_c)

                bot.send_message(message.chat.id, 'Перевод осуществлён успешно')
                bot.send_message(us[int(pr)][3], 'Вам перевели некоторую сумму, проверьте баланс')
            else:
                bot.send_message(message.chat.id, 'Недостаточно средств для совершения перевода')
            
            db.wrTo(us, 'users.txt')
        except:
            bot.send_message(message.chat.id, 'Чёт сервера не справляются, попробуй что ли еще')
            print('Перевод коинов')
            pass

@bot.message_handler(commands=['cb'])
def cb(message):
    center_bank()
    bot.send_message(message.chat.id, "Вас приветствует Центробанк, введите сумму обмена (коины)")
    bot.register_next_step_handler(message, center)

def center(message):
    c = ''
    c = message.text.strip()
    global course
    global center_bank_coins
    global center_bank_leaves
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    ce = db.getMas("center")
    try:
        if c.isdigit() and int(us[user][2]) >= int(c) and int(c)*int(round(course*0.7, 0))<center_bank_leaves:
            us[user][1] = int(us[user][1]) + int(c)*int(round(course*0.7, 0))
            us[user][2] = int(us[user][2]) - int(c)
            db.wrTo(us, 'users.txt')
            center_bank_coins += int(c)
            center_bank_leaves -= int(c)*int(round(course*0.7, 0))
            ce[0][0] = str(center_bank_leaves)
            ce[1][0] = str(center_bank_coins)

            howmuch = int(c)*int(round(course*0.7, 0))
            db.wrTo(ce,"center")
            bot.send_message(message.chat.id, f"Обмен произведён успешно ,\n вы получили {howmuch} листьев ")
        else:
            bot.send_message(message.chat.id, "Что-то пошло не так, возможно недостаточно средств")
    except:

        bot.send_message(message.chat.id, 'Чёт сервера не справляются, попробуй что ли еще')
        print('Центробанк')
        pass

@bot.message_handler(commands=['cb_coins'])
def cbf(message):
    bot.send_message(message.chat.id, "Вас приветствует Центробанк, введите сумму обмена (листья)")
    bot.register_next_step_handler(message, centrc)
def centrc(message):
    c = ''
    c = message.text.strip()
    global course
    global center_bank_coins
    global center_bank_leaves
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    ce = db.getMas("center")

    try:
        if c.isdigit() and int(us[user][1]) >= int(c) and int(c)//int(round(course*0.7, 0))<center_bank_coins:
            us[user][2] = int(us[user][2]) + int(c)//int(round(course*0.7, 0))
            us[user][1] = int(us[user][1]) - int(c)
            center_bank_leaves += int(c)
            center_bank_coins -= int(c)//int(round(course*0.7, 0))

            ce[0][0] = str(center_bank_leaves)
            ce[1][0] = str(center_bank_coins)
            howmuch_koins = int(c)//int(round(course*0.7, 0))

            db.wrTo(ce,"center")

            db.wrTo(us, 'users.txt')
            bot.send_message(message.chat.id, f"Обмен произведён успешно,\nВы получили {howmuch_koins} коинов")
        else:
            bot.send_message(message.chat.id, "Что-то пошло не так, возможно недостаточно средств")
    except:

        bot.send_message(message.chat.id, 'Чёт сервера не справляются, попробуй что ли еще')
        print('Центробанк1')
        pass


@bot.message_handler(commands=['mining'])
def min(message):
    global coins_am
    markup2 = telebot.types.ReplyKeyboardMarkup()
    b1 = telebot.types.KeyboardButton("Создать ферму")
    b2 = telebot.types.KeyboardButton("Улучшить ферму")
    b3 = telebot.types.KeyboardButton("Купить видеокарту")
    b4 = telebot.types.KeyboardButton("Выйти")
    markup2.row(b1)
    markup2.add(b2, b3)
    markup2.row(b4)
    mg = db.getMas('mining.txt')

    try:

        if db.find_string(mg, '@'+str(message.from_user.username)) != None:
            a = int(tm.time()//1)-int(mg[db.find_string(mg, '@'+str(message.from_user.username))][3])
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+message.from_user.username)
            mus = db.find_string(mg, '@'+message.from_user.username)
            global course
            global center_bank_coins
            if a//3600*int(mg[mus][2]) <= int(mg[mus][1]):
                pribl = a//3600*int(mg[mus][2])
            else:
                pribl = int(mg[mus][1])

            if pribl != 0 and int(coins_am[0][0])-pribl >= 0:
                
                if pribl < 99:
                    us[user][2] = int(us[user][2]) + pribl
                    coins_am[0][0] = str(int(coins_am[0][0])-pribl)
                    bot.send_message(message.chat.id, f"Ваша ферма принесла вам {pribl} коинов\nСумма налогооблажения составила 0 коинов")
                else:
                    us[user][2] = int(int(us[user][2]) + pribl*0.9)
                    center_bank_coins += int(pribl*0.1)
                    coins_am[0][0] = str(int(coins_am[0][0])-pribl)
                    bot.send_message(message.chat.id, f"Ваша ферма принесла вам {int(pribl*0.9)} коинов\nСумма налогооблажения составила {int(pribl*0.1)} коинов")

                mg[mus][3] = str(int(tm.time()//1))

                db.wrTo(coins_am, 'coins_amount.txt')
                    
                bot.send_message(message.chat.id, f"Выбери действие\nСоздание фермы - 10000 к.л.\nУлучшение фермы - {int(mg[mus][1])*1000} к.л.\n\nТвоя ферма приносит {int(mg[mus][2])} коинов в час", reply_markup=markup2)
                bot.send_message(message.chat.id, f"Рыночная цена видеокарты {course*10000}")

            else:
                bot.send_message(message.chat.id, "Ваша ферма принесла вам 0 коинов")
                bot.send_message(message.chat.id, f"Выбери действие\nСоздание фермы - 10000 к.л.\nУлучшение фермы - {int(mg[mus][1])*1000} к.л.\n\nТвоя ферма приносит {int(mg[mus][2])} коинов в час", reply_markup=markup2)
                bot.send_message(message.chat.id, f"Рыночная цена видеокарты {course*10000}")
            db.wrTo(us, 'users.txt')
            bot.register_next_step_handler(message, on1_click)
        else:
            bot.send_message(message.chat.id, 'Ох зря ты сюда полез...')
            bot.send_message(message.chat.id, 'Создание фермы будет стоить 10000 к.л.', reply_markup=markup2)
            
        bot.register_next_step_handler(message, on1_click)
        db.wrTo(us, 'users.txt')
        db.wrTo(mg, 'mining.txt')
    except:
        bot.send_message(message.chat.id, 'Чёт сервера не справляются, попробуй что ли еще')
        print('Майнинг 1')
        pass


def on1_click(message):
    txt = message.text
    try:
        if txt == "Создать ферму":
            mg = db.getMas('mining.txt')
            if db.find_string(mg, '@'+str(message.from_user.username)) == None:
                us = db.getMas("users.txt")
                user = db.find_string(us, "@"+str(message.from_user.username))
                us[user][1] = str(int(us[user][1]) - 10000)
                db.wrTo(us, 'users.txt')
                db.addMass(['@'+str(message.from_user.username), "10", "1", str(int(tm.time()//1)), "0"], "mining.txt")
                bot.send_message(message.chat.id, "Ферма успешно создана")
            else:
                bot.send_message(message.chat.id, "У тебя уже есть ферма, дуй отсюда")
            bot.register_next_step_handler(message, on1_click)

        elif txt == "Улучшить ферму":
            mg = db.getMas('mining.txt')
            us = db.getMas("users.txt")
            mus = db.find_string(mg, '@'+str(message.from_user.username))
            user = db.find_string(us, "@"+str(message.from_user.username))
            global center_bank_leaves

            if int(us[user][1]) >= int(mg[mus][1])*1000:
                mg[mus][1] = int(mg[mus][1]) + 10
                us[user][1] = int(us[user][1]) - int(mg[mus][1])*1000
                center_bank_leaves += int(mg[mus][1])*1000
                bot.send_message(message.chat.id, f'Ферма улучшена, текущий уровень фермы {mg[mus][1]}')
            else:
                bot.send_message(message.chat.id, 'На твоём счету недостаточно средств')

            db.wrTo(us, 'users.txt')
            db.wrTo(mg, 'mining.txt')
            bot.register_next_step_handler(message, on1_click)

        elif txt == "Купить видеокарту":
            mg = db.getMas('mining.txt')
            us = db.getMas("users.txt")
            mus = db.find_string(mg, '@'+str(message.from_user.username))
            user = db.find_string(us, "@"+str(message.from_user.username))
            global course
            global transactions
            global history

            if int(us[user][1]) >= course*10000:
                mg[mus][2] = int(mg[mus][2]) + 1
                us[user][1] = int(us[user][1]) - course*10000
                center_bank_leaves += course*10000
                bot.send_message(message.chat.id, f'Видеокарта куплена, ферма будет приносить {mg[mus][2]} коинов в час')
                history.append(course*10)
                transactions += 1

                c = sum_of_last_10_elements(history)
                course = c//transactions

                db.addMass([str(course*1000)], "history.txt")
                cr = [str(course), str(transactions), str(videocards_course)]
                db.addMass(cr, 'course')
                
            else:
                bot.send_message(message.chat.id, 'На твоём счету недостаточно средств')
            db.wrTo(us, 'users.txt')
            db.wrTo(mg, 'mining.txt')
            bot.register_next_step_handler(message, on1_click)



    except:
        bot.send_message(message.chat.id, "Чёт сервера не справляются, попробуй что ли еще")
        print('Майнинг 2')
        pass



@bot.message_handler(commands=['del'])
def delet(message):
    burse = db.getMas("burse.txt")
    out = ''
    try:
        for i in range(1, len(burse)):
            out += str(i) + '. ' + burse[i][0] + ' продаёт ' + burse[i][1] + ' коинов за ' + burse[i][2] + ' к.л.' + '\n'
        bot.send_message(message.chat.id, out)
        bot.send_message(message.chat.id, "Введи номер трейда")
        bot.register_next_step_handler(message, del_c)
    except:
        pass
def del_c(message):
    c = message.text.strip()
    burse = db.getMas("burse.txt")
    try:
        if c.isdigit():
            if burse[int(c)][0] == '@'+str(message.from_user.username):
                del burse[int(c)]
                db.wrTo(burse, 'burse.txt')
                bot.send_message(message.chat.id, "Трейд удалён")
            else:
                bot.send_message(message.chat.id, "Ты не можешь удалить чужой трейд")
    except:
        pass
    

@bot.message_handler(commands=['give'])
def secr(message):
    bot.send_message(message.chat.id, "Операция производится...")
    try:
        t = ['@societykolyan' , 200000]
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][1] = int(us[pers][1]) + int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "братишка , ты пожертвовал 200000 листьев админу на чай и получил +1000000 к карме")
        bot.send_message(809500318 , 'бро , тебе пришло 200к от поклонников')
    except:
        bot.send_message(message.chat.id, "ошибка выплаты админу")
        pass
    try:
        t = [f'{"@"+str(message.from_user.username)}' ,-200000]
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][1] = int(us[pers][1]) + int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "средства списаны с вашего баланса")
    except:
        bot.send_message(message.chat.id, "ошибка списания")
        pass

@bot.message_handler(commands=['secret'])
def sec(message):
    bot.send_message(message.chat.id , 'ботик , тут ничего нет')
    for i in range(100):
        bot.send_message(message.chat.id , 'ботик , тут ничего нет')

@bot.message_handler(commands=['info'])
def info(message):
    global course
    global transactions
    global x
    global y
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    usb = db.getMas('us_b.txt')
    burse = db.getMas("burse.txt")
    x = []
    y = []
    out = ''
    score = 0
    try:
        for i, item in enumerate(burse, start=1):
            
            out += str(i) + '. ' + item[0] + ' (<i>' + str(round((tm.time()-int(item[3]))/3600)) + 'ч' +'</i>) <b>продаёт ' + item[1] + ' CBC</b> за <b>' + item[2] + ' к.л.</b>'+ '\n' + '\n'
            score += 1
            if i == len(burse) or score == 5:
                score = 0
                bot.send_message(message.chat.id, out, parse_mode="html")
                out = ''

        buyer = db.find_string(usb,'@'+str(message.from_user.username))
        if buyer != None:
            bot.send_message(message.chat.id, f"{usb[buyer][1]} хочет продать вам {usb[buyer][2]} коин за {usb[buyer][3]} к.л.")
        else:
            bot.send_message(message.chat.id, "У вас нет личных предложений)]")
        

        x_str = db.getCols('course')[1]
        
        for i in x_str:
            x.append(int(i))

        y_str = db.getCols('course')[0]
        
        for i in y_str:
            y.append(int(i))
        print(x, y)

        procent = round(((y[-1]-y[-2])/y[-2])*100, 2)
        if procent > 0:
            bot.send_message(message.chat.id, f"\nТекущий курс Кобякоина составляет\n<b>{course} к.л.</b>        🔼 <b>{procent}%</b>", parse_mode="html")
        else:
            bot.send_message(message.chat.id, f"\nТекущий курс Кобякоина составляет\n<b>{course} к.л.</b>        🔽 <b>{procent}%</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"Общее количество транзакций составляет <b>{transactions+2590}</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"Системное количество транзакций составляет <b>{transactions}</b>", parse_mode="html")

    except Exception as e:
        bot.send_message(message.chat.id, "Ой, что-то пошло не так")
        print('Инфо основа')
        print(e)
        pass
    try:
        plt.clf()
        plt.plot(x, y)
        plt.savefig("coursie.png")
        with open ('./coursie.png', 'rb') as ph:
            bot.send_photo(message.chat.id, ph)
    except:
        bot.send_message(message.chat.id, "Ой, с загрузкой изображения возникли проблемы, подожди и попробуй еще раз")
        print('Инфо плот')
        pass
    #plt.show()
    
    
@bot.message_handler(commands=['admin'])
def adm(message):
    global admins
    global promocodeL
    global promocodeC
    if '@'+str(message.from_user.username) in admins:
        markup5 = telebot.types.ReplyKeyboardMarkup()
        bt1 = telebot.types.KeyboardButton("Забанить пользователя")
        bt2 = telebot.types.KeyboardButton("Выдать кленовые листья")
        bt3 = telebot.types.KeyboardButton("Выдать коины")
        bt4 = telebot.types.KeyboardButton("Объявление")
        bt5 = telebot.types.KeyboardButton("Разбанить пользователя")
        bt6 = telebot.types.KeyboardButton("Сделать админом")
        bt7 = telebot.types.KeyboardButton("Удалить трейд")
        bt8 = telebot.types.KeyboardButton("Просмотреть таблицу пользователей")
        bt9 = telebot.types.KeyboardButton("Админская группа")
        markup5.add(bt1)
        markup5.row(bt6)
        markup5.row(bt9)
        markup5.add(bt5)
        markup5.add(bt2, bt3 , bt8)
        markup5.row(bt7)
        markup5.row(bt4)
        bot.send_message(message.chat.id, "Приветствую админа", reply_markup=markup5)
        bot.send_message(message.chat.id, f"Промокоды на листья {promocodeL}, промокоды на коины {promocodeC}")
        bot.register_next_step_handler(message, admin)
    else:
        bot.send_message(message.chat.id, "Ты не админ")
def admin(message):
    if message.text == "Забанить пользователя":

        bot.send_message(message.chat.id, "Пиши ник пользователя, обязательно начиная с @")
        bot.register_next_step_handler(message, bnd)

    elif message.text == "Разбанить пользователя":
        bot.send_message(message.chat.id, "Пиши ник пользователя, обязательно начиная с @")
        bot.register_next_step_handler(message, rzb)

    elif message.text == "Выдать кленовые листья":

        bot.send_message(message.chat.id, "Введи имя пользователя и сумму перевода в формате:\n@ivan 2000")
        bot.register_next_step_handler(message, mcl)

    elif message.text == "Выдать коины":

        bot.send_message(message.chat.id, "Введи имя пользователя и сумму перевода в формате:\n@ivan 2000")
        bot.register_next_step_handler(message, cbc)

    elif message.text == "Объявление":

        bot.send_message(message.chat.id, "Введите объявление")
        bot.register_next_step_handler(message, alr)

    elif message.text == "Сделать админом":
        bot.send_message(message.chat.id, "Пиши ник пользователя, обязательно начиная с @")
        bot.register_next_step_handler(message, nad)

    elif message.text == "Удалить трейд":
        burse = db.getMas("burse.txt")
        out = ''
        bot.send_message(message.chat.id, "Пиши номер трейда")
        for i in range(1, len(burse)):
            out += str(i) + '. ' + burse[i][0] + ' продаёт ' + burse[i][1] + ' коинов за ' + burse[i][2] + ' к.л.' + '\n'
        bot.send_message(message.chat.id, out)
        bot.register_next_step_handler(message, dtr)
    
    elif message.text == "Просмотреть таблицу пользователей":
        with open ('users.txt', 'rb') as ph:
            bot.send_document(message.chat.id, ph) 

    elif message.text == "Админская группа":
        bot.send_message(message.chat.id, "вот ссылка на группу ===>https://t.me/+XqnYBzMciRg1Y2Iy")


def bnd(message):
    try:
        global ban
        us = db.getMas("users.txt")
        u = message.text.strip()
        ban.append(u)
        del us[db.find_string(us, u)]
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "Пользователь успешно забанен")
        print(ban)
    except:
        pass
def rzb(message):
    global ban
    u = message.text.strip()
    del ban[ban.index(u)]
    bot.send_message(message.chat.id, "Пользователь успешно разбанен")
    print(ban)

def nad(message):
    u = message.text.strip()
    global admins
    admins.append(u)

def mcl(message):
    try:
        text = message.text.strip()
        t = text.split(" ")
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][1] = int(us[pers][1]) + int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "Средства начислены")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так")
        pass
 
def dtr(message):
    try:
        burse = db.getMas("burse.txt")
        c = message.text.strip()
        del burse[int(c)]
        db.wrTo(burse, "burse.txt")
        bot.send_message(message.chat.id, "Трейд удалён")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так")
        pass

def cbc(message):
    try:
        text = message.text.strip()
        t = text.split(" ")
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][2] = int(us[pers][2]) + int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "Средства начислены")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так")
        pass

def alr(message):
    try:
        text = message.text.strip()
        us = db.getMas("users.txt")
        for i in range(1,len(us)):
            bot.send_message(us[i][3], text)
    except:
        pass

#@bot.message_handler(commands=)
@bot.message_handler(commands=promocodeL)
def prml(message):
    try:
        global promocodeL
        us = db.getMas("users.txt")
        user = db.find_string(us, "@"+str(message.from_user.username))
        us[user][1] = str(int(us[user][1])+10000)
        db.wrTo(us, "users.txt")
        promocodeL.remove(message.text.strip()[1:])
        bot.send_message(message.chat.id, "Вам начислено 10000 к.л.")
        s = ''
        for i in range(4):
            s += r.choice(list("qwertyuiop[]asdfghjkl;'zxcvbnm,.1234567890QWERTYUIOPASDFGHJKL:ZXCVBNM<>?@%$&*()_-+="))
        promocodeL.append(s)
        s = ''
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, проверьте что вы зарегестированы")
@bot.message_handler(commands=promocodeC)
def prmc(message):
    try:
        global promocodeC
        us = db.getMas("users.txt")
        user = db.find_string(us, "@"+str(message.from_user.username))
        us[user][2] = str(int(us[user][2])+50)
        db.wrTo(us, "users.txt")
        promocodeC.remove(message.text.strip()[1:])
        bot.send_message(message.chat.id, "Вам начислено 50 коинов")
        s = ''
        for i in range(4):
            s += r.choice(list("qwertyuiop[]asdfghjkl;'zxcvbnm,.1234567890QWERTYUIOPASDFGHJKL:ZXCVBNM<>?@%$&*()_-+="))
        promocodeL.append(s)
        s = ''
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так, проверьте что вы зарегестированы")

@bot.message_handler(commands=['nft_sell'])
def handle_start(message):
    bot.send_message(message.chat.id, "Введи название NFT")
    bot.register_next_step_handler(message, nft_name)

def handle_file(message, nft_n, nft_p):

    try:
        file_info = bot.get_file(message.document.file_id if message.document else message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)

        # Определяем путь и имя файла для сохранения
        file_extension = message.document.file_name.split('.')[-1] if message.document else "jpg"
        file_name = f"{str(message.from_user.username)+str(message.message_id)}.{file_extension}"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(file)

        bot.send_message(message.chat.id, f"Файл сохранен как {file_name}")
        db.addMass(["@"+str(message.from_user.username), nft_n, str(nft_p), file_name],"NFT")
        bot.send_message(message.chat.id, f"NFT успешно размещена на рынке")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

def nft_name(message):
    
    cnsr = True
    text = message.text.strip()
    text1 = text
    for i in cf.substr:
        if i in text1.lower():
            cnsr = False
    if cnsr:
        nft_n = text
        bot.send_message(message.chat.id, "Принято\nВведите цену(коины)")
        bot.register_next_step_handler(message, nft_price, args=nft_n)
    else:
        bot.send_message(message.chat.id, "Ваше название содержит нецензурную лексику, введите цензурное название")
        bot.register_next_step_handler(message, nft_name)

def nft_price(message, args):
    
    text = message.text.strip()
    if text.isdigit():
        if int(text) > 0 and int(text) < 50000:
            nft_p = int(text)
            bot.send_message(message.chat.id, "Хорошо, теперь пришли файл(изображение или документ) который ты хочешь продать")
            bot.register_next_step_handler(message, handle_file, nft_n=args, nft_p = nft_p)
        else:
            bot.send_message(message.chat.id, "Ты не можешь ввести такую цену, введи правильно")
            bot.register_next_step_handler(message, nft_price)
    else:
        bot.send_message(message.chat.id, "Операция отменена")

@bot.message_handler(commands=['nft_buy'])
def nft_buy(message):
    nft = db.getMas("NFT")
    ms = ""
    nom = 1
    if len(nft) != 0:
        for i in nft:
            ms += str(nom) + ". " + i[0] + " продаёт NFT '" + i[1] + "' за " + i[2] + " коинов\n" 
            nom += 1
        bot.send_message(message.chat.id, ms)
        bot.send_message(message.chat.id, "Для просмотра NFT введи его номер")
        bot.register_next_step_handler(message, nft_view)
    else:
        bot.send_message(message.chat.id, "Биржа пуста(")
    

def nft_view(message):
    try:
        c = message.text.strip()
        if c.isdigit():
            nft = db.getMas("NFT")
            if int(c) > 0 and int(c) <= len(nft):
                photo = Image.open(nft[int(c)-1][3]).convert("RGBA")
                photo = photo.resize((photo.width // 6, photo.height // 6))   
                watermark = Image.open("watermark.png").convert("RGBA")
                watermark = watermark.resize((photo.width, photo.height)) 
                photo.paste(watermark, (0, 0), watermark)
                photo.save("wt"+nft[int(c)-1][3], format="png")

                with open ("wt"+nft[int(c)-1][3], 'rb') as ph:
                        bot.send_photo(message.chat.id, ph)

                markup90 = telebot.types.ReplyKeyboardMarkup()
                butt1 = telebot.types.KeyboardButton("Купить NFT")
                butt2 = telebot.types.KeyboardButton("Отмена")
                markup90.row(butt1)
                markup90.row(butt2)
                bot.send_message(message.chat.id, "Выбери действие", reply_markup=markup90)
                bot.register_next_step_handler(message, nft_buym, args=str(int(c)-1))
                
            else:
                bot.send_message(message.chat.id, "Такого NFT не существует, введи номер ещё раз")
                bot.register_next_step_handler(message, nft_view)
                
        else:
            bot.send_message(message.chat.id, "Операция отменена")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        pass
    return c

def nft_buym(message, args):
    c = args
    global transactions
    global history
    global course
    global timer
    text = message.text.strip()
    nft = db.getMas("NFT")
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    seller = db.find_string(us, nft[int(c)][0])
    if text == "Купить NFT":
        try:
            if int(nft[int(c)][2]) < int(us[user][2]):
                if nft[int(c)][0] != "@"+str(message.from_user.username):
                    sel_coin = int(us[seller][2]) + int(nft[int(c)][2])
                    us_coin = int(us[user][2]) - int(nft[int(c)][2])
                    us[seller][2] = sel_coin
                    us[user][2] = us_coin

                    with open (nft[int(c)][3], 'rb') as ph:
                        bot.send_document(message.chat.id, ph) 

                    os.remove(nft[int(c)][3])
                    os.remove("wt"+nft[int(c)][3])
                    
                    db.wrTo(us, "users.txt")
                    
                    bot.send_message(us[seller][3], "Ваша NFT была куплена")
                    transactions += 1
                    history.append(course*int(nft[int(c)][2])*2)
                    course = sum_of_last_10_elements(history)//transactions
                    cr = [str(course), str(transactions), str(videocards_course)]
                    db.addMass(cr, 'course')
                    db.addMass([course*int(nft[int(c)][2])], "history.txt")
                    del nft[int(c)]
                    db.wrTo(nft, "NFT")
                    bot.send_message(message.chat.id, "NFT успешно приобретена")
                else:
                    bot.send_message(message.chat.id, "Нельзя купить свою NFT")
            else:
                bot.send_message(message.chat.id, "Недостаточно средств")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
            pass
    else:
        bot.send_message(message.chat.id, "Операция отменена")

@bot.message_handler(commands=['nft_del'])
def nft_del(message):
    nft = db.getMas("NFT")
    ms = ""
    nom = 1
    if len(nft) != 0:
        for i in nft:
            ms += str(nom) + ". " + i[0] + " продаёт NFT '" + i[1] + "' за " + i[2] + " коинов\n" 
            nom += 1
        bot.send_message(message.chat.id, ms)
        bot.send_message(message.chat.id, "Для удаления NFT введи его номер")
        bot.register_next_step_handler(message, nft_del_view)
    else:
        bot.send_message(message.chat.id, "Биржа пуста(")
    
def nft_del_view(message):
    c = message.text.strip()
    if c.isdigit():
        c = str(int(c)-1)
        nft = db.getMas("NFT")
        us = db.getMas("users.txt")
        user = db.find_string(us, "@"+str(message.from_user.username))
        try:  
            if int(c) >= 0 and int(c) < len(nft):
                if nft[int(c)][0] == us[user][0]:

                    os.remove(nft[int(c)][3])
                    os.remove("wt"+nft[int(c)][3])
                    del nft[int(c)]
                    db.wrTo(us, "users.txt")
                    db.wrTo(nft, "NFT")
                    bot.send_message(message.chat.id, "NFT удалена")
                else:
                    bot.send_message(message.chat.id, "Нельзя удалить не свою NFT")
            else:
                bot.send_message(message.chat.id, "Такой NFT нет(")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка {e}")

@bot.message_handler(commands=['report'])
def report_main(message):
    bot.send_message(message.chat.id, "Опишите проблему")
    bot.register_next_step_handler(message, report_text)

def report_text(message):
    text = message.text.strip()
    bot.send_message(6258402934, f"{message.from_user.username} отправил жалобу:\n{text}") 

@bot.message_handler(commands=['leg'])
def leg(message):
    markup80 = telebot.types.ReplyKeyboardMarkup()
    butt18 = telebot.types.KeyboardButton("Основная трилогия")
    butt19 = telebot.types.KeyboardButton("Легенды 6В")
    butt20 = telebot.types.KeyboardButton("Дополнения")
    markup80.row(butt18)
    markup80.add(butt19, butt20)
    bot.send_message(message.chat.id, "Выберите издание\nОсновная трилогия --- 2000 к.л.\nЛегенды 6В --- 1000 к.л.\nДополнения --- 500 к.л.", reply_markup=markup80)
    bot.register_next_step_handler(message, leg_click)

def leg_click(message):
    global center_bank_leaves
    text = message.text.strip()
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    if text == "Основная трилогия":
        if int(us[user][1]) >= 2000:
            us[user][1] = int(us[user][1]) - 2000
            center_bank_leaves += 2000
            db.wrTo(us, "users.txt")
            with open ("Trilogy.docx", 'rb') as ph:
                bot.send_document(message.chat.id, ph)
    elif text == "Легенды 6В":
        bot.send_message(message.chat.id, "Здесь пока ничего нет, команда Cobya_coin_bot собирает легенды о Кобякове Великом и скоро они сдесь появятся")
    elif text == "Дополнения":
        bot.send_message(message.chat.id, "Здесь пока ничего нет, команда Cobya_coin_bot собирает легенды о Кобякове Великом и скоро они сдесь появятся")


@bot.message_handler(commands=['liders'])
def lid_main(message):
    sp.update()
    s_kl = ''
    s_cb = ''
    for i in range(len(sp.liders_kl)):
        s_kl += str(i+1) + ". " + sp.liders_kl[i] + "\n"
        s_cb += str(i+1) + ". " + sp.liders_cb[i] + "\n"

    bot.send_message(message.chat.id, f"Лидеры по листьям:\n\n{s_kl}")
    bot.send_message(message.chat.id, f"Лидеры по коинам:\n\n{s_cb}")
   

@bot.message_handler(commands=["auc_sell"])
def auc_sell_main(message):
    bot.send_message(message.chat.id, "Введи описание товара")
    bot.register_next_step_handler(message, auc_sell_dis)

def auc_sell_dis(message):
    disc = message.text.strip()
    bot.send_message(message.chat.id, "Введи начальную цену")
    bot.register_next_step_handler(message, auc_sell_price, disc=disc)

def auc_sell_price(message, disc):
    if message.text.strip().isdigit():
        start_price = int(message.text.strip())
        markup456 = telebot.types.ReplyKeyboardMarkup()
        butt41 = telebot.types.KeyboardButton("Загрузить фото")
        butt42 = telebot.types.KeyboardButton("Не прикреплять фото")
        markup456.add(butt41, butt42)
        bot.send_message(message.chat.id, "Прикрепить фото товара?", reply_markup=markup456)
        bot.register_next_step_handler(message, aic_sell_sogl, disc = disc, start_price = start_price)
    else:
        bot.send_message(message.chat.id, "Неправильная цена")
    
def aic_sell_sogl(message, disc, start_price):
    if message.text == "Не прикреплять фото":
        markup500 = telebot.types.ReplyKeyboardMarkup()
        butt51 = telebot.types.KeyboardButton("Соглашаюсь")
        butt52 = telebot.types.KeyboardButton("Отмена")
        markup500.row(butt51)
        markup500.row(butt52)
        bot.send_message(message.chat.id, "Размещая объявление вы несёте полную ответственость за передачу товара, в случае не получения товара покупателем, он имеет право подачи жалобы админу, с последущем ее рассмотрением и вынесением приговора (бан или крупный штраф в обоих валютах)", reply_markup=markup500)
        bot.register_next_step_handler(message, aic_sell_fin, disc = disc, start_price = start_price, file_name = "#@#")
        #db.addMass(["@"+str(message.from_user.username), disc, start_price, "#@#", str(tm.time())], "auction.txt")
    elif message.text == "Загрузить фото":
        bot.send_message(message.chat.id, "Пришли одну фотографию с товаром")
        bot.register_next_step_handler(message, auc_sell_file, disc = disc, start_price = start_price)

def aic_sell_fin(message, disc, start_price, file_name):
    if message.text == "Соглашаюсь":
        db.addMass(["@"+str(message.from_user.username), disc, start_price, file_name, str(int(round(tm.time()))), "@"+str(message.from_user.username)], "auction.txt")
        bot.send_message(message.chat.id, "Аукцион начался!")
    else:
        bot.send_message(message.chat.id, "Операция отменена(")
        
def auc_sell_file(message, disc, start_price):
    file_info = bot.get_file(message.document.file_id if message.document else message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)

        # Определяем путь и имя файла для сохранения
    file_extension = message.document.file_name.split('.')[-1] if message.document else "jpg"
    file_name = f"{str(message.from_user.username)+str(message.message_id)}.{file_extension}"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, 'wb') as new_file:
        new_file.write(file)
    	
    bot.send_message(message.chat.id, "Фото сохранено")
    markup500 = telebot.types.ReplyKeyboardMarkup()
    butt51 = telebot.types.KeyboardButton("Соглашаюсь")
    butt52 = telebot.types.KeyboardButton("Отмена")
    markup500.row(butt51)
    markup500.row(butt52)
    bot.send_message(message.chat.id, "Размещая объявление вы несёте полную ответственость за передачу товара, в случае не получения товара покупателем, он имеет право подачи жалобы админу, с последущем ее рассмотрением и вынесением приговора (бан или крупный штраф в обоих валютах)", reply_markup=markup500)
    bot.register_next_step_handler(message, aic_sell_fin, disc = disc, start_price = start_price, file_name = file_name)


@bot.message_handler(commands=["auc"])
def auc_buy_out(message):
    auc = db.getMas('auction.txt')
    out = ''
    for i in auc:
        out += i[0] + ":\n"+"'" + i[1] + "' \n<b>Цена:</b> " + i[2]
        if i[3] != "#@#":
            out += "   <u>(1 фото)</u> \n\n"
        else: 
            out += "\n\n"
    bot.send_message(message.chat.id, out, parse_mode="html")
    bot.register_next_step_handler(message, auc_buy_vib)

def auc_buy_vib(message):
    auc = db.getMas('auction.txt')
    c = message.text.strip()
    markup777 = telebot.types.ReplyKeyboardMarkup()
    butt71 = telebot.types.KeyboardButton("Предложить цену")
    butt72 = telebot.types.KeyboardButton("Отмена")
    markup777.add(butt71, butt72)
    if c.isdigit():
        vibor = int(c)-1
        if auc[vibor][3] != "#@#":
            with open (auc[vibor][3], 'rb') as ph:
                bot.send_photo(message.chat.id, ph)
        else:
            bot.send_message(message.chat.id, "*Фото отсутствует*")

        bot.send_message(message.chat.id, "Описание: "+auc[vibor][1], reply_markup=markup777)
        bot.register_next_step_handler(message, auc_buy_pred, vib = vibor)
        
    else:
        bot.send_message(message.chat.id, "Напиши НОМЕР аукциона")
        bot.register_next_step_handler(message, auc_buy_vib)

def auc_buy_pred(message, vib):
    if message.text == "Предложить цену":
        bot.send_message(message.chat.id, "Введи цену:")
        bot.register_next_step_handler(message, auc_buy_buy, vib = vib)
    

def auc_buy_buy(message, vib):
    c = message.text.strip()
    if c.isdigit() :
        auc = db.getMas('auction.txt')
        if auc[vib][0] != "@"+str(message.from_user.username):
            if int(c) > int(auc[vib][2]):
                auc[vib][2] = str(c)
                auc[vib][4] = str(int(round(tm.time())))
                auc[vib][5] = "@"+str(message.from_user.username)
                bot.send_message(message.chat.id, "Цена успешно предложена")
                db.wrTo(auc, 'auction.txt')
            else:
                bot.send_message(message.chat.id, f"Цена должна быть выше предидущей, текущая цена: {auc[vib][2]}")
                bot.register_next_step_handler(message, auc_buy_buy, vib = vib)
        else:
            bot.send_message(message.chat.id, "Нельзя предложить самому себе цену")
    else:
        bot.send_message(message.chat.id, "ЦЕНУ!!!! ЭТО ТЕКСТ, А НУЖНА ЦЕНА")
        bot.register_next_step_handler(message, auc_buy_buy, vib = vib)

@bot.message_handler(commands=["auc_cl"])
def auc_cl_main(message):
    auc = db.getMas('auction.txt')
    out = ''
    for i in auc:
        out += i[0] + ":\n"+"'" + i[1] + "' \n<b>Цена:</b> " + i[2]
        if i[3] != "#@#":
            out += "   <u>(1 фото)</u> \n\n"
        else: 
            out += "\n\n"
    bot.send_message(message.chat.id, out, parse_mode="html")
    bot.register_next_step_handler(message, auc_cl_vib)

def auc_cl_vib(message):
    c = message.text.strip()
    if c.isdigit():
        vib = int(c)-1
        auc = db.getMas('auction.txt')
        users = db.getMas('users.txt')
        seller = db.find_string(users, auc[vib][0])
        buyer = db.find_string(users, auc[vib][5])
        if auc[vib][0] == "@"+str(message.from_user.username):
            seller_cb = int(users[seller][2])+int(auc[vib][2])
            buyer_cb = int(users[buyer][2])-int(auc[vib][2])

            users[seller][2] = seller_cb
            users[buyer][2]=buyer_cb

            bot.send_message(users[buyer][3], f"Вы успешно приобрели {auc[vib][1]}")
            bot.send_message(users[seller][3], f"{auc[vib][5]} приобрел ваш товар в аукционе за {auc[vib][2]}")

            del auc[vib]
        else:
            bot.send_message(message.chat.id, "Нельзя завершить чужой аукцион")
        db.wrTo(auc, 'auction.txt')
        db.wrTo(users, 'users.txt')
    else:
        bot.send_message(message.chat.id, "Это не число, операция отменена")

@bot.message_handler(commands=["casino"])
def casino_main(message):
    bot.send_message(message.chat.id, "Добро пожаловать в наше казино")
    markup787 = telebot.types.ReplyKeyboardMarkup()
    butt_cas = telebot.types.KeyboardButton("Правила")
    butt_cas1 = telebot.types.KeyboardButton("Играть")
    markup787.add(butt_cas, butt_cas1)
    bot.send_message(message.chat.id, "Вы можете ознакомиться с правилами, или приступить к игре", reply_markup=markup787)

    bot.register_next_step_handler(message, cas_ch)

def cas_ch(message):
    if message.text == "Правила":
        pass
    
    elif message.text == "Играть":
        markup797 = telebot.types.ReplyKeyboardMarkup()
        butt_cas_v1 = telebot.types.KeyboardButton("Черные")
        butt_cas_v2 = telebot.types.KeyboardButton("Красные")
        butt_cas_v3 = telebot.types.KeyboardButton("Zero")
        butt_cas_v4 = telebot.types.KeyboardButton("Два числа")
        butt_cas_v5 = telebot.types.KeyboardButton("Одно число")
        
        
        markup797.add(butt_cas_v1, butt_cas_v2, butt_cas_v3, butt_cas_v4,  butt_cas_v5)
        bot.send_message(message.chat.id, "Ваши ставки господа", reply_markup=markup797)
        bot.register_next_step_handler(message, stavki, am = 1, stav = [])

def stavki(message, am, stav):
    text = message.text.strip()
    chat_id = message.chat.id
    digits = [0, 5, 25, 12, 28, 14, 20, 16, 11, 34, 19, 22, 17, 24, 1, 26, 7, 27, 18, 29, 9, 32, 8, 30, 6, 31, 15, 2, 13, 4, 21, 3, 23, 7, 33, 10]
    black = [25, 28, 20, 11, 19, 17, 1, 7, 18, 9, 8, 6, 15, 13, 21, 23, 33]
    red = [5, 12, 14, 16, 34, 22, 24, 26, 27, 29, 32, 30, 31, 2, 4, 3, 7, 10]
    if am < 5:
        match text:
            case "Черные" : 
                stav.append('b')
                am+=1
                bot.send_message(chat_id, "Ставка принята")
            case "Красные" : 
                print("r is pres")
                stav.append('r')
                am+=1
                bot.send_message(chat_id, "Ставка принята")
            case "Zero" : 
                stav.append('z')
                am+=1
                bot.send_message(chat_id, "Ставка принята")
            case "Два числа" :
                bot.send_message(message.chat.id, "Введите числа через пробел")
                bot.register_next_step_handler(message, dva_ch, am = am, stav = stav)
                return
            case  "Одно число" :
                bot.send_message(message.chat.id, "Введи число")
                bot.register_next_step_handler(message, odno_ch, am = am, stav = stav)
                return
        print(stav)
        bot.register_next_step_handler(message, stavki, am = am, stav = stav)
    else:
        bot.send_message(chat_id, "Время вышло, ставки приняты")
        roll = r.choice(digits)
        for i in stav:
            if i == 'b':
                if roll in black:
                    pass
            elif i == 'r':
                if roll in red:
                    pass
            elif i == 'z':
                if roll == 0:
                    pass
            else:
                pass
                
        

def dva_ch(message, am, stav):
    text = message.text
    chat_id = message.chat.id
    stav.append(text)
    am += 1
    bot.send_message(chat_id, "Ставка принята")
    bot.register_next_step_handler(message, stavki, am = am, stav = stav)
        
def odno_ch(message, am, stav):
    text = message.text
    chat_id = message.chat.id
    stav.append(text)
    am += 1
    bot.send_message(chat_id, "Ставка принята")
    bot.register_next_step_handler(message, stavki, am = am, stav = stav)        


    
bot.infinity_polling()
#created by Lamba_40 and @sosietykolyan