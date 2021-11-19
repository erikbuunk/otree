import csv
import os
import pathlib
import random
import time
from os.path import join
import itertools
from random import randint


from otree.api import *

doc = """
Demo of Simple Survey with Images per Question
"""

# current directory name
PROJECT_NAME = str(pathlib.Path(__file__).parent.absolute()).split(os.sep)[-1]
HTML = join(PROJECT_NAME, "Pages")
CSV = join(PROJECT_NAME, 'questions.csv')


# -------------HELPER FUNCTIONS -----------------
# read csv
def read_csv(file_name=CSV):
    """Read the CSV file for pages and multiple choice options"""
    local_csv = []
    with open(file_name) as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for i, line in enumerate(file):
            tmpDict = {}
            if i == 0:
                header = line
            else:
                for j, f in enumerate(line):
                    tmpDict[header[j]] = f
            if tmpDict != {}:
                local_csv.append(tmpDict)
    return local_csv


def eliminate_options(choices, correct_option):
    """
    Keeps the correct choice and a random one
    """
    correct = choices.pop(int(correct_option))
    choices.pop(0)
    random_option = random.choice(choices)

    eliminated = sorted([correct, random_option])

    return (eliminated)


# FUNCTIONS
def creating_session(subsession):
    treated = itertools.cycle([True, False])
    # select the quiztype
    quiz = itertools.cycle([3])  # quiz: SciTech
    # quiz = itertools.cycle([2]) # quiztype psyling
    for player in subsession.get_players():
        player.participant.Prolific_ID = player.participant.label
        player.treatment = next(treated)
        player.participant.quiztype = next(quiz) # this one is not remembered
        player.participant.vars['test_var'] = randint(1, 100)


def get_timeout_seconds(player):
    participant = player.participant  # We are defining a function that counts the time left for completing the task
    return participant.expiry - time.time()


def set_payoffs(player):
    totalpayoff = Constants.showup + player.participant.confidence_win + player.participant.advice_payoff
    player.participant.totalpayoff = round(totalpayoff, 2)

    totalpayoff_w_promotion = Constants.showup + player.participant.confidence_win + player.participant.payoff_w_promotion
    player.participant.totalpayoff_w_promotion = round(totalpayoff_w_promotion, 2)

    total_bonus = player.participant.totalpayoff - Constants.flat_rate
    player.participant.total_bonus = round(total_bonus, 2)


# ----------------------Standard Classes ---------------

class Constants(BaseConstants):
    name_in_url = PROJECT_NAME
    players_per_group = None
    num_rounds = 1

    # define the images to use for the different questions
    images = [row["image_link"] for row in read_csv()]

    name_in_url = 'ASG_P1'  # Change
    players_per_group = None
    num_rounds = 1
    showup = 1.25
    low_pr = 0.2  # low piece rate, probability defined in the payoff function
    high_pr = 0.6  # high piece rate, probability defined in the payoff function below
    answertime = 30  # seconds
    confidencetime = 15  # seconds
    confidence_pay = 0.5
    timeout_advice = 15
    advice_cost = 0.05
    max_bonus = 5  # Value for the first page of instructions: ShowUp+Karni+10q*high_pr
    flat_rate = 0.2  # flat piece rate for bonus payment structure
    flat_bonus = 2.5  # bonus pay if "promoted"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # helper variables - not used in survey
    page_number = models.IntegerField(initial=0)
    image = models.StringField(initial=Constants.images[0])

    #### Generate Variables
    quiztype = models.IntegerField(choices=[[1, 'Arts and Literature'], [2, 'Psychology and Linguistics'],
                                            [3, 'Science and Technology'], [4, 'History and Politics']])
    treatment = models.BooleanField()  # To assign for the treatment and control groups

    #### Gen variable-fields for the calculated variables to export with output data file
    quiz_type = models.LongStringField()
    nr_correct_before = models.LongStringField()
    nr_correct_after = models.LongStringField()
    nr_q_advice = models.LongStringField()
    dummy_advice = models.LongStringField()
    coeff_pay = models.LongStringField()
    tot_payoff = models.LongStringField()
    tot_advice_cost = models.LongStringField()
    quiz_pay_beforeA = models.LongStringField()
    total_bonus = models.IntegerField()

    #### Declare Constants
    advice_cost = models.FloatField()
    showup = models.FloatField()
    low_pr = models.FloatField()
    high_pr = models.FloatField()
    answertime = models.IntegerField()
    confidencetime = models.IntegerField()
    confidence_pay = models.FloatField()
    timeout_advice = models.IntegerField()
    flat_bonus = models.FloatField()
    flat_rate = models.FloatField()
    # Prolific Integration
    Prolific_ID = models.LongStringField()

    PID = models.StringField(
        label="Please enter your Prolific ID (PID) below.",
        blank=False)

    q_comprehension1 = models.StringField(
        choices=[["True", "True"], ["False", "False"]], blank=False
    )
    q_comprehension2 = models.StringField(
        choices=[["True", "True"], ["False", "False"]],  blank=False
    )
    q_comprehension3 = models.StringField(
        choices=[["True", "True"], ["False", "False"]], blank=False
    )

    #### Survey variables ---------------
    csv_data = read_csv()
    for row in csv_data:
        choices = [[0, "No Answer"], [1, row['A']], [2, row['B']], [3, row['C']], [4, row['D']], [5, row['E']]]
        question_nr = row['question']
        # q123
        locals()[f"q{question_nr}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )

        # trust_q123
        locals()[f"trust_q{question_nr}"] = models.IntegerField(initial=0, \
                                                                label='I am ___ % certain that my answer is correct')

        # # advice and eliminated
        # # advice_q123
        locals()[f"advice_q{question_nr}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )
        # seek_advice_q123, initiliaze on 0
        locals()[f"seek_advice_q{question_nr}"] = models.IntegerField(initial=0)
        #
        # # advice_q123_eliminated
        locals()[f"advice_q{question_nr}_eliminated"] = models.StringField(
            choices=eliminate_options(choices, row['answer']),
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"])

    # remove the temp variables, since they will not be used in the survey
    del (csv_data)
    del (row)
    del (choices)
    del (question_nr)



# ----------------TEMPLATE PAGES-----------------------

class Question(Page):
    """
    Template page for the questions
    """
    form_model = 'player'

    # Base this page on the the template model
    template_name = join(HTML, 'Question.html')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        """Update pagenumber and image to show"""
        player.page_number = player.page_number + 1

        # Check if we have enough images in the array
        if player.page_number >= len(Constants.images):
            player.image = "empty.jpg"
        else:
            player.image = Constants.images[player.page_number]

    def vars_for_template(player):
        """Return page number and image to the page as a variable
        This can be used in the HTML Page"""
        return dict(
            page=player.page_number,
            image=player.image
        )


class A_a_Welcome1(Page):
    pass


class A_a_Welcome1_PID(Page):
    form_model = 'player'
    form_fields = ['PID']


class A_b_Welcome2(Page):
    def vars_for_template(player: Player):
        player.Prolific_ID = player.participant.label


class B_a_Instructions1(Page):
    def vars_for_template(player: Player):
        return dict(quiztype=player.participant.quiztype)


class B_b_Instructions2(Page):
    # TODO: quiztype not recognized
    def vars_for_template(player: Player):
        return dict(quiztype=player.participant.quiztype)


class B_c_Instructions3(Page):
    pass


class B_d_Comprehension_P1(Page):
    form_model = 'player'
    form_fields = ['q_comprehension1', 'q_comprehension2', 'q_comprehension3']

    def error_message(player, values):
        solutions = dict(
            q_comprehension1="True",
            q_comprehension2="True",
            q_comprehension3="True")
        error_messages = dict()
        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[
                    field_name] = 'One of the answers is incorrect. Please consult the instructions below and try again'
                return error_messages


class B_e_Final_Before_Questions(Page):

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened == True:
            participant.expiry = time.time() + Constants.answertime


class Instructions(Page):
    template_name = join(HTML, 'Instructions.html')


class AdviceQuestion(Page):
    template_name = join(HTML, 'AdviceQuestion.html')
    form_model = 'player'


class AdviceQuestionEliminated(Page):
    template_name = join(HTML, 'AdviceQuestionEliminated.html')
    form_model = 'player'


class Trust(Page):
    """
    Template for confidence page
    """
    template_name = join(HTML, 'Trust.html')
    form_model = 'player'


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    template_name = join(HTML, 'Results.html')
    pass


# -------------- CONSTRUCT PAGES---------------------
# initial pages
page_sequence = [
    A_a_Welcome1,
    A_b_Welcome2,
    B_a_Instructions1,
    B_b_Instructions2,
    B_c_Instructions3,
    B_d_Comprehension_P1,
    B_e_Final_Before_Questions
]

csv_file = read_csv()
for row in csv_file:
    # add survey field
    question_nr = row['question']
    form_fields = [f"q{question_nr}"]
    ## Create a class with (name, template and a dictory of variables/functions)
    cl = type(f"Page{question_nr}", (Question,), {'form_fields': form_fields})
    page_sequence.append(cl)

    # add Trust
    form_fields = [f"trust_q{question_nr}"]
    cl = type(f"Trust{question_nr}", (Trust,), {'form_fields': form_fields})
    page_sequence.append(cl)

## inststructions
page_sequence.append(Instructions)

## Add advice sequence
for row in csv_file:
    # Advice question
    question_nr = row['question']
    form_fields = [f"advice_q{question_nr}", f"seek_advice_q{question_nr}"]
    cl = type(f"AdviceQuestion{question_nr}", (AdviceQuestion,), {'form_fields': form_fields})
    page_sequence.append(cl)

    # AdviceQuestionEliminated
    form_fields = [f"advice_q{question_nr}_eliminated"]
    cl = type(f"AdviceQuestionEliminated{question_nr}", (AdviceQuestionEliminated,), {'form_fields': form_fields})
    page_sequence.append(cl)

# add additional pages
page_sequence.append(Results)
