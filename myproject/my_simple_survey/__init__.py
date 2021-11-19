import os
import csv
from otree.api import *

doc = """
Demo of Simple Survey with Images per Question
"""

# read csv
def read_csv():
    local_csv=[]
    with open('my_simple_survey/questions_bak.csv') as csvfile:
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
    # This can be done later by reading a CSV with the data
    images = ["puppy.jpg", "python.jpg"]


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
    for i in csv_data:
        locals()[f"question{i['question_nr_exp']}"] = models.StringField(
            choices=[i['A'], i['B'], i['C'], i['D'], i['E']],
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=i["label_text"]
        )

    # remove the local variables, since they will not be used in the survey
    del(csv_data)
    del(i)


# PAGES
class PageTemplate(Page):
    """
    Template page for the questions
    We use this to prevent duplicate code per page
    """

    form_model = 'player'

    # Base this page on the the template model
    template_name = 'my_simple_survey/MyPage.html'

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
        """Return pagenumber and image to the page as a variable"""
        return dict(
            page=player.page_number,
            image=player.image
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    pass


# opening the CSV file
page_sequence = []



# for i in range(2):
#     ff = [f'name{i}', f'age{i}', f'level{i}']
#
#     print(ff)
#     cl = type(f"Page{i}", (PageTemplate,), {'form_fields': ff})
#     page_sequence.append(cl)
# page_sequence.append(Results)

csv_data = read_csv()
print ("Creating page sequence")
for i in csv_data:
    ff = [f"question{i['question_nr_exp']}"]
    cl = type(f"Page{i['question_nr_exp']}", (PageTemplate,), {'form_fields': ff})
    page_sequence.append(cl)

# add results page
page_sequence.append(Results)


print(page_sequence)

# page_sequence = [Page0, Page1, Results]
# print(page_sequence)
