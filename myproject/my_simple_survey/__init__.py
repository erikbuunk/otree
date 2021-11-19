import csv
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


class Player(BasePlayer):
    # helper variables - not used in survey
    page_number = models.IntegerField(initial=0)
    image = models.StringField(initial=Constants.images[0])

    # Survey variables
    csv_data = read_csv()
    for row in csv_data:
        locals()[f"q{row['question_nr_exp']}"] = models.StringField(
            choices=[row['A'], row['B'], row['C'], row['D'], row['E']],
            widget=widgets.RadioSelectHorizontal,
            initial=0,
            label=row["label_text"]
        )

    # remove the temp variables, since they will not be used in the survey
    del(csv_data)
    del(row)


# PAGES
class PageTemplate(Page):
    """
    Template page for the questions
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
        """Return page number and image to the page as a variable
        This can be used in the HTML Page"""
        return dict(
            page=player.page_number,
            image=player.image
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    pass


# initial pages
page_sequence = []

# print ("Creating page sequence")
for row in read_csv():
    form_fields = [f"q{row['question_nr_exp']}"]
    cl = type(f"Page{row['question_nr_exp']}", (PageTemplate,), {'form_fields': form_fields})
    page_sequence.append(cl)

# add additional pages
page_sequence.append(Results)

