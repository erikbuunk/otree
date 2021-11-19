import csv
import random

from otree.api import *

doc = """
Demo of Simple Survey with Images per Question
"""

# read csv
def read_csv(file_name='my_simple_survey/questions.csv'):
    """Read the CSV file"""
    local_csv=[]
    with open(file_name) as csvfile:
        csv_file = csv.reader(csvfile, delimiter=';')
        for i, line in enumerate(csv_file):
            tmpDict = {}
            if i==0:
                header= line
            else:
                for j, f in enumerate(line):
                    tmpDict[header[j]]=f
            if tmpDict != {}:
                local_csv.append(tmpDict)
    return local_csv



class Constants(BaseConstants):
    name_in_url = 'my_simple_survey'
    players_per_group = None
    num_rounds = 1

    # define the images to use for the different questions
    images=[row["image_link"] for row in read_csv()]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def eliminate_options(choices, correct_option):
    correct = choices.pop(int(correct_option))
    choices.pop(0)
    random_option = random.choice(choices)
    eliminated=[correct, random_option]
    print(choices, "->", eliminated)
    return(eliminated)

class Player(BasePlayer):
    # helper variables - not used in survey
    page_number = models.IntegerField(initial=0)
    image = models.StringField(initial=Constants.images[0])

    # Survey variables
    csv_data = read_csv()
    for row in csv_data:
        choices = [[0, "No Answer"],[1, row['A']], [2, row['B']], [3,row['C']], [4,row['D']], [5,row['E']]]
        all_options = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )

        # q123
        locals()[f"q{row['question']}"] = all_options

        #trust_q123
        locals()[f"trust_q{row['question']}"] = models.IntegerField(initial=0, \
            label='I am ___ % certain that my answer is correct')

        # # advice and eliminated
        # # advice_q123
        locals()[f"advice_q{row['question']}"] = models.StringField(
            choices=choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )
        # seek_advice_q123
        locals()[f"seek_advice_q{row['question']}"]=models.IntegerField(initial=0)
        #
        # # advice_q123_eliminated
        new_choices = eliminate_options(choices, row['answer'] )
        subset_options = models.StringField(
            # TODO: check order
            choices=new_choices,
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"])
        locals()[f"advice_q{row['question']}_eliminated"]=subset_options
    del(new_choices)
    del(subset_options)
    #
    # remove the temp variables, since they will not be used in the survey
    del(csv_data)
    del(row)
    del(choices)
    del(all_options)


# PAGES
class Question(Page):
    """
    Template page for the questions
    """

    form_model = 'player'

    # Base this page on the the template model
    template_name = 'my_simple_survey/Question.html'

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
    template_name = 'my_simple_survey/Instructions.html'

class AdviceQuestion(Page):
    template_name = 'my_simple_survey/AdviceQuestion.html'
    form_model = 'player'

class AdviceQuestionEliminated(Page):
    template_name = 'my_simple_survey/AdviceQuestionEliminated.html'
    form_model = 'player'


class Trust(Page):
    """
    Template for confidence page
    """
    template_name = 'my_simple_survey/Trust.html'
    form_model = 'player'

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    pass


# initial pages
page_sequence = [Instructions]

# print ("Creating page sequence")
csv_file = read_csv()
for row in csv_file:
    # add survey field
    form_fields = [f"q{row['question']}"]
    ## Create a class with (name, template and a dictory of variables/functions)
    cl = type(f"Page{row['question']}", (Question,), {'form_fields': form_fields})
    page_sequence.append(cl)

    # add Trust
    form_fields = [f"trust_q{row['question']}"]
    cl = type(f"Trust{row['question']}", (Trust,), {'form_fields': form_fields})
    page_sequence.append(cl)


## inststructions
page_sequence.append(Instructions)

## Add advice sequence

for row in csv_file:
    # Advice question
    form_fields = [f"advice_q{row['question']}", f"seek_advice_q{row['question']}"]
    cl = type(f"AdviceQuestion{row['question']}", (AdviceQuestion,), {'form_fields': form_fields})
    page_sequence.append(cl)

    # AdviceQuestionEliminated
    form_fields = [f"advice_q{row['question']}_eliminated"]
    cl = type(f"AdviceQuestionEliminated{row['question']}", (AdviceQuestionEliminated,), {'form_fields': form_fields})
    page_sequence.append(cl)


# add additional pages
page_sequence.append(Results)

print(page_sequence)