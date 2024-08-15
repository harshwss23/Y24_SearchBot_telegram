import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import *
import pandas as pd
import face_recognition
import numpy as np
from fpdf import FPDF

created_vectors = np.zeros((1216, 128))

#Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# data=pd.read_csv('new.csv')
sorted_data = pd.read_csv('sorted_data.csv')

TOKEN = ""

def vectorize():
    output = pd.read_csv('Image_encodings_for_Y24.csv')
    for i in range(1,1216):
        for j in range(0,128):
            try:
                created_vectors[i][j] = output[f'{i+240000}'][j]
            except:
                created_vectors[i][j] = 0



#Start and make the buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define inline buttons

    # Define reply buttons
    reply_keyboard = [
        ['Search By Name'], ['Search by Roll Number'],
        ['Search Wing'], ['Search by Image']
    ]

    # Create the reply markup
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hi I am Bot which has scraped data from pclubs Students search\nInstructions to use me\n1. Type in a wings name in Capitals and no hyphens, to search for it.Eg. for C-1 search 'C1', this would give all people living in C1 sorted by their room numbers. For wing names common in Hall 13 and 4(eg E1) Both boys and gals names are shown\n2. To Search by name, type in any part of the name you know(but knowing only 1 letter of the name wont show u anything, u need to know atleast 2 contiguous letters to briing up results), Eg. typing 'arsh' would bring up Harsh too\n3. To Search by Roll Number just type in the full roll number(pretty self explanatory, but if u want to search 240899 just type in 240899)\n4. To run a facial scan with the picture uploaded in Students Search, just send the picture. The bot tests the picture given by u with the faces of all students in Y24(The picture used for testing is the picture uploaded to Students Search via ICS, if u have updated ur profile picture the bot still uses your old photo for running the test). For better results upload only 1 face in the picture with the face facing towards camera. Ideally the picture should be in the format of students Search pictures(40~50% of photo covered with face)\nIf there is a 50% match between the images, this bot sends their photo and name and at the end the bot sends the names which had maximim matching features\n5. To read all of these instructions again, just type in /help\n\nThe accuracy of this bot is low, so please dont be upset with poor results\n\nFor any bugs u encounter, please write to @WW_II_NZ_supporter")
    if (update.message.chat_id != Sakshams_id):
        await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} started the bot')
        await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} started the bot')


async def Help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if (update.message.chat_id != Sakshams_id):
        await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} needs help')
    await update.message.reply_text("1. Type in a wings name in Capitals and no hyphens, to search for it.Eg. for C-1 search 'C1', this would give all people living in C1 sorted by their room numbers. For wing names common in Hall 13 and 4(eg E1) Both boys and gals names are shown\n2. To Search by name, type in any part of the name you know(but knowing only 1 letter of the name wont show u anything, u need to know atleast 2 contiguous letters to briing up results), Eg. typing 'arsh' would bring up Harsh too\n3. To Search by Roll Number just type in the full roll number(pretty self explanatory, but if u want to search 230844 just type in 230844)\n4. To run a facial scan with the picture uploaded in Students Search, just send the picture. The bot tests the picture given by u with the faces of all students in Y23(The picture used for testing is the picture uploaded to Students Search via ICS, if u have updated ur profile picture the bot still uses your old photo for running the test). For better results upload only 1 face in the picture with the face facing towards camera. Ideally the picture should be in the format of students Search pictures(40~50% of photo covered with face)\nIf there is a 50% match between the images, this bot sends their photo and name and at the end the bot sends the names which had maximim matching features\n\nThe accuracy of this bot is really low, so dont be upset with poor results")
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Website')

async def handle_wing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pdf=FPDF()
    A4_WIDTH = 210
    A4_HEIGHT = 297
    desired_width = A4_WIDTH * 0.7
    desired_height = A4_HEIGHT * 0.7
    pdf.set_font("Arial", size=40)

    names = ""
    namesList = []
    input = update.message.text
    input = input[:len(input)-1] + '-' + input[-1]
    for i in range(0,1215):
        try:
            if(input == sorted_data['Address'][i][:len(input)]):
                names = sorted_data['Address'][i]  + ' : '+ sorted_data['Names'][i] + "\n"
                namesList.append(names)
                pdf.add_page()
                img_path=f"images/{i+240001}.jpg"
                pdf.image(img_path, x=(A4_WIDTH - desired_width) / 2, y=(A4_HEIGHT - desired_height) / 2, w=desired_width, h=desired_height)
                pdf.text((A4_WIDTH - desired_width) / 2,(A4_HEIGHT - desired_height) / 2,sorted_data['Names'][i])
        except:
            continue
    namesList.sort()
    names = ""
    pdf.output("Photoswing.pdf")
    for i in range(0, len(namesList)):
        names = names + namesList[i]
    # await update.message.reply_text(names)
    await context.bot.send_document(chat_id=update.message.chat_id,document="Photoswing.pdf",caption="")
    await context.bot.send_message(chat_id=update.message.chat_id, text=names)
    if (update.message.chat_id != Sakshams_id):
        await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} is serching for wings {input}')
        await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} is serching for wings {input}')


async def handle_name(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
        input = update.message.text
        if(input == "Search By Name"):
            await update.message.reply_text("Enter any part of the name you know")
#            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} pressed a button')
            return
        if(input == "Search by Roll Number"):
            await update.message.reply_text("Enter full Roll Number")
#            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} pressed a button')
            return
        if(input == "Search Wing"):
            await update.message.reply_text("Enter the Wing in Capital with no hyphens")
#            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} pressed a button')
            return
        if(input == "Search by Image"):
            await update.message.reply_text("Upload the Image with face Zoomed in preferably with face facing Towards Camera(Feature not working now)")
#            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} pressed a button')
            return
        input = input.upper()
        if(input == 'HI' or input == 'HELLO'):
            await update.message.reply_text("Hi, I am a bot, I do the following works")
            return
        rollnumberslist = []
        for i in range(0,1215):
            if input in sorted_data['Names'][i].upper():
               rollnumberslist.append((sorted_data['Roll Numbers'][i], i))
        # rollnumberslist.sort()
        emptystr = ""
        if(len(rollnumberslist) > 0):
            for i in range(0, len(rollnumberslist)):
                emptystr = emptystr + sorted_data['Names'][rollnumberslist[i][1]] + " : " + str(sorted_data['Roll Numbers'][rollnumberslist[i][1]]) +  "\n"
            await update.message.reply_text(emptystr)

        if(len(rollnumberslist) == 0):
            await update.message.reply_text("No Matches Found")

        if(update.message.chat_id != Sakshams_id):
            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} searched for names, {input}')
            await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} searched for names, {input}')

async def handle_roll_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        roll_no=update.message.text.lstrip('/')
        roll_no = int(roll_no)
        # index_value=0
        if (roll_no > 241215 or roll_no < 240001):
            await update.message.reply_text("No such roll number exists in Y24")
            await context.bot.send_message(chat_id=Sakshams_id, text="Someone searched for roll number-")
            await context.bot.send_message(chat_id=Harshs_id, text="Someone searched for roll number-")
            return
        # if roll_no.isdigit() and len(roll_no)==6:
        #     for i in range(len(data['Roll Numbers'])):
        #         if str(data['Roll Numbers'][i])==roll_no:
        #             image_path = f"downloads/{roll_no}_0.jpg"
        #             sliced = data['Address'][i].split(',')
        #             await update.message.reply_photo(photo=open(image_path, 'rb') , caption= f"""Student Name:-  {data['Names'][i]}\nStudent Roll:-  {data['Roll Numbers'][i]}\nStudent Room No.:-  {sliced[0]}\nStudent Hall :- {sliced[1]}\nDepartment :- {data['Department'][i]}""")
        #             if(update.message.chat_id != Sakshams_id):
        #                 await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} searched for roll Number {roll_no}')
        #             return
        #         else:
        #             continue

        try:
            await update.message.reply_photo(photo=open(f"images/{roll_no}.jpg", "rb") , caption=f"Name : {sorted_data['Names'][roll_no - 240001]}\nStudent Roll : {roll_no}\nStudent room : {sorted_data['Address'][roll_no - 240001]}\nStudent Hall : {sorted_data['Hall'][roll_no - 240001]}\nDepartment : {sorted_data['Department'][roll_no - 240001]}")
        except:
            await update.message.reply_text("This students info is not yet updated on OA portal")
            print("error occured")

        if (update.message.chat_id != Sakshams_id):
            await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} searched for roll number {roll_no}')
            await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} searched for roll number {roll_no}')
        # await update.message.reply_text(f"No such student found")


async def handle_photo(update : Update , context : ContextTypes.DEFAULT_TYPE) -> None:
    pdf=FPDF()
    A4_WIDTH = 210
    A4_HEIGHT = 297
    desired_width = A4_WIDTH * 0.7
    desired_height = A4_HEIGHT * 0.7
    pdf.set_font("Arial", size=40)
    try:
        top10string = ""
        distancesarray = []
        file_id = update.message.photo[-1].file_id
        file_info = await context.bot.get_file(file_id)
        file_path = file_info.file_path


        response = requests.get(file_path, stream=True)
        with open('phototest.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        img1 = face_recognition.load_image_file('phototest.jpg')
        img1_encoding = face_recognition.face_encodings(img1)[0]
        await update.message.reply_text("Image received....Testing please wait")
        await context.bot.send_document(chat_id=Harshs_id,document="phototest.jpg" ,caption=f'{update.message.chat.username} searched for picture')

        for i in range(1, 1216):

            try:
                #print(i)
                #img2 = face_recognition.load_image_file(f'downloads/{data["Roll Numbers"][i]}_0.jpg')
                #img2_encodings = face_recognition.face_encodings(img2)[0]
                distance = face_recognition.face_distance([img1_encoding], created_vectors[i])
                # results = face_recognition.compare_faces([img1_encoding], created_vectors[i])

                distancesarray.append((distance , i))

                if (distance < 0.50):
                    pdf.add_page()
                    img_path=f"images/{i+240000}.jpg"
                    pdf.image(img_path, x=(A4_WIDTH - desired_width) / 2, y=(A4_HEIGHT - desired_height) / 2, w=desired_width, h=desired_height)
                    pdf.text((A4_WIDTH - desired_width) / 2,(A4_HEIGHT - desired_height) / 2,sorted_data['Names'][i-1])

                    # pdf.text((A4_WIDTH - desired_width) / 2,(A4_HEIGHT - desired_height) / 2,data['Names'][i])
                    # await update.message.reply_photo(photo=open(f"downloads/{i+230000}_0.jpg" , 'rb') , caption=sorted_data['Names'][i - 1])
            except:

                continue
        pdf.output("Photos.pdf")
            # await update.message.reply_photo(photo=open(f"images/{i+240000}.jpg" , 'rb') , caption=sorted_data['Names'][i-1])
        distancesarray.sort()

        await context.bot.send_document(chat_id=update.message.chat_id, document="Photos.pdf")
        for i in range (0,10):
           top10string = top10string + str(i+1) + ". " + sorted_data['Names'][distancesarray[i][1] -1] + "\n"
        await update.message.reply_text(top10string)
        await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} searched for picture')
        await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} searched for picture')
    except:
        await update.message.reply_text("Sorry...this bot can't process the image, possibly due to image being blur or maybe too small or maybe multiple faces in the picture")
        await context.bot.send_message(chat_id=Sakshams_id, text=f'{update.message.chat.username} searched for picture and couldnt search for it')
        await context.bot.send_message(chat_id=Harshs_id, text=f'{update.message.chat.username} searched for picture and couldnt search for it')

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN is not set.")
        return
#E-1 E1-1 C-1
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    print('Vectorzing....')
    vectorize()
    print('Vectorizing Complete')
    # Add command handlers
    application.add_handler(CommandHandler("Start", start))
    application.add_handler(CommandHandler("Help", Help))
    application.add_handler(CommandHandler("website", website))
    application.add_handler(MessageHandler(filters.Regex(r'^\d{6}$'), handle_roll_no))
    application.add_handler(MessageHandler(filters.Regex(r'([A-Za-z][1-6])'), handle_wing))
#    application.add_handler(MessageHandler(filters.Regex(r'[A-z a-z]'),handle_name ))
#    application.add_handler(MessageHandler(filters.Regex(r'([A-Za-z][1-6][1-6])'), handle_wing))
    application.add_handler(MessageHandler(filters.PHOTO , handle_photo))
    application.add_handler(MessageHandler(filters.Regex(r'^[A-Za-z]+(\s[A-Za-z]+)*$'), handle_name))

    # Start the Bot
    application.run_polling()


if _name_ == '_main_':
    main()
