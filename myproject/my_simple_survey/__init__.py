import csv
import random
import os
from os.path import join
import pathlib


from otree.api import *

doc = """
Demo of Simple Survey with Images per Question
"""

# current directory name
# TODO Read from config file
PROJECT_NAME = str(pathlib.Path(__file__).parent.absolute()).split(os.sep)[-1]
HTML = join(PROJECT_NAME, "Pages")
CSV = join(PROJECT_NAME,'questions.csv')


# -------------HELPER FUNCTIONS -----------------
# read csv
def read_csv(file_name=CSV):
    """Read the CSV file for pages and multiple choice options"""
    local_csv=[]
    with open(file_name) as csvfile:
        file = csv.reader(csvfile, delimiter=';')
        for i, line in enumerate(file):
            tmpDict = {}
            if i==0:
                header= line
            else:
                for j, f in enumerate(line):
                    tmpDict[header[j]]=f
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

    eliminated=sorted([correct, random_option])

    return(eliminated)


#----------------------Standard Classes ---------------

class Constants(BaseConstants):
    name_in_url = PROJECT_NAME
    players_per_group = None
    num_rounds = 1

    # define the images to use for the different questions
    images=[row["image_link"] for row in read_csv()]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # helper variables - not used in survey
    page_number = models.IntegerField(initial=0)
    image = models.StringField(initial=Constants.images[0])

    # Survey variables
    csv_data = read_csv()
    for row in csv_data:
        choices = [[0, "No Answer"],[1, row['A']], [2, row['B']], [3,row['C']], [4,row['D']], [5,row['E']]]
        question_nr = row['question']
        # q123
        locals()[f"q{question_nr}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )

        #trust_q123
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
        # seek_advice_q123
        locals()[f"seek_advice_q{question_nr}"]=models.IntegerField(initial=0)
        #
        # # advice_q123_eliminated
        locals()[f"advice_q{question_nr}_eliminated"]=models.StringField(
            choices=eliminate_options(choices, row['answer'] ),
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"])

    # remove the temp variables, since they will not be used in the survey
    del(csv_data)
    del(row)
    del(choices)
    del(question_nr)


# ----------------TEMPLATE PAGES-----------------------

class Question(Page):
    """
    Template page for the questions
    """
    form_model = 'player'

    # Base this page on the the template model
    template_name = join(HTML,'Question.html')

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


class Instructions(Page):
    template_name = join(HTML,'Instructions.html')

class AdviceQuestion(Page):
    template_name = join(HTML,'AdviceQuestion.html')
    form_model = 'player'

class AdviceQuestionEliminated(Page):
    template_name = join(HTML,'AdviceQuestionEliminated.html')
    form_model = 'player'


class Trust(Page):
    """
    Template for confidence page
    """
    template_name = join(HTML,'Trust.html')
    form_model = 'player'

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    template_name = join(HTML, 'Results.html')
    pass



# -------------- CONSTRUCT PAGES---------------------
# initial pages
page_sequence = [Instructions]

csv_file = read_csv()
for row in csv_file:
    # add survey field
    question_nr=row['question']
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