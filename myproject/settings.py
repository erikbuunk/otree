from os import environ

SESSION_CONFIGS = [
    dict(
        name='my_simple_survey',
        num_demo_participants=2,
        app_sequence=['my_simple_survey'],
        time_pressure=True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4526688996736'
PARTICIPANT_FIELDS = ['expiry',
                      'is_dropout',
                      'payoff_employee',
                      'trust_bonus',
                      'randomroundnumber',
                      'computers_probability',
                      #ArtLit Values
                      'q2payoff',
                      'q4payoff',
                      'q6payoff',
                      'q13payoff',
                      'q19payoff',
                      'q21payoff',
                      'q74payoff',
                      'q75payoff',
                      'q76payoff',
                      'q81payoff',
                      'q2advicepayoff',
                      'q4advicepayoff',
                      'q6advicepayoff',
                      'q13advicepayoff',
                      'q19advicepayoff',
                      'q21advicepayoff',
                      'q74advicepayoff',
                      'q75advicepayoff',
                      'q76advicepayoff',
                      'q81advicepayoff',
                      'q2adviceeliminatedpayoff',
                      'q4adviceeliminatedpayoff',
                      'q6adviceeliminatedpayoff',
                      'q13adviceeliminatedpayoff',
                      'q19adviceeliminatedpayoff',
                      'q21adviceeliminatedpayoff',
                      'q74adviceeliminatedpayoff',
                      'q75adviceeliminatedpayoff',
                      'q76adviceeliminatedpayoff',
                      'q81adviceeliminatedpayoff',
                      'q2adviceeliminateddebt',
                      'q4adviceeliminateddebt',
                      'q6adviceeliminateddebt',
                      'q13adviceeliminateddebt',
                      'q19adviceeliminateddebt',
                      'q21adviceeliminateddebt',
                      'q74adviceeliminateddebt',
                      'q75adviceeliminateddebt',
                      'q76adviceeliminateddebt',
                      'q81adviceeliminateddebt',

                      #SciTech Values
                      'q50payoff',
                      'q52payoff',
                      'q59payoff',
                      'q60payoff',
                      'q88payoff',
                      'q90payoff',
                      'q101payoff',
                      'q92payoff',
                      'q97payoff',
                      'q98payoff',
                      'q50advicepayoff',
                      'q52advicepayoff',
                      'q59advicepayoff',
                      'q60advicepayoff',
                      'q88advicepayoff',
                      'q90advicepayoff',
                      'q101advicepayoff',
                      'q92advicepayoff',
                      'q97advicepayoff',
                      'q98advicepayoff',
                      'q50adviceeliminatedpayoff',
                      'q52adviceeliminatedpayoff',
                      'q59adviceeliminatedpayoff',
                      'q60adviceeliminatedpayoff',
                      'q88adviceeliminatedpayoff',
                      'q90adviceeliminatedpayoff',
                      'q101adviceeliminatedpayoff',
                      'q92adviceeliminatedpayoff',
                      'q97adviceeliminatedpayoff',
                      'q98adviceeliminatedpayoff',
                      'q50adviceeliminateddebt',
                      'q52adviceeliminateddebt',
                      'q59adviceeliminateddebt',
                      'q60adviceeliminateddebt',
                      'q88adviceeliminateddebt',
                      'q90adviceeliminateddebt',
                      'q101adviceeliminateddebt',
                      'q92adviceeliminateddebt',
                      'q97adviceeliminateddebt',
                      'q98adviceeliminateddebt',

                      #PsyLing Values
                      'q67payoff',
                      'q69payoff',
                      'q71payoff',
                      'q72payoff',
                      'q133payoff',
                      'q134payoff',
                      'q135payoff',
                      'q137payoff',
                      'q97payoff',
                      'q145payoff',
                      'q67advicepayoff',
                      'q69advicepayoff',
                      'q71advicepayoff',
                      'q72advicepayoff',
                      'q133advicepayoff',
                      'q134advicepayoff',
                      'q135advicepayoff',
                      'q137advicepayoff',
                      'q142advicepayoff',
                      'q145advicepayoff',
                      'q67adviceeliminatedpayoff',
                      'q69adviceeliminatedpayoff',
                      'q71adviceeliminatedpayoff',
                      'q72adviceeliminatedpayoff',
                      'q133adviceeliminatedpayoff',
                      'q134adviceeliminatedpayoff',
                      'q135adviceeliminatedpayoff',
                      'q137adviceeliminatedpayoff',
                      'q142adviceeliminatedpayoff',
                      'q145adviceeliminatedpayoff',
                      'q67adviceeliminateddebt',
                      'q69adviceeliminateddebt',
                      'q71adviceeliminateddebt',
                      'q72adviceeliminateddebt',
                      'q133adviceeliminateddebt',
                      'q134adviceeliminateddebt',
                      'q135adviceeliminateddebt',
                      'q137adviceeliminateddebt',
                      'q142adviceeliminateddebt',
                      'q145adviceeliminateddebt',

                      'confidence_win',
                      'advice_payoff',
                      'random_number',
                      'randomnumber', #complained in PsyLing Quiz about the _, in code indeed the variable is defined without
                      'result_number',
                      'quiztype',
                      'coefficient',
                      'total_cost',
                      'number_advice',
                      'sum_correct',
                      'number_correct',
                      'total_payoff',
                      'totalpayoff', #complained in PsyLing Quiz about the _, in code indeed the variable is defined without, puzzing, run in SciTech
                      'Prolific_ID',

                      ### Correct Answers
                      'q50_anscorrect',
                      'q52_anscorrect',
                      'q59_anscorrect',
                      'q60_anscorrect',
                      'q88_anscorrect',
                      'q90_anscorrect',
                      'q101_anscorrect',
                      'q92_anscorrect',
                      'q97_anscorrect',
                      'q98_anscorrect',
                      'newpayoff',

                      ### Correct Answers
                      'q67_anscorrect',
                      'q69_anscorrect',
                      'q71_anscorrect',
                      'q72_anscorrect',
                      'q133_anscorrect',
                      'q134_anscorrect',
                      'q135_anscorrect',
                      'q137_anscorrect',
                      'q142_anscorrect',
                      'q145_anscorrect',

                      #Marina New Variables
                      'dummyadvice',
                      'number_correct_before',
                      'number_correct_after'
                      ]