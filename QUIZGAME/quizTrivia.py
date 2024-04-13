# importing the necessary libraries
from customtkinter import *
import customtkinter as ck
import time as tm
from PIL import Image
from helper import get_quiz, reshape_quiz, resource_path
from threading import Thread

USERS_FILE = 'users.csv'  # users database
current_user = None
ck.set_appearance_mode('dark')

class User(object):

    def __init__(self, user_information):
        self.name, self.total_score, self.quiz_taken, self.CA = user_information
        self.total_score = int(self.total_score)
        self.quiz_taken = int(self.quiz_taken)
        self.CA = int(self.CA)

    def update_data(self, score, correct_ans, questions_taken):
        self.total_score += score
        self.quiz_taken += questions_taken
        self.CA += correct_ans

    def __str__(self):
        return f'<User.__init.__Username:{self.name}, total_score:{self.total_score}, q_taken:{self.quiz_taken}, \
                CA:{self.CA}>'

    def user_information(self):
        return [self.name, self.total_score, self.quiz_taken, self.CA]

    def save(self):
        with open(USERS_FILE, 'a') as file:
            file.write(f'\n{self.name},{self.total_score},{self.quiz_taken},{self.CA}\n')

# This is login page for the trivia quiz game
# It checks if there's any user in the database and if not it creates a new user and database
class LoginPage:
    def __init__(self, master):
        self.master = master

    def new_user_loginpage(self):
        side_img_data = Image.open(resource_path("icons/quizpic3.png"))
        user_icon_data = Image.open(resource_path("icons/man.png"))
        gender_icon_data = Image.open(resource_path('icons/equality.png'))
        google_icon_data = Image.open(resource_path("icons/google-icon.png"))

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(380, 600))
        user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20, 20))
        gender_icon = CTkImage(dark_image=gender_icon_data, light_image=gender_icon_data, size=(17, 17))
        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

        self.label = CTkLabel(master=self.master, text="", image=side_img)
        self.label.pack(expand=True, side="left")

        self.frame = CTkFrame(master=self.master, width=380, height=600, fg_color="#B8860B")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="right")

        new_user_label = CTkLabel(master=self.frame, text="Welcome to \nword quiz trivia!".upper(), text_color="#601E88",
                                  anchor="w", justify="left", font=("Arial Bold", 25)).pack(anchor="w", pady=(50, 5),
                                                                                            padx=(25, 0))
        signin = CTkLabel(master=self.frame, text="Create a new user account", text_color="#7E7E7E", anchor="w",
                          justify="left", font=("Arial Bold", 15)).pack(anchor="w", padx=(25, 0))

        name_label = CTkLabel(master=self.frame, text="  Username:", text_color="#601E88", anchor="w", justify="left",
                              font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(38, 0),
                                                                                              padx=(25, 0))
        username = CTkEntry(master=self.frame, width=300, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                            text_color="#000000", font=('Helvetica', 17))
        username.pack(anchor="w", padx=(25, 0))

        Gender_label = CTkLabel(master=self.frame, text="  Gender:", text_color="#601E88", anchor="w", justify="left",
                                font=("Arial Bold", 14), image=gender_icon, compound="left").pack(anchor="w",
                                                                                                  pady=(21, 0),
                                                                                                  padx=(25, 0))
        self.gender = CTkOptionMenu(master=self.frame, values=['Male', 'Female', 'Others'], width=300, fg_color="#EEEEEE",

                               text_color="#000000", font=('Helvetica', 17))
        self.gender.pack(anchor="w", padx=(25, 0))

        create_user_button = CTkButton(master=self.frame, text="Create new user", fg_color="#601E88", hover_color="#E44982",
                                       font=("Arial Bold", 12), text_color="#ffffff", width=300, height=40,
                                        command=lambda: self.create_user(username.get()))
        create_user_button.pack(anchor="w", pady=(40, 0), padx=(25, 0))
        ggogle_button = CTkButton(master=self.frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE",
                                  font=("Arial Bold", 9), text_color="#601E88", width=300, image=google_icon).pack(
            anchor="w", pady=(20, 0), padx=(25, 0))

    def getuser(self):
        # checking to see if we have any user in the database
        try:

            user_file = open(USERS_FILE, 'r')
            users = [i.strip().split(',') for i in user_file.readlines()]
            global current_user
            current_user = User(users[-1])

            HomePage(master=self.master, user=current_user)
        # if there's no database, we create a new user and store his details in a new database
        except FileNotFoundError:

            self.new_user_loginpage()

    def create_user(self, name: str):
        if name is None:
            pass
        else:
            # creating a new file to save the user records
            with open(USERS_FILE, 'a') as user:
                user.write('Name,Quizzes_taken,Correct_Questions,Total_Score \n')
                user.write(f'{name},0,0,0\n')
            global current_user
            current_user = User([name, 0, 0, 0])
            self.frame.pack_forget()
            self.label.pack_forget()
            HomePage(self.master, current_user)



# This is the home page of the game
# It shows the users stats(how many games played, correct answers etc)
# The user also selects the quiz he wants to take
class HomePage:
    def __init__(self, master, user: User):
        self.user = user

        self.master = master
        self.frame = CTkScrollableFrame(self.master, height=580, width=750)
        self.frame.pack(padx=5, pady=10)

        stats = CTkLabel(master=self.frame, text=f"Welcome back {self.user.name} \n \n Your Stats:", font=("Arial Bold", 30),
                         justify="left").pack(anchor="w", pady=(43, 18), padx=(56, 0))

        stats_frame = CTkFrame(master=self.frame, fg_color="transparent")
        stats_frame.pack(padx=(54, 0), pady=(18, 0), anchor="nw")

        quizzes_taken_frame = CTkFrame(master=stats_frame, fg_color="#70179A", width=200, height=100, corner_radius=8)
        quizzes_taken_frame.pack_propagate(0)
        quizzes_taken_frame.pack(anchor="w", side="left", padx=(0, 20))

        quizzes_taken = CTkLabel(master=quizzes_taken_frame, text="Quizzes Taken", font=("Arial Bold", 10),
                                 text_color="#F3D9FF").pack(anchor="nw", padx=(14, 0))
        no_quiz_taken = CTkLabel(master=quizzes_taken_frame, text=f"{self.user.quiz_taken}", justify="left", font=("Arial Bold", 25),
                                 text_color="#F3D9FF").pack(anchor="nw", padx=(14, 0))

        correct_qs_frame = CTkFrame(master=stats_frame, fg_color="#146C63", width=200, height=100, corner_radius=8)
        correct_qs_frame.pack_propagate(0)
        correct_qs_frame.pack(anchor="w", side="left", padx=(0, 20))

        correct_questions = CTkLabel(master=correct_qs_frame, text="Correct Questions", font=("Arial Bold", 10),
                                     text_color="#D5FFFB").pack(anchor="nw", padx=(14, 0))
        no_correct_questions = CTkLabel(master=correct_qs_frame, text=f"{self.user.CA}", justify="left",
                                        font=("Arial Bold", 25), text_color="#D5FFFB").pack(anchor="nw", padx=(14, 0))

        highest_score_frame = CTkFrame(master=stats_frame, fg_color="#9A1717", width=200, height=100, corner_radius=8)
        highest_score_frame.pack_propagate(0)
        highest_score_frame.pack(anchor="w", side="left", padx=(0, 20))

        highest_score = CTkLabel(master=highest_score_frame, text="Total Score", font=("Arial Bold", 10),
                                 text_color="#FFCFCF").pack(anchor="nw", padx=(14, 0))
        highest_score_no = CTkLabel(master=highest_score_frame, text=f"{self.user.total_score}", justify="left",
                                    font=("Arial Bold", 25), text_color="#FFCFCF").pack(anchor="nw", padx=(14, 0))

        take_quiz_label = CTkLabel(master=self.frame, text="Take A Quiz", font=("Arial Bold", 30), justify="left").pack(
            anchor="nw", side="top", padx=(56, 0), pady=(41, 0))

        quizzes_frame = CTkFrame(master=self.frame, fg_color="transparent")
        quizzes_frame.pack(pady=(21, 0), padx=(50, 0), anchor="nw")

        self.category = ['Books', 'Celebrities', 'Computers', 'General-\nKnowledge', 'Geography', 'History', 'Music', 'Sports']
        colors = ['#ffd700', '#ba55d3', '#adff2f', '#20b2aa', '#FFFACD', '#00FFFF','#ba55d3', '#adff2f',]
        categories_button = [CTkButton(master=quizzes_frame, text=self.category[i], width=260, height=100, border_width=5,
                                       border_color=colors[i],command=lambda index = i: self.next_page(index),
                                       corner_radius=8, fg_color='transparent', font=('Arial', 30, 'bold')) for i in
                             range(len(self.category))

                             ]
        grids = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1),(3, 0), (3, 1)]
        [categories_button[i].grid(row=grid[0], column=grid[1], sticky="nw", pady=10, padx=25) for i, grid in
         enumerate(grids)]

    def next_page(self, index):
        self.frame.pack_forget()
        category = self.category[index]
        if category == 'General-\nKnowledge':
            category = 'General-Knowleadge'
        # going to the next page
        DifficultyPage(self.master, category)

class DifficultyPage:
    def __init__(self, master, quizcategory):
        self.master = master
        self.quizcategory = quizcategory
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.bg_img = CTkLabel(self.master, text='',
                               image=CTkImage(light_image=Image.open(resource_path('icons/quizpic3.png')),
                                size=(760, 600)))
        self.bg_img.place(relx=0, rely=0)
        self.difficulty_label = CTkLabel(master=self.master, text='Choose Difficulty: ', font=("Arial Bold", 35),
                                         justify="left")
        self.difficulty_label.pack(anchor="w", pady=(43, 18), padx=(56, 0))
        self.difficulties_button = [CTkButton(master=self.master, text=i, width=200, height=50, border_width=5,
                                              border_color='#fff8dc', command=lambda cat = i: self.next_page(cat), # '#fffacd',
                                              corner_radius=8, fg_color='#d2691e', font=('Arial', 30, 'bold')) for i
                                    in
                                    self.difficulties

                                    ]
        [i.pack(padx=10, pady=20) for i in self.difficulties_button]

    def next_page(self, category: str):
        # print(category)
        [i.pack_forget() for i in self.difficulties_button]
        self.difficulty_label.pack_forget()
        self.bg_img.place_forget()
        # tm.sleep(1)
        QuizPage(self.master, [self.quizcategory, category.lower()])
        # Thread(target=QuizPage, args=(self.master, [self.quizcategory, category.lower()])).start()

# This the quiz page for the Game
# it takes in a CTk class and the name of the quiz to play
class QuizPage:
    def __init__(self, master, quiz: list, ):

        self.master = master
        self.master.geometry("760x600")
        self.start_time = tm.time()
        self.question_num = 0
        self.current_score = 0
        self.correct = 0
        self.choice = None
        self.options = []

    # Getting the quiz from The Quiz folder
        self.questions, self.correct_answer, self.answers = get_quiz(category=quiz[0], difficulty=quiz[1])

        # seting up the User interface and given it functionality
        self.frame = CTkFrame(master=self.master, fg_color="transparent")
        self.frame.pack(padx=(54, 0), pady=(18, 0), anchor="nw")

        time_frame = CTkFrame(master=self.frame, fg_color="#800000", width=200, height=70, corner_radius=8)
        time_frame.pack_propagate(0)
        time_frame.pack(anchor="w", side="left", padx=(10, 20))

        self.time = CTkLabel(master=time_frame, text="00:00", justify="center", font=("Arial Bold", 70),
                             text_color="#F3D9FF")
        self.time.pack(anchor="nw", padx=(14, 0))

        score_frame = CTkFrame(master=self.frame, fg_color="#146C63", width=300, height=70, corner_radius=8)
        score_frame.pack_propagate(0)
        score_frame.pack(anchor="w", side="left", padx=30)

        self.score = CTkLabel(master=score_frame, text=f'SCORE: {self.current_score}', justify="center",
                              font=("Helvetica Bold", 55),
                              text_color="#D5FFFB")
        self.score.pack(anchor="nw", padx=(14, 0))

        self.question_label = CTkLabel(master=self.master, text=f'{self.question_num + 1}/20', justify='left',
                                       font=("Arial Bold", 20),
                                       text_color="#D5FFFB")
        self.question_label.place(relx=0.45, rely=0.18)
        self.question_bar = CTkProgressBar(master=self.master, progress_color="#2A55B8")
        self.question_bar.set(self.question_num + 1 / 20)
        self.question_bar.pack(fill="x", anchor="n", pady=(46, 0), padx=50)

        self.quiz_label = CTkLabel(master=self.master,
                                   text=f"Q{self.question_num + 1}: {reshape_quiz(self.questions[self.question_num])}",
                                   font=("Arial Bold", 20), justify="left")
        self.quiz_label.pack(anchor="w", pady=(33, 0), padx=(50, 0))

        q1_frame = CTkFrame(master=self.master, corner_radius=8, fg_color="#fff")
        q1_frame.pack(fill="x", anchor="w", pady=(39, 0), padx=50)

        Q1 = CTkCheckBox(master=q1_frame, text_color="black", fg_color="#2A55B8", checkmark_color="#fff",

                         hover_color="#A6C1FF", text=f'{self.answers[0][0]}', font=('Arial', 20),
                         command=lambda: self.button_command(0))
        Q1.pack(side="left", padx=(16, 20), pady=(8, 8))

        q2_frame = CTkFrame(master=self.master, corner_radius=8, fg_color="#fff")
        q2_frame.pack(fill="x", anchor="w", pady=(20, 0), padx=50)

        Q2 = CTkCheckBox(master=q2_frame, text_color="black", fg_color="#2A55B8", checkmark_color="#fff",
                         hover_color="#2A55B8", text=f'{self.answers[self.question_num][1]}', font=('Arial', 20),
                         command=lambda: self.button_command(1))
        Q2.pack(side="left", padx=(16, 20), pady=(8, 8))

        q3_frame = CTkFrame(master=self.master, corner_radius=8, fg_color="#fff")
        q3_frame.pack(fill="x", anchor="w", pady=(20, 0), padx=50)

        Q3 = CTkCheckBox(master=q3_frame, text_color="black", fg_color="#2A55B8", checkmark_color="#fff",
                         hover_color="#2A55B8", text=f'{self.answers[self.question_num][2]}', font=('Arial', 20),
                         command=lambda: self.button_command(2))
        Q3.pack(side="left", padx=(16, 20), pady=(8, 8))

        q4_frame = CTkFrame(master=self.master, corner_radius=8, fg_color="#fff")
        q4_frame.pack(fill="x", anchor="w", pady=(20, 0), padx=50)

        Q4 = CTkCheckBox(master=q4_frame, text_color="black", fg_color="#2A55B8", checkmark_color="#fff",
                         hover_color="#2A55B8", text=f'{self.answers[self.question_num][3]}', font=('Arial', 20),
                         command=lambda: self.button_command(3))
        Q4.pack(side="left", padx=(16, 20), pady=(8, 8))

        self.next_button = CTkButton(master=self.master, text="Next Question", font=("Arial Bold", 20),
                                hover_color="#299039",
                                fg_color="#35B248", command=self.nextquiz)
        self.next_button.pack(fill="x", ipady=15, pady=(50, 0), padx=50)
        self.options = [(Q1, q1_frame), (Q2, q2_frame), (Q3, q3_frame), (Q4, q4_frame)]

        Thread(target=self.update_time).start()

    def nextquiz(self):
        if self.choice is None:
            pass
        else:
            #increase the user's score if he gets the answer right
            if self.choice == self.correct_answer[self.question_num]:
                self.current_score += 5
                self.correct += 1
                self.score.configure(text=f'SCORE: {self.current_score}')
            # End quiz
            if self.question_num == 19:
                self.nextpage()
            else:
                # update the GUI to go to next quiz
                self.question_num += 1
                self.question_bar.set(self.question_num / 20)
                self.question_label.configure(text=f'{self.question_num + 1}/20')
                self.choice = None
                [self.options[i][1].configure(fg_color="#fff") for i in range(len(self.options))]
                [self.options[i][0].configure(state=NORMAL) for i in range(len(self.options))]

                self.quiz_label.configure(text=reshape_quiz(self.questions[self.question_num]))
                [self.options[i][0].configure(text=self.answers[self.question_num][i]) for i in range(len(self.options))]

    # collects the answer the user chose
    def button_command(self, index):

        if self.options[index][0].get() == 1:
            self.choice = self.answers[self.question_num][index]
            [self.options[i][1].configure(fg_color="#2A55B8") if i == index else self.options[i][1].configure(
                fg_color="#fff") for i in range(len(self.options))]
            [self.options[i][0].configure(state=DISABLED) for i in range(len(self.options)) if i != index]


        else:
            self.choice = None
            [self.options[i][1].configure(fg_color="#fff") for i in range(len(self.options))]
            [self.options[i][0].configure(state=NORMAL) for i in range(len(self.options))]

    # upadtes the timer every second
    def update_time(self):

        timer = int(tm.time() - self.start_time)
        if timer >= 60:
            minutes = int(timer / 60)
            seconds = timer % 60
            self.time.configure(text=f'0{minutes}:{seconds}') if seconds >= 10 else self.time.configure(
                text=f'0{minutes}:0{seconds}')
        else:
            self.time.configure(text=f'00:0{timer}') if timer < 10 else self.time.configure(text=f'00:{timer}')

        self.time.after(1000, self.update_time)

    def nextpage(self):
        self.frame.pack_forget()

        for i in self.options:
            i[0].pack_forget()
            i[1].pack_forget()

        self.question_label.place_forget()
        self.question_bar.pack_forget()
        self.quiz_label.pack_forget()
        self.next_button.pack_forget()

        current_user.update_data(self.current_score, self.correct, 20)
        current_user.save()

        CompleteQuiz(self.master, self.current_score, self.correct)



class CompleteQuiz:
    def __init__(self, master, score: int, correct: int):
        self.master = master

        self.frame = CTkFrame(master=self.master, fg_color='#d2691e', border_width=6,border_color="#f5f5f5")
        self.frame.pack(fill='x',ipady=15, pady=(50, 0),padx=50, anchor="nw")

        trophy_icon_data = Image.open(resource_path("icons/trophy.png"))
        trophy_icon = CTkImage(dark_image=trophy_icon_data, light_image=trophy_icon_data, size=(100, 100))

        self.trophy_image = CTkLabel(self.frame, text=f'', image=trophy_icon, height=100, width=100,
                                     font=('Arial', 40))
        self.trophy_image.pack(padx=30, pady=20)

        self.score = CTkLabel(self.frame, text=f'Score: \n{score}', height=20, width=100,
                              font=('Arial', 40))
        self.score.pack(padx=30, pady=20)

        self.correct = CTkLabel(self.frame, text=f'You got {correct} out of 20 questions', height=15, width=100,
                                font=('Arial', 25))
        self.correct.pack(padx=10, pady=10)

        self.nextquiz_button = CTkButton(master=self.master, text="Next Quiz?", font=("Arial Bold", 20),
                                hover_color="#299039",command=self.goto_nextpage,
                                fg_color="#35B248")
        self.nextquiz_button.pack(fill="x", ipady=15, pady=(50, 0), padx=50)

    def goto_nextpage(self):
        self.frame.pack_forget()
        self.nextquiz_button.pack_forget()
        HomePage(self.master, current_user)


class QuizTrivia:
    def __init__(self):
        self.master = CTk()
        self.master.iconbitmap(resource_path('icons/favicon.ico'))
        self.master.title('QuizTrivia')
        self.master.geometry("760x600")
        self.master.resizable(0, 0)

    def play(self):
        print('Starting Game')
        LoginPage(master=self.master).getuser()
        self.master.mainloop()
