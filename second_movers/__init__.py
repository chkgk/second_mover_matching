from otree.api import *
import csv
import itertools
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'second_movers'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    FIRST_MOVER_FILE = 'first_movers.csv'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # which type should the second mover be matched with
    match_with_type = models.StringField()

    # id and value from the matched first mover
    matched_with_id = models.StringField()
    first_mover_value = models.StringField()

    def get_first_mover_data(self):
        # select the correct list, A or B
        source = self.session.a_type_matches if self.match_with_type == 'A' else self.session.b_type_matches

        # ask the itertools generator to yield the next entry in the list
        first_mover = next(source)

        self.matched_with_id = first_mover['id']
        self.first_mover_value = first_mover['some_value']


# PAGES
class MyPage(Page):
    def before_next_page(player: Player, timeout_happened):
        player.get_first_mover_data()


class Results(Page):
    pass


# FUNCTIONS
def creating_session(subsession):
    # load the data from the csv into the subsession
    load_first_mover_data(subsession)

    # for this demo: assign each player a type to match with
    for player in subsession.get_players():
        player.match_with_type = random.choice(['A', 'B'])


def load_first_mover_data(subsession):
    a_type_matches = []
    b_type_matches = []
    # open the first mover file, read it line by line
    with open(C.FIRST_MOVER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # get the data from each line into a dictionary
            data = {'id': row['id'], 'some_value': row['some_value']}
            # separate the data into two lists, one for each type
            if row['match_with_type'] == 'A':
                a_type_matches.append(data)
            if row['match_with_type'] == 'B':
                b_type_matches.append(data)

    # make sure you have added the two variables in settings!
    subsession.session.vars['a_type_matches'] = itertools.cycle(a_type_matches)
    subsession.session.vars['b_type_matches'] = itertools.cycle(b_type_matches)


# PAGE SEQUENCE

page_sequence = [MyPage, Results]
