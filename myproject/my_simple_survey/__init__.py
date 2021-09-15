from otree.api import *


doc = """
Demo of Simple Survey
"""


class Constants(BaseConstants):
    name_in_url = 'my_simple_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()
    age = models.IntegerField()
    level = models.IntegerField(
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )

    name2 = models.StringField()
    age2 = models.IntegerField()
    level2 = models.StringField(
        choices=["Yes", "No", "Maybe"],
        widget=widgets.RadioSelect
    )

# PAGES


class PageTemplate(Page):
    images = ["python.jpg", "puppy.jpg"]
    form_model = 'player'
    template_name = 'my_simple_survey/MyPage.html'

    def vars_for_template(player, page_nr=0):
        return dict(
            img="puppy.jpg",
            page=self.page_nr
        )


# TODO: herhaling van template Pages voorkomen
# TODO: herhaling van de velden voorkomen
class MyPage(PageTemplate):
    # TODO Page nr door geven
    page_nr = 0
    form_fields = ['name', 'age', 'level']


class MyPage2(PageTemplate):
    page_nr = 1
    form_fields = ['name2', 'age2', 'level2']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    # No form
    pass


page_sequence = [MyPage, MyPage2, Results]
