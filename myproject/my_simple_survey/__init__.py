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
HTML = join(PROJECT_NAME, "")
CSV = join(PROJECT_NAME, 'questions.csv')

# prefixes in constants
QUESTION = "q"
TRUST = "trust_q"
ADVICE = "advice_q"
SEEK_ADVICE = "seek_advice_q"
ADVICE_ELIMINATED = "advice_eliminated_q"


# -------------HELPER FUNCTIONS -----------------
# read csv
def read_csv(file_name=CSV):
    """Read the CSV file for pages and multiple choice options"""
    local_csv = []
    with open(file_name) as csv_file:
        file = csv.reader(csv_file, delimiter=';')
        for i, line in enumerate(file):
            tmp_dict = {}
            if i == 0:
                header = line
            else:
                for j, f in enumerate(line):
                    tmp_dict[header[j]] = f
            if tmp_dict != {}:
                local_csv.append(tmp_dict)
    return local_csv


def eliminate_options(choices, correct_option):
    """
    Keeps the correct choice and one other choice, randomly chosen
    """
    correct = choices.pop(int(correct_option))
    choices.pop(0)
    random_option = random.choice(choices)

    eliminated = sorted([correct, random_option])

    return eliminated


def create_class(class_prefix, question_nr, base_class, form_fields_prefixes) -> object:
    """
    Since otree works with add classes (as opposed to instantiated objects
    from the Class, this function create a Class with the formields as attributes
    This function is creates to hide the special syntax

    class_prefix (str):                 prefix used in the Class name and the form fields,
                                            eg 'Question' -> Class name: Question_52
    question_nr (str):                  identifier of the question, eg. 52
    base_class (Class object):          the parent Class from which this class will inherit its properties. eg. Question
    form_fields_prefixes (list of str): variables that will be created, question number will be added
                                           eg. ["trust_q"] -> trust_q52
    """
    form_fields = [f"{ff_prefix}{question_nr}" for ff_prefix in form_fields_prefixes]
    return type(f"{class_prefix}{question_nr}", (base_class,), {'form_fields': form_fields})

def create_page_sequences():
    """
    Create 2 sequences of pages
    The first is the initial Question + Trust Question
    The second sequence is the the Question where advice can be asked
    """
    csv_file = read_csv()
    sequence_1 = []
    sequence_2 = []
    for row in csv_file:
        question_nr = row['question']

        # First Round
        # add survey field
        sequence_1.append(create_class("Question", question_nr, Question, [QUESTION]))
        # add Trust
        sequence_1.append(create_class("Trust", question_nr, Trust, [TRUST]))

        # Second Round
        # Advice question
        sequence_2.append(create_class("AdviceQuestion", question_nr, AdviceQuestion, [ADVICE, SEEK_ADVICE]))
        # AdviceQuestionEliminated
        sequence_2.append(
            create_class("AdviceQuestionEliminated", question_nr, AdviceQuestionEliminated, [ADVICE_ELIMINATED]))

    return (sequence_1, sequence_2)

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

    #### CreateSurvey variables from CSV file---------------
    csv_data = read_csv()
    for row in csv_data:
        choices = [[0, "No Answer"], [1, row['A']], [2, row['B']], [3, row['C']], [4, row['D']], [5, row['E']]]
        question_nr = row['question']
        # q123
        locals()[f"{QUESTION}{question_nr}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )

        # trust_q52
        locals()[f"{TRUST}{question_nr}"] = models.IntegerField(initial=0, \
                                                                label='I am ___ % certain that my answer is correct')

        # # advice_q52
        locals()[f"{ADVICE}{question_nr}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )
        # seek_advice_q52, initiliaze on 0
        locals()[f"{SEEK_ADVICE}{question_nr}"] = models.IntegerField(initial=0)

        # advice_eliminated_q52
        locals()[f"{ADVICE_ELIMINATED}{question_nr}"] = models.StringField(
            choices=eliminate_options(choices, row['answer']),
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"])

    # remove the temp variables, since they will not be used in the survey
    del (csv_data)
    del (row)
    del (choices)
    del (question_nr)



# ----------------Pages-----------------------

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

class Question(Page):
    """
    Template page for the questions
    """
    form_model = 'player'

    # Base this page on the the template model
    template_name = join(HTML, 'C_a_Question.html')

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

class Trust(Page):
    """
    Template for confidence page
    """
    template_name = join(HTML, 'C_b_Trust.html')
    form_model = 'player'

class D_a_Advice_Instructions1(Page):
    pass
class D_b_Advice_Instructions2(Page):
    pass
class D_c_Advice_Instructions3_BL(Page):
    pass
class D_c_Advice_Instructions3_TM(Page):
    pass
class D_d_Advice_Comprehension_BL(Page):
    pass
class D_d_Advice_Comprehension_TM(Page):
    pass
class D_e_Final_Before_Questions_BL(Page):
    pass
class D_e_Final_Before_Questions_TM(Page):
    pass

class AdviceQuestion(Page):
    template_name = join(HTML, 'E_a_AdviceQuestion.html')
    form_model = 'player'


class AdviceQuestionEliminated(Page):
    template_name = join(HTML, 'E_b_AdviceQuestionEliminated.html')
    form_model = 'player'

class E_w_Payoffs(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    template_name = join(HTML, 'Results.html')
    pass


# -------------- Page sequence ---------------------

# Initial pages
page_sequence = [
    A_a_Welcome1,
    A_b_Welcome2,
    B_a_Instructions1,
    B_b_Instructions2,
    B_c_Instructions3,
    B_d_Comprehension_P1,
    B_e_Final_Before_Questions
]

(first_sequence, second_sequence) = create_page_sequences()
page_sequence.extend(first_sequence) # use extend because first sequence is a list

## Intermediate instructions
page_sequence.extend([D_a_Advice_Instructions1,
                 D_b_Advice_Instructions2,
                 D_c_Advice_Instructions3_BL,
                 D_c_Advice_Instructions3_TM,
                 D_d_Advice_Comprehension_BL,
                 D_d_Advice_Comprehension_TM,
                 D_e_Final_Before_Questions_BL,
                 D_e_Final_Before_Questions_TM])

## Second round with advice
page_sequence.extend(second_sequence)

# add additional pages
page_sequence.append(E_w_Payoffs)

print(page_sequence)