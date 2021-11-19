import os
import csv
from otree.api import *


doc = """
Demo of Simple Survey with Images per Question
"""


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

    for i in range(0,2):
        locals()[f"name{i}"] = models.StringField(initial="1")
        locals()[f"age{i}"] = models.IntegerField(initial="1")
        locals()[f"level{i}"] = models.IntegerField(
         choices=[1, 2, 3],
         widget=widgets.RadioSelect,
         initial=1
     )
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
    def before_next_page(player:Player, timeout_happened):
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

def read_csv()

    # opening the CSV file
    # directory_path = os.getcwd()
    # print(directory_path)
    #
    # page_sequence = []
    # questions = []
    #
    # with open('my_simple_survey/questions.csv') as csvfile:
    #     csvFile = csv.reader(csvfile, delimiter=';')
    #     for i, line in enumerate(csvFile):
    #         tmpDict = {}
    #         if i==0:
    #             header= line
    #         else:
    #             # tmpPage = PageTemplate()
    #             # page_sequence.append(PageTemplate())
    #             for j, f in enumerate(line):
    #                 tmpDict[header[j]]=f
    #             questions.append(tmpDict)
    #

page_sequence = []
for i in range(2):
    ff = [f'name{i}', f'age{i}', f'level{i}']

    print(ff)
    cl = type(f"Page{i}", (PageTemplate,), {'form_fields': ff})
    page_sequence.append(cl)
page_sequence.append(Results)
print(page_sequence)

# page_sequence = [Page0, Page1, Results]
# print(page_sequence)
