import telebot
import config as cf
import support as sp
import time as tm
import random as r
import TableLib as db
import os
import threading
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')

bot = telebot.TeleBot(cf.test)

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
am = []
am = db.getMas('coins_amount.txt')
coins_am = int(am[0][0])
cl_am = int(am[0][1])
video_am = int(am[0][2])
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
jackpot = int(db.getMas('course')[len(db.getMas('course'))-1][3])
burse_timer = 0
planka = 5000
torg = True
normal_course = 100
transactions_as_hour = 0
videocards_transactions_as_hour = 0

timer = 0

admins = ["@IL76pd", "@societykolyan", "@unlucky_POvelitel" , '@Dan9kov']
ban = ['@Hv2_0' , '@user1864926' , '@unknown_user63594', '@NEGRA0956']
promocodeL = ["K9x7", "R2g6", "T3d8", "M4h5", "L6y2", "J1p9", "F5a2", "N8z1", "D7b3", "G2s4", "#KamilaChiter"]
promocodeC = ["Q4x8", "P7g3", "R2d6", "S3h8", "M5l4", "L6f2", "K1p9", "J5a2", "F8z1", "N7b3", "D2s4"]


def sum_of_last_10_elements(arr):
    if len(arr) <= 5:
        return sum(arr)
    else:
        return sum(arr[-5:])
    
def median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 0:
        middle1 = sorted_numbers[n//2 - 1]
        middle2 = sorted_numbers[n//2]
        return (middle1 + middle2) / 2
    else:
        return sorted_numbers[n//2]
    
def number_to_emoji(number):
    # Словарь соответствия между цифрами и эмодзи
    emoji_map = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    } 
    # Преобразование числа в строку и подмена каждой цифры на эмодзи
    return ''.join(emoji_map[digit] for digit in str(number))

    
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
                    
                    bot.send_message(users[buyer][3], f"🔔Вы успешно приобрели {auc[i][1]}")
                    bot.send_message(users[seller][3], f"🔔{auc[i][5]} приобрел ваш товар в аукционе за {auc[i][2]}")

                    if auc[i][3] != "#@#":
                        os.remove(auc[i][3])

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
    sp.update()
    try:
        
        global course
        global center_bank_leaves
        global center_bank_coins
        global transactions
        global transactions_as_hour
        global burse_timer
        global planka
        global torg
        global normal_course
        ce = db.getMas("center")
        us = db.getMas("users.txt")
        burse = db.getMas("burse.txt")

        if not(torg) and int(tm.time()) - burse_timer > 900 and burse_timer != 0:
            burse_timer = 0
            torg =True

        if course > planka and burse_timer == 0 and torg:
            torg = False
            burse_timer = int(tm.time())
            course = normal_course
        
        print(torg, burse_timer, course)
        
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

        am = db.getMas('coins_amount.txt')
        am[0][1] = str(cl_am)
        am[0][0] = str(coins_am)
        am[0][2] = str(video_am)
        db.wrTo(am, 'coins_amount.txt')

        cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
        db.addMass(cr, 'course')
        
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
        print("Центробанк функция", e)
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


def mining_update():
    global coins_am
    global cl_am
    global video_am
    am = db.getMas('coins_amount.txt')
    mg = db.getMas('mining.txt')
    us = db.getMas("users.txt")
    new_mg = []
    for item in mg:
        user = db.find_string(us, item[0])
        speed = int(item[2])
        time = int(item[3])
        last = int(item[4])
        
        pribl = speed*0.1*int(round(tm.time()-time, 0)//3600.0)

        if coins_am-int(pribl//1) > 0:
            last += int(pribl//1)
            if user != None:
                us[user][2] = int(us[user][2])+int(pribl//1)
                db.wrTo(us, "users.txt")
                coins_am -= int(pribl//1)
            if round(pribl%1, 2) != 0.0:
                time = int(round(tm.time(), 0)-(round(pribl%1, 2)//speed*0.1))
            else:
                time = int(round(tm.time(), 0))
        else:
            if user != None:
                us[user][2] = int(us[user][2])+int(coins_am)
                db.wrTo(us, "users.txt")
                coins_am = 0

        new_mg.append([item[0], item[1], str(speed), str(time), str(last)])
        am[0][0] = str(coins_am)
        am[0][1] = str(cl_am)
        am[0][2] = str(video_am)

        #print(pribl, last, time, round(pribl%1, 2))
    db.wrTo(am, 'coins_amount.txt')
    db.wrTo(new_mg, 'mining.txt')

def mining_pereod():
    mining_update()
    print("майнинг")

def start_mining():
    N = 3600
    threading.Timer(N, start_mining).start()  # Перезапускаем таймер
    mining_pereod()


def your_periodic_function():
    center_bank()
    print("Эта функция выполняется каждые N секунд")

def start_timer():
    # Указываем количество секунд (N) до следующего вызова
    N = 900
    threading.Timer(N, start_timer).start()  # Перезапускаем таймер
    your_periodic_function()

def active_plus(message, act=1):
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    if user != None:
        us[user][4] = int(us[user][4])+act
    db.wrTo(us, "users.txt")


start_timer()
start_mining()



# команда старт

@bot.message_handler(commands=['start'])
def main(message):
    #center_bank()
    try:
        global ban
        global center_bank_leaves
        global center_bank_coins
        us = db.getMas("users.txt")
        user = db.find_string(us, "@"+str(message.from_user.username))
        user_id = db.find_in("users.txt", str(message.chat.id), 3)
        usn = "@"+str(message.from_user.username)

        ref = db.getMas("referals.txt")
        referral_code = message.text.partition(' ')[2]
        
        new_user_coins = 10
        new_user_leaves = 50000
        

    

        if message.from_user.username == None:
            bot.send_message(message.chat.id, "❌У вас отсутствует имя пользователя, для регистрации в системе оно необходимо")
        else:
            if user == None and user_id == None and not(usn in ban):
                
                if referral_code:
                    if db.find_string(ref, referral_code[1:]):
                        new_user_coins = 100
                        new_user_leaves = 80000
                        ref_user = db.find_string(us, "@"+ref[db.find_string(ref, referral_code[1:])][0].split("_usern_")[1])

                        if ref_user:
                            us[ref_user][1] = int(us[ref_user][1]) + 10000
                            us[ref_user][2] = int(us[ref_user][2]) + 50
                            center_bank_coins -= 50
                            center_bank_leaves -= 10000
                            bot.send_message(int(us[ref_user][3]), "🔔Пользователь перешел по вашей реферальной ссылке\n✅Вам зачислено 10000 к.л и 50 CBC")
                            db.wrTo(us, "users.txt")

                        bot.send_message(message.chat.id, "🎫Переход по реферальной ссылке\nБонус 30000 к.л 90 CBC")
                        del ref[db.find_string(ref, referral_code[1:])]
                        db.wrTo(ref, "referals.txt")
                    else:
                        bot.send_message(message.chat.id, "❌Реферальной ссылки не существует")

                nu = [usn, new_user_leaves, new_user_coins, str(message.chat.id), 1, 0]  
                db.addMass(nu, "users.txt")
                
                bot.send_message(message.chat.id, "✅Пользователь успешно зарегестрирован в системе")
                bot.send_message(message.chat.id, f"🤖Приветствую {usn}, ты находишься в системе обмена псевдокриптовалютой <b>CobyaCoin (CBC)</b>\nНа твой счет начислено <b>{new_user_leaves}</b> кленовых листьев (к.л.) и <b>{new_user_coins}</b> CBC", parse_mode="html")
                bot.send_message(message.chat.id, "В этом боте ты можешь:\n💰Купить валюту - /buy\n💸Продать валюту - /sell\n⛏Создать ферму и майнить CBC - /mining\n💳Просмотреть свой баланс - /balance\n📈Изучить статистику - /info\n🏆Найти себя в таблице лидеров - /liders\n🎰Сыграть в азартную игру - /casino\nИ еще много всякого разного... Начинай торговать!")

            elif user == None and user_id != None and not(usn in ban):
                us[user_id][0] = "@"+str(message.from_user.username)
                db.wrTo(us, "users.txt")
                bot.send_message(message.chat.id, f"✅Имя пользователя изменено на {usn}, счет восстановлен")
                bot.send_message(message.chat.id, f"<b>С возвращением!</b> У вас уже есть счет в системе, проверьте баланс", parse_mode="html")
                
            elif user != None and user_id != None and not(usn in ban):
                bot.send_message(message.chat.id, f"✅С возвращением {usn}, ваш счет в полном порядке")
            elif usn in ban:
                bot.send_message(message.chat.id, f"❌Вы были забанены админом, доступ в систему <b>запрещен</b>", parse_mode="html")
            else:
                bot.send_message(message.chat.id, f"❌Ошибка авторизации, доступ в систему <b>запрещен</b>", parse_mode="html")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка {e}")

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
                bot.send_message(message.chat.id, "❌На твоём счету недостаточно средств для совершения транзакции, нажми /sell и введи другую сумму")
                bot.send_message(message.chat.id, f"Твой счёт составляет {us[user][1]} кленовых листьев, {us[user][2]} Кобякоинов")
            else:
                bot.send_message(message.chat.id, f"Введи цену, текущий курс составляет {course}, рекомендуемая цена {course*int(coin)}")
                bot.register_next_step_handler(message, prise, args=coin)
        else:
            bot.send_message(message.chat.id, "❌Операция отменена, неверный формат данных")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Продажа данные {e}")
        pass

def prise(message, args):
    usern = '@'+ str(message.from_user.username)
    coin = args
    global course
    price = message.text.strip()
    print(price)
    try:
        if price.isdigit() and int(price) < int(coin)*10*course:

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
            bot.send_message(message.chat.id, "❌Операция отменена, неверный формат данных")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Продажа цена {e}")
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    global course
    colvo = 0
    data = call.data.split()
    usern = data[3]
    coin = int(data[1])
    price = int(data[2])
    message = call.message
    if str(price).isdigit() and int(price) < course*10*int(coin):
        try:
            if data[0] == 'bs_sell':
                burse = db.getMas("burse.txt")
            
                for i in burse:
                    if i[0] == usern:
                        print("ass")
                        colvo += 1
                if colvo < 8:
                    db.addMass([usern, coin, price, int(round(tm.time()))], "burse.txt")
                    bot.send_message(message.chat.id, "✅Ваше объявление опубликовано на бирже")
                    active_plus(message)
                else:
                    bot.send_message(message.chat.id, "😡😡😡Хватит рушить бота!")
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
                bot.send_message(message.chat.id, "❌Операция отменена")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
            print(f"Продажа способ {e}")
            pass
    else:
        bot.send_message(message.chat.id, "❌Операция отменена, неверный формат данных")
def choise(message, arg1, arg2, arg3):
    try:
        coin = arg1
        price = arg2
        usern = arg3
        ch = message.text.strip()
        us = db.getMas('users.txt')
        tread = [us[int(ch)][0], usern, str(coin), str(price)]
        db.addMass(tread, 'us_b.txt')
        bot.send_message(message.chat.id, "✅Ваше предложение появится у друга если он захочет купить валюту")
        bot.send_message(us[int(ch)][3], f"🔔Вам поступило личное предложение от @{message.from_user.username}", disable_notification=True)
        active_plus(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Продажа выбор друга {e}")
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
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Покупка вывод биржи {e}")
        pass

def chos(message, messageid, messagetxt, page=0):
    global timer
    global transactions
    global course
    global history
    global torg
    ch = message.text.strip()
    global center_bank_leaves

    if ch.isdigit() or ch == '-1':
        if torg:
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
                                bot.send_message(message.chat.id, "❌Операция отменена, недостаточно средств")
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
                                
                                if course <= 0:
                                    course = 1

                                #infodb.getMas('course')
                                #cr[0][0] = str(course)
                                timer += 1
                                cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
                                db.addMass(cr, 'course')
                                
                                bot.send_message(us[seller][3], f"🔔Ваше объявление было куплено! Покупатель: {us[buyer][0]}", disable_notification=True)
                                
                                db.wrTo(us, 'users.txt')
                                del burse[int(ch)]
                                db.wrTo(burse, 'burse.txt')

                                bot.send_message(message.chat.id, "✅Транзакция проведена успешно")
                                active_plus(message)
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
                                course = c//5
                                
                                if course <= 0:
                                    course = 1
                                #cr = db.getMas('course')
                                #cr[0][0] = str(course)
                                #db.wrTo(cr, 'course')
                                timer += 1
                                cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
                                db.addMass(cr, 'course')

                                bot.send_message(us[seller][3], "🔔Ваше личное предложение было куплено!", disable_notification=True)

                                db.wrTo(us, 'users.txt')
                                del usb[buyer]
                                db.wrTo(usb, 'us_b.txt')

                            bot.send_message(message.chat.id, "Транзакция проведена успешно")
                            active_plus(message)
                        else:
                            bot.send_message(message.chat.id, "Что-то пошло не так")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
                print(f"Покупка {e}")
                pass
        else:
            bot.send_message(message.chat.id, "❌Вы не можете преобрести валюту, так как курс превысил планку")
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
           
            
            bot.send_message(message.chat.id, f"-----  <b>Ваш счет</b> -----\n\n<b>🍁{us[user][1]}</b> <i>к.л</i>\n\n<b>💰{us[user][2]}</b> <i>CBC</i>", parse_mode="html")
            tm.sleep(0.1)
            bot.send_message(message.chat.id,f"Курс CBC составляет {number_to_emoji(course)}")
            active_plus(message)
        else:
            bot.send_message(message.chat.id, "Погоди, я тебя в списке не видел, пройди регистрацию --> /start")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Баланс {e}")


@bot.message_handler(commands=['trans'])
def main(message):
    bot.send_message(message.chat.id, "👥Выберите пользователя")
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
        bt1 = telebot.types.KeyboardButton("🍁Кленовые листья")
        bt2 = telebot.types.KeyboardButton("💰Кобякоины")
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
    if message.text == "🍁Кленовые листья":
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
                active_plus(message)
            else:
                bot.send_message(message.chat.id, 'Недостаточно средств для совершения перевода')

            db.wrTo(us, 'users.txt')
        except Exception as e:
            bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
            print(f"Перевод кл {e}")
            pass
    elif message.text == "💰Кобякоины":
        try:
            us = db.getMas("users.txt")
            user = db.find_string(us, "@"+str(message.from_user.username))
            pr_c = int(us[int(pr)][2]) + int(sc)
            us_c = int(us[user][2]) - int(sc)
            
            if int(sc) <= int(us[user][2]):
                us[int(pr)][2] = str(pr_c)
                us[user][2] = str(us_c)

                bot.send_message(message.chat.id, '✅Перевод осуществлён успешно')
                bot.send_message(us[int(pr)][3], '🔔Вам перевели некоторую сумму, проверьте баланс')
                active_plus(message)
            else:
                bot.send_message(message.chat.id, '❌Недостаточно средств для совершения перевода')
            
            db.wrTo(us, 'users.txt')
        except Exception as e:
            bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
            print(f"Перевод коины {e}")
            pass


@bot.message_handler(commands=['mining'])
def min(message):
    mg = db.getMas("mining.txt")
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    mining_user = db.find_string(mg, "@"+str(message.from_user.username))

    min_markup = telebot.types.ReplyKeyboardMarkup()
    btm1 = telebot.types.KeyboardButton("Создать ферму ⛏")
    btm2 = telebot.types.KeyboardButton("Улучшить ферму 🛠")
    btm3 = telebot.types.KeyboardButton("Купить \nвидеокарту🛍")
    btm4 = telebot.types.KeyboardButton("Продать \nвидеокарту💰")
    btm5 = telebot.types.KeyboardButton("❌Выйти")

    

    if user == None:
        bot.send_message(message.chat.id, "❌Пользователь не зарегестрирован в CobyaCoin\nПожалуйста пройдите регестрацию")
    elif mining_user == None:
        min_markup.row(btm1)
        min_markup.row(btm5)
        bot.send_message(message.chat.id, "❗У тебя нет фермы, можешь создать ее нажав кнопу ниже", reply_markup=min_markup)
        bot.register_next_step_handler(message, min_buttns)
    else:
        min_markup.row(btm3, btm4)
        min_markup.row(btm2)
        min_markup.row(btm5)
        bot.send_message(message.chat.id, "С возвращением!", reply_markup=min_markup)
        
        #начинаем е**ю с данными таблицы --> 0:Имя юзера 1:Уровень(ёмкость фермы) 2:Скорость добычи 3: time 4: С последнего
        min_data = mg[mining_user]
        level = int(min_data[1])
        speed = int(min_data[2])
        time = int(min_data[3])
        last = int(min_data[4])

        bot.send_message(message.chat.id, f"💰С момента предыдущей сессии ферма принесла вам {last} CBC\n{(last)*course} к.л.")
        bot.send_message(message.chat.id, f"Стоимость улучшения фермы {level*1000}\nРыночная стоимость видеокарты {videocards_course}")
        bot.register_next_step_handler(message, min_buttns)
        
def min_buttns(message):
    try:
        global center_bank_leaves
        global videocards_course
        global video_am
        global course
        text = message.text.strip()
        mg = db.getMas("mining.txt")
        mining_user = db.find_string(mg, "@"+str(message.from_user.username))
        us = db.getMas("users.txt")
        user = db.find_string(us, "@"+str(message.from_user.username))
        if mining_user != None:
            min_data = mg[mining_user]
            level = int(min_data[1])
            speed = int(min_data[2])
            time = int(min_data[3])
            last = int(min_data[4])

        match text:
            case "Создать ферму ⛏":
                if user != None:
                    if mining_user == None:
                        if int(us[user][1]) >= 10000:
                            us[user][1] = str(int(us[user][1])-10000)
                            center_bank_leaves += 10000
                            mg.append(["@"+str(message.from_user.username), 1, 1, str(int(round(tm.time(), 0))), 0])
                            bot.send_message(message.chat.id, "✅Ферма успешно создана")
                            db.wrTo(mg, "mining.txt")
                            db.wrTo(us, "users.txt")
                            active_plus(message)
                            bot.register_next_step_handler(message, min_buttns) 
                        else:
                            bot.send_message(message.chat.id, "❌На вашем счету недостаточно средств")
                    else:
                        bot.send_message(message.chat.id, "❌У тебя уже есть ферма, вторую нельзя")
                else:
                    bot.send_message(message.chat.id, "❌Пользователь не зарегестрирован в CobyaCoin\nПожалуйста пройдите регестрацию")

            case "Улучшить ферму 🛠":
                if user != None:
                    if int(us[user][1]) >= level*1000:
                        us[user][1] = str(int(us[user][1])-level*1000)
                        center_bank_leaves += level*1000
                        level+=1
                        min_data[1] = str(level)
                        mg[mining_user] = min_data
                        db.wrTo(mg, "mining.txt")
                        db.wrTo(us, "users.txt")
                        bot.send_message(message.chat.id, f"✅Ферма улучшена, текущий уровень фермы {level}")
                        active_plus(message)
                        bot.register_next_step_handler(message, min_buttns) 
                    else:
                        bot.send_message(message.chat.id, "❌На вашем счету недостаточно средств")
                else:
                    bot.send_message(message.chat.id, "❌Пользователь не зарегестрирован в CobyaCoin\nПожалуйста пройдите регестрацию")

            case "Купить \nвидеокарту🛍":
                if user != None:
                    if speed+1 <= level*10:
                        if int(us[user][1]) >= videocards_course:
                            if video_am-1 >= 0:
                                us[user][1] = str(int(us[user][1])-videocards_course)
                                center_bank_leaves += videocards_course
                                speed += 1
                                video_am -= 1
                                min_data[2] = str(speed)
                                mg[mining_user] = min_data
                                db.wrTo(mg, "mining.txt")
                                db.wrTo(us, "users.txt")
                                videocards_course = r.randint(1, course*10)
                                cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
                                db.addMass(cr, 'course')
                                bot.send_message(message.chat.id, f"✅Видеокарта куплена, количество видеокарт на ферме: {speed}")
                                active_plus(message)
                                bot.register_next_step_handler(message, min_buttns) 
                            else:
                                bot.send_message(message.chat.id, f"❌Операция отменена, на складе не осталось видеокарт")
                        else:
                            bot.send_message(message.chat.id, f"❌На вашем счету недостаточно средств")
                    else:
                        bot.send_message(message.chat.id, f"❌Операция отменена, нет места для новых видеокарт, улучшите ферму")
                else:
                    bot.send_message(message.chat.id, "❌Пользователь не зарегестрирован в CobyaCoin\nПожалуйста пройдите регестрацию") 

            case "Продать \nвидеокарту💰":
                if user != None:
                    if speed > 1:
                        us[user][1] = str(int(us[user][1])+videocards_course)
                        speed -= 1
                        video_am += 1
                        center_bank_leaves -= videocards_course
                        min_data[2] = str(speed)
                        mg[mining_user] = min_data
                        db.wrTo(mg, "mining.txt")
                        db.wrTo(us, "users.txt")
                        bot.send_message(message.chat.id, f"✅Видеокарта продана, количество видеокарт на ферме: {speed}, вы получили {videocards_course}")
                        videocards_course = r.randint(1, course*10)
                        cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
                        db.addMass(cr, 'course')
                        active_plus(message)
                        bot.register_next_step_handler(message, min_buttns) 
                    else:
                        bot.send_message(message.chat.id, f"❌Операция отменена, вы не можете продать последнюю видеокарту")
                    
                else:
                    bot.send_message(message.chat.id, "❌Пользователь не зарегестрирован в CobyaCoin\nПожалуйста пройдите регестрацию") 
            case "❌Выйти":
                bot.send_message(message.chat.id, "❗Осуществлен выход из команды") 
           
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Удаление трейда вывод {e}")
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Удаление трейда обработка {e}")
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Донат 1 {e}")
        pass
    try:
        t = [f'{"@"+str(message.from_user.username)}' ,-200000]
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][1] = int(us[pers][1]) + int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "средства списаны с вашего баланса")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Донат 2 {e}")
        pass

@bot.message_handler(commands=['secret'])
def sec(message):
    bot.send_message(message.chat.id , 'ботик , тут ничего нет')
    for i in range(1):
        bot.send_message(message.chat.id , '🎰')

@bot.message_handler(commands=['info'])
def info(message):
    global course
    global transactions
    global center_bank_leaves
    global center_bank_coins
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
            bot.send_message(message.chat.id, f"\nТекущий курс Кобякоина составляет\n<b>{number_to_emoji(course)} к.л.</b>        🔼 <b>{procent}%</b>", parse_mode="html")
        else:
            bot.send_message(message.chat.id, f"\nТекущий курс Кобякоина составляет\n<b>{number_to_emoji(course)} к.л.</b>        🔽 <b>{procent}%</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"💸Общее количество транзакций составляет <b>{transactions+2590}</b>", parse_mode="html")
        #bot.send_message(message.chat.id, f"Системное количество транзакций составляет <b>{transactions}</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"💰Количество недобытых коинов составляет <b>{coins_am}</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"⛏Рыночная стоимость видеокарты <b>{videocards_course}</b>\n📦Видеокарт на складе: <b>{video_am}</b>", parse_mode="html")
        bot.send_message(message.chat.id, f"🏛<b>Центробанк</b>\n\n🍁к.л. <b>{center_bank_leaves}</b>\n💰CBC <b>{center_bank_coins}</b>", parse_mode="html")
        
        active_plus(message)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Инфо основа {e}")
        print(e)
        pass
    try:
        plt.clf()
        plt.plot(x, y)
        plt.savefig("coursie.png")
        with open ('./coursie.png', 'rb') as ph:
            bot.send_photo(message.chat.id, ph)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Инфо графики {e}")
        pass
    #plt.show()
    
    
@bot.message_handler(commands=['admin'])
def adm(message):
    global admins
    global promocodeL
    global promocodeC
    if '@'+str(message.from_user.username) in admins:
        markup5 = telebot.types.ReplyKeyboardMarkup()
        bt1 = telebot.types.KeyboardButton("🔒Забанить пользователя")
        bt2 = telebot.types.KeyboardButton("🍁Выдать листья")
        bt3 = telebot.types.KeyboardButton("💰Выдать коины")
        bt4 = telebot.types.KeyboardButton("📢Объявление")
        bt5 = telebot.types.KeyboardButton("🔓Разбанить пользователя")
        bt6 = telebot.types.KeyboardButton("💼Сделать админом")
        bt7 = telebot.types.KeyboardButton("❌Удалить трейд")
        bt8 = telebot.types.KeyboardButton("🛠Просмотреть файлы проекта")
        bt9 = telebot.types.KeyboardButton("💬Админская группа")
        markup5.add(bt1, bt5)
        markup5.add(bt2, bt3)
        markup5.row(bt4)
        markup5.row(bt8)
        markup5.row(bt7)
        markup5.row(bt6)
        markup5.row(bt9)
        
        bot.send_message(message.chat.id, "Приветствую админа", reply_markup=markup5)
        bot.send_message(message.chat.id, f"Промокоды на листья {promocodeL}, промокоды на коины {promocodeC}")
        bot.register_next_step_handler(message, admin)
    else:
        bot.send_message(message.chat.id, "Ты не админ")


def admin(message):
    text = message.text.strip()
    match text:
        case "🔒Забанить пользователя":
            bot.send_message(message.chat.id, "Введите имя пользователя:")
            bot.register_next_step_handler(message, adm_ban)

        case "🔓Разбанить пользователя":
            bot.send_message(message.chat.id, "Введите имя пользователя:")
            bot.register_next_step_handler(message, adm_anti_ban)
        
        case "🍁Выдать листья":
            bot.send_message(message.chat.id, "Введите имя пользователя и сумму\n✏<i>@ivan 1000</i>", parse_mode="html")
            bot.register_next_step_handler(message, adm_mpl)

        case "💰Выдать коины":
            bot.send_message(message.chat.id, "Введите имя пользователя и сумму\n✏<i>@ivan 1000</i>", parse_mode="html")
            bot.register_next_step_handler(message, adm_cbc)

        case "📢Объявление":
            bot.send_message(message.chat.id, "Введите объявление:")
            bot.register_next_step_handler(message, adm_alert)

        case "🛠Просмотреть файлы проекта":
            try:
                with open ('users.txt', 'rb') as ph:
                    bot.send_document(message.chat.id, ph) 
            except:
                pass
            try:
                with open ('mining.txt') as mn:
                    bot.send_document(message.chat.id, mn) 
            except:
                pass
            try:
                with open ('history.txt') as hn:
                    bot.send_document(message.chat.id, hn) 
            except:
                pass
            try:
                with open ('auction.txt') as an:
                    bot.send_document(message.chat.id, an) 
            except:
                pass
            try:
                with open ('burse.txt') as bn:
                    bot.send_document(message.chat.id, bn) 
            except:
                pass

        case "❌Удалить трейд":
            burse = db.getMas("burse.txt")
            out = ''
            score = 0
            for i, item in enumerate(burse, start=1):
            
                out += str(i) + '. ' + item[0] + ' (<i>' + str(round((tm.time()-int(item[3]))/3600)) + 'ч' +'</i>) <b>продаёт ' + item[1] + ' CBC</b> за <b>' + item[2] + ' к.л.</b>'+ '\n' + '\n'
                score += 1
                if i == len(burse) or score == 5:
                    score = 0
                    bot.send_message(message.chat.id, out, parse_mode="html")
                    out = ''

        case "💼Сделать админом":
            bot.send_message(message.chat.id, "Введите имя пользователя:")
            bot.register_next_step_handler(message, adm_adm_plus)

        case "💬Админская группа":
            bot.send_message(message.chat.id, "Ссылка на группу ==> https://t.me/+XqnYBzMciRg1Y2Iy")

def adm_ban(message):
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

def adm_anti_ban(message):
    global ban
    u = message.text.strip()
    del ban[ban.index(u)]
    bot.send_message(message.chat.id, "Пользователь успешно разбанен")
    print(ban)

def adm_adm_plus(message):
    u = message.text.strip()
    global admins
    admins.append(u)

def adm_alert(message):
    try:
        text = "🔊"+message.text.strip()
        us = db.getMas("users.txt")
        for i in range(0,len(us)):
            bot.send_message(us[i][3], text)
    except:
        pass

def adm_cbc(message):
    global center_bank_coins
    try:
        text = message.text.strip()
        t = text.split(" ")
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][2] = int(us[pers][2]) + int(t[1])
        center_bank_coins -= int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "Средства начислены")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так")
        pass

def adm_mpl(message):
    global center_bank_leaves
    try:
        text = message.text.strip()
        t = text.split(" ")
        us = db.getMas('users.txt')
        pers = db.find_string(us, t[0])
        us[pers][1] = int(us[pers][1]) + int(t[1])
        center_bank_leaves -= int(t[1])
        db.wrTo(us, "users.txt")
        bot.send_message(message.chat.id, "Средства начислены")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так")
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Промокоды листья {e}")

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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"Промокоды коины {e}")

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
        active_plus(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"НФТ сохранение файла {e}")

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
        bot.send_message(message.chat.id, "❗Ваше название содержит нецензурную лексику, введите цензурное название")
        bot.register_next_step_handler(message, nft_name)

def nft_price(message, args):
    
    text = message.text.strip()
    if text.isdigit():
        if int(text) > 0 and int(text) < 50000:
            nft_p = int(text)
            bot.send_message(message.chat.id, "Хорошо, теперь пришли файл(изображение или документ) который ты хочешь продать")
            bot.register_next_step_handler(message, handle_file, nft_n=args, nft_p = nft_p)
        else:
            bot.send_message(message.chat.id, "❌Ты не можешь ввести такую цену, введи правильно")
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
            bot.send_message(message.chat.id, "❌Операция отменена")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        print(f"НФТ покупка превью {e}")
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
            if int(nft[int(c)][2]) <= int(us[user][2]):
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
                    
                    bot.send_message(us[seller][3], "🔔Ваша NFT была куплена", disable_notification=True)
                    transactions += 1
                    history.append(course*int(nft[int(c)][2])*2)
                    course = sum_of_last_10_elements(history)//transactions
                    cr = [str(course), str(transactions), str(videocards_course), str(jackpot)]
                    db.addMass(cr, 'course')
                    db.addMass([course*int(nft[int(c)][2])], "history.txt")
                    del nft[int(c)]
                    db.wrTo(nft, "NFT")
                    bot.send_message(message.chat.id, "✅NFT успешно приобретена")
                    active_plus(message)
                else:
                    bot.send_message(message.chat.id, "❌Нельзя купить свою NFT")
            else:
                bot.send_message(message.chat.id, "❌Недостаточно средств")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
            print(f"НФТ покупка {e}")
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
            bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
            print(f"НФТ удаление {e}")

@bot.message_handler(commands=['report'])
def report_main(message):
    bot.send_message(message.chat.id, "Опишите проблему")
    bot.register_next_step_handler(message, report_text)

def report_text(message):
    text = message.text.strip()
    bot.send_message(6258402934, f"@{message.from_user.username} отправил жалобу:\n{text}") 
    bot.send_message(809500318, f"@{message.from_user.username} отправил жалобу:\n{text}")

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
            active_plus(message)
    elif text == "Легенды 6В":
        bot.send_message(message.chat.id, "Здесь пока ничего нет, команда Cobya_coin_bot собирает легенды о Кобякове Великом и скоро они сдесь появятся")
    elif text == "Дополнения":
        bot.send_message(message.chat.id, "Здесь пока ничего нет, команда Cobya_coin_bot собирает легенды о Кобякове Великом и скоро они сдесь появятся")


@bot.message_handler(commands=['liders'])
def lid_main(message):
    sp.update()
    s_kl = ''
    s_cb = ''
    s_at = ''
    s_cs = ''
    for i in range(len(sp.liders_kl)):
        if (i+1 == 1):
            s_kl += str(i+1) + ". " + sp.liders_kl[i] + "🥇" + "\n"
            s_cb += str(i+1) + ". " + sp.liders_cb[i] + "🥇" + "\n"
            s_at += str(i+1) + ". " + sp.liders_act[i] + "🥇" + "\n"
            s_cs += str(i+1) + ". " + sp.liders_cas[i] + "🥇" + "\n"
        elif (i+1 == 2):
            s_kl += str(i+1) + ". " + sp.liders_kl[i] + "🥈" + "\n"
            s_cb += str(i+1) + ". " + sp.liders_cb[i] + "🥈" + "\n"
            s_at += str(i+1) + ". " + sp.liders_act[i] + "🥈" + "\n"
            s_cs += str(i+1) + ". " + sp.liders_cas[i] + "🥈" + "\n"
        elif (i+1 == 3):
            s_kl += str(i+1) + ". " + sp.liders_kl[i] + "🥉" + "\n"
            s_cb += str(i+1) + ". " + sp.liders_cb[i] + "🥉" + "\n"
            s_at += str(i+1) + ". " + sp.liders_act[i] + "🥉" + "\n"
            s_cs += str(i+1) + ". " + sp.liders_cas[i] + "🥉" + "\n"
        else:
            s_kl += str(i+1) + ". " + sp.liders_kl[i] + "\n"
            s_cb += str(i+1) + ". " + sp.liders_cb[i] + "\n"
            s_at += str(i+1) + ". " + sp.liders_act[i] + "\n"
            s_cs += str(i+1) + ". " + sp.liders_cas[i] + "\n"

    bot.send_message(message.chat.id, f"🍁Лидеры по <b>листьям:</b>\n\n{s_kl}", parse_mode="html")
    bot.send_message(message.chat.id, f"💰Лидеры по <b>коинам:</b>\n\n{s_cb}", parse_mode="html")
    bot.send_message(message.chat.id, f"📈Лидеры по <b>активности:</b>\n\n{s_at}", parse_mode="html")
    bot.send_message(message.chat.id, f"🎰Лидеры по <b>казино:</b>\n\n{s_cs}", parse_mode="html")
   

@bot.message_handler(commands=["auc_sell"])
def auc_sell_main(message):
    bot.send_message(message.chat.id, "Введи описание товара")
    bot.register_next_step_handler(message, auc_sell_dis)

def auc_sell_dis(message):
    disc = message.text.strip()
    bot.send_message(message.chat.id, "Введи начальную цену")
    bot.register_next_step_handler(message, auc_sell_price, disc=disc)

def auc_sell_price(message, disc):
    try:
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

    
def aic_sell_sogl(message, disc, start_price):
    try:
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

def aic_sell_fin(message, disc, start_price, file_name):
    try:
        if message.text == "Соглашаюсь":
            db.addMass(["@"+str(message.from_user.username), disc, start_price, file_name, str(int(round(tm.time()))), "@"+str(message.from_user.username)], "auction.txt")
            bot.send_message(message.chat.id, "Аукцион начался!")
            active_plus(message)
        else:
            bot.send_message(message.chat.id, "Операция отменена(")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
        
def auc_sell_file(message, disc, start_price):
    try:
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")


@bot.message_handler(commands=["auc"])
def auc_buy_out(message):
    try:
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

def auc_buy_vib(message):
    try:
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
            #bot.register_next_step_handler(message, auc_buy_vib)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

def auc_buy_pred(message, vib):
    try:
        if message.text == "Предложить цену":
            bot.send_message(message.chat.id, "Введи цену:")
            bot.register_next_step_handler(message, auc_buy_buy, vib = vib)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")
    

def auc_buy_buy(message, vib):
    try:
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
                    active_plus(message)
                else:
                    bot.send_message(message.chat.id, f"Цена должна быть выше предидущей, текущая цена: {auc[vib][2]}")
                    bot.register_next_step_handler(message, auc_buy_buy, vib = vib)
            else:
                bot.send_message(message.chat.id, "Нельзя предложить самому себе цену")
        else:
            bot.send_message(message.chat.id, "ЦЕНУ!!!! ЭТО ТЕКСТ, А НУЖНА ЦЕНА")
            bot.register_next_step_handler(message, auc_buy_buy, vib = vib)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

@bot.message_handler(commands=["auc_cl"])
def auc_cl_main(message):
    try:
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
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")

def auc_cl_vib(message):
    try:
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

                bot.send_message(users[buyer][3], f"🔔Вы успешно приобрели {auc[vib][1]}")
                bot.send_message(users[seller][3], f"🔔{auc[vib][5]} приобрел ваш товар в аукционе за {auc[vib][2]}")
                if auc[vib][3] != "#@#":
                    os.remove(auc[vib][3])

                active_plus(message)

                del auc[vib]
            else:
                bot.send_message(message.chat.id, "Нельзя завершить чужой аукцион")
            db.wrTo(auc, 'auction.txt')
            db.wrTo(users, 'users.txt')
        else:
            bot.send_message(message.chat.id, "Это не число, операция отменена")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")


@bot.message_handler(commands=["casino"])
def casino_main(message):
    bot.send_message(message.chat.id, "🤖Добро пожаловать в наше казино")
    markup787 = telebot.types.ReplyKeyboardMarkup()
    butt_cas = telebot.types.KeyboardButton("Однорукий бандит🎰")
    butt_cas1 = telebot.types.KeyboardButton("Цветовое колесо🎨")
    markup787.add(butt_cas, butt_cas1)
    bot.send_message(message.chat.id, "Выбирайте игру:", reply_markup=markup787)

    bot.register_next_step_handler(message, cas_ch)

def cas_ch(message):
    global jackpot
    text = message.text.strip()
    match text:
        case "Однорукий бандит🎰":
            markup707 = telebot.types.ReplyKeyboardMarkup()
            butt_cas2 = telebot.types.KeyboardButton("10")
            butt_cas3 = telebot.types.KeyboardButton("50")
            butt_cas4 = telebot.types.KeyboardButton("100")
            butt_cas5 = telebot.types.KeyboardButton("❌Выйти")
            markup707.row(butt_cas2); markup707.row(butt_cas3); markup707.row(butt_cas4); markup707.row(butt_cas5) 
            bot.send_message(message.chat.id, "<b>Сделайте ставку (к.л.)</b> \n\n📌<i>Вы можете ввести свою ставку вручную</i>", parse_mode="html", reply_markup=markup707)
            bot.send_message(message.chat.id, "Комбинации:\n🍁🍁🍁 - 1x\n🍒🍒🍒 - 5x\n🥕🥕🥕 - 10x\n💎💎💎 - 50x\n💯💯💯 - 100x\n\n🥕🥕🍒 - 25x\n💎🍁💎 - 65x\n🍒🥕🍒 - 69x\n💯💯🍒 - 70x\n💯💎🍁 - 80x")
            bot.send_message(message.chat.id, f"Джекпот составляет <b>{jackpot}</b>🍁", parse_mode="html")
            bot.register_next_step_handler(message, cas_game_bandit)
        case "Цветовое колесо🎨":
            bot.send_message(message.chat.id, "На данный момент эта игра недоступна( <b>CobyaCoin Team</b> уже работают над этим", parse_mode="html")
def cas_game_bandit(message):
    global center_bank_leaves
    global jackpot

    text = message.text.strip()
    us = db.getMas("users.txt")
    user = db.find_string(us, "@"+str(message.from_user.username))
    string = "⬜⬜⬜"
    string2 = list(string)
    win = 0
    try:
        if text.isdigit():
            stavka = int(text)
            if int(us[user][1]) > stavka:
                bot.send_message(message.chat.id, "Вращаем барабан...")
                b_mes = bot.send_message(message.chat.id, string)
                r.seed(b_mes.id)
                for i in range(0, 3):
                    for j in range(5):
                        string2 = list(string)
                        string2[i] = r.choice(["🍒", "🍒","🍒","🍒","🥕","🥕","🥕", "💎","💎", "🍁","🍁","🍁","🍁","🍁", "💯", "💯"])
                        if ''.join(string2) != string:
                            string = ''.join(string2)
                            bot.edit_message_text(text=string, message_id=b_mes.id, chat_id=message.chat.id)
                            tm.sleep(0.2)
                    
                
                win = stavka*(-1)
                match string:
                    case "🍒🍒🍒":
                        win = stavka*5
                    case "🥕🥕🥕":
                        win = stavka*10
                    case "💎💎💎":
                        win = stavka*50
                    case "🍁🍁🍁":
                        win = stavka
                    case "💯💯💯":
                        win = jackpot+stavka
                        jackpot = 10000
                        center_bank_leaves-=10000
                    case "🥕🥕🍒":
                        win = stavka*25
                    case "💎🍁💎":
                        win = stavka*65
                    case "🍒🥕🍒":
                        win = stavka*69
                    case "💯💯🍒":
                        win = stavka*70
                    case "💯💎🍁":
                        win = stavka*80
                    
                if win < 0:
                    jackpot+=(win*(-1)//2)
                    center_bank_leaves+=(win*(-1)//2)
                else:
                    center_bank_leaves+=(win*(-1))

                bot.send_message(message.chat.id, f"Поздравляю! Ваш выигрыш составил <b>{win}</b>", parse_mode="html")
                bot.send_message(message.chat.id, f"Джекпот составляет <b>{jackpot}</b>🍁", parse_mode="html")
                us[user][1] = str(int(us[user][1])+win)
                if int(us[user][5]) < win:
                    us[user][5] = win
                
                
                db.wrTo(us, 'users.txt')
                active_plus(message)
                bot.register_next_step_handler(message, cas_game_bandit)
            else:
                bot.send_message(message.chat.id, "❌Недостаточно денег на балансе")
        elif text == "❌Выйти": bot.send_message(message.chat.id, "✅Заходите ещё!")
        else:
            bot.send_message(message.chat.id, "❌Неверный формат данных")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌Произошла ошибка: {e}")


@bot.message_handler(commands=["account", "me"])
def me_main(message):
    mg = db.getMas("mining.txt")
    us = db.getMas("users.txt")
    usn = "@"+str(message.from_user.username)
    user = db.find_string(us, "@"+str(message.from_user.username))
    mining_user = db.find_string(mg, "@"+str(message.from_user.username))
    if user != None:
        bot.send_message(message.chat.id, f"👤Имя пользователя: {usn}")
        bot.send_message(message.chat.id, f"🏛Баланс:\n{us[user][1]}🍁к.л.\n{us[user][2]}💰CBC")
        bot.send_message(message.chat.id, f"📊Очки активности:\n{us[user][4]}")
        if mining_user != None:
            bot.send_message(message.chat.id, f"⛏Майнинг:\nУровень: {mg[mining_user][1]}\nВидеокарт: {mg[mining_user][2]}")

        markup709 = telebot.types.ReplyKeyboardMarkup()
        butt_cas2 = telebot.types.KeyboardButton("🔗Создать реферальную ссылку")
        butt_cas3 = telebot.types.KeyboardButton("⚙Настройки аккаунта")
        butt_cas4 = telebot.types.KeyboardButton("❌Выйти")
        markup709.row(butt_cas2); markup709.row(butt_cas3); markup709.row(butt_cas4)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup709)
        bot.register_next_step_handler(message, me_butt)
def me_butt(message):
    text = message.text.strip()
    match text:
        case "🔗Создать реферальную ссылку":
            string = 'L'
            for i in range(0, 8):
                string = string+r.choice(list("1234567890qwertyuiopasdfghjklzxcvbnm"))
            string = string + "_usern_" + message.from_user.username
            db.addMass([string[1:], "10000", "50"], "referals.txt")
            ref = "http://t.me/Cobya3bot?start=" + string
            bot.send_message(message.chat.id, f"🔗Ваша реферальная ссылка: \n{ref}")
        case "❌Выйти":
            bot.send_message(message.chat.id, "✅Заходите еще!")
        case "⚙Настройки аккаунта":
            bot.send_message(message.chat.id, "Coming soon...")

bot.infinity_polling()
#created by Lamba_40 and @sosietykolyan