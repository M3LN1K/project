import telebot
import config
from telebot import types
import os, signal, pickle, sys

# сам бот
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sent = bot.send_message(message.chat.id, "Здравствуйте, как я могу к вам обращаться?")
    bot.register_next_step_handler(sent, Hello)




@bot.message_handler(content_types=['text'])
def Hello(message):
    name = bot.send_message(message.chat.id, 'Здравствуйте, {name}. Позвольте вам помочь, что вы хотели бы узнать?'. format(name=message.text))
    bot.register_next_step_handler(name, callback_inline)
    doc = open('file.txt', 'a')
    doc.write("Имя заказчика - {imia}\n".format(imia=message.text))
    doc.close()

    markup = types.InlineKeyboardMarkup(row_width=4)
    but_1 =types.InlineKeyboardButton("Указать критерии для поиска", callback_data="criteria")
    but_2 =types.InlineKeyboardButton("Платная подписка", callback_data="subscription")
    but_3 =types.InlineKeyboardButton("Возможности бота", callback_data="opportunities")
    but_4 =types.InlineKeyboardButton("Информация о нас", callback_data="info")
    but_5 =types.InlineKeyboardButton("Пока", callback_data="Poka")
    markup.add(but_1, but_2)
    markup.add(but_3, but_4)
    markup.add(but_5)

    
def choice(message):
    uslugi = bot.send_message(message.chat.id, 'you select: '. format(name=message.text), reply_markup=markup)
    bot.register_next_step_handler(uslugi, callback_inline)
    doc = open('file.txt', 'a')
    doc.write("usluga: %s\n".format(uslugi=message.text))
    doc.close()


'''def telephon(message):

	nomer = bot.send_message(message.from_user.id, 'Оставьте ваш контактный номер, что бы наш менеджер смог связаться с вами.')
	bot.register_next_step_handler(nomer, application)
	doc = open('file.txt', 'a')
	doc.write("Услуга - {uslugi}\n".format(uslugi=message.text))

def mail(message):

	mail =  bot.send_message(message.from_user.id, 'Оставьте вашу почту, что бы наш менеджер смог связаться с вами.')
	bot.register_next_step_handler(mail, poka)
	doc = open('file.txt', 'a')
	doc.write("E-mail - {mail}\n".format(uslugi=message.text))

def poka(message):
    bot.send_message(message.from_user.id, 'Спасибо за обращение. Мы сяжемся с вами в ближайшее время.')
    doc = open('file.txt', 'a')
    doc.write("Телефон - {telephon}\n".format(telephon=message.text))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)'''

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'criteria':
		
				markup = telebot.types.InlineKeyboardMarkup(row_width=4)
				but_1 =types.InlineKeyboardButton("Указать ценовой диапозон", callback_data="price")
				but_2 =types.InlineKeyboardButton("Телефон", callback_data="telephon")
				but_3 =types.InlineKeyboardButton("E-mail", callback_data="e-mail")
				but_4 =types.InlineKeyboardButton("Предпочтительные марки авто", callback_data="stamp")
				markup.add(but_1, but_2)
				markup.add(but_3, but_4)
				application = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
					text="",
						reply_markup=markup )
				bot.register_next_step_handler(application, FIO, telephon, mail, poka)

			if call.data == 'price':
				def FIO(message):
					fio = bot.send_message(call.message.from_user.id, 'Укажите имя, фамилию и отчество:')
					bot.register_next_step_handler(fio, application)
					
			if call.data == 'telephon':
				def telephon(message):
					nomer = bot.send_message(call.message.from_user.id, 'Оставьте ваш контактный номер, что бы наш менеджер смог связаться с вами.')
					bot.register_next_step_handler(nomer, application)
					doc = open('file.txt', 'a')
					doc.write("ФИО - {FIO}\n".format(fio=message.text))
					doc.close()
			if call.data == 'e-mail':
				def mail(message):
					mail =  bot.send_message(call.message.from_user.id, 'Оставьте вашу почту, что бы наш менеджер смог связаться с вами.')
					bot.register_next_step_handler(mail, stamp)
					doc = open('file.txt', 'a')
					doc.write("Телефон - str({telephon}\n)".format(telephon=message.text))
					doc.close()
			if call.data == 'stamp':
				def stamp(message):
					stamp = bot.send_message(call.message.from_user.id, 'Пожалуйска укажите какие марки автомобилей вы хотели бы, что бы мы нашли?')
					bot.register_next_step_handler(stamp, poka)
					doc = open('file.txt', 'a')
					doc.write("E-mail - {mail}\n".format(mail=message.text))
					doc.close()
					
		
				def poka(message):
					bot.send_message(message.from_user.id, 'Спасибо за обращение. Мы сяжемся с вами в ближайшее время.')
					doc = open('file.txt', 'a')
					doc.write("stamp - {stamp}\n".format(stamp=message.text))
					doc.close()
			if call.data == 'Poka':
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
					text='Надеемся, что вы нашли то, что искали. Досвидания!')
	except Exception as e:
		print(str(e))

bot.polling(none_stop=True)