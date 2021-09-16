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
    # We can see if we can define arrays for this that we read from a CSV

    # Variables for Page0
    name = models.StringField(initial="1")
    age = models.IntegerField(initial=1)
    level = models.IntegerField(
        choices=[1, 2, 3],
        widget=widgets.RadioSelect,
        initial=1
    )

    # Variables for Page1
    name2 = models.StringField(initial="2")
    age2 = models.IntegerField(initial=2)
    level2 = models.StringField(
        choices=["Yes", "No", "Maybe"],
        widget=widgets.RadioSelect,
        initial="Maybe"
    )


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
    def before_next_page(player, timeout_happened):
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


class Page0(PageTemplate):
    # define with fields need to be filled in this survey page
    form_fields = ['name', 'age', 'level']


class Page1(PageTemplate):
    # define with fields need to be filled in this survey page
    form_fields = ['name2', 'age2', 'level2']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    pass


page_sequence = [Page0, Page1, Results]
