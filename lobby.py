from datetime import datetime
from collections import namedtuple

class ClassPlayers:
  """The players playing one class on a team."""

  # Enumeration over all classes.
  PYRO = 'pyro'
  ENGINEER = 'engineer'
  SPY = 'spy'
  HEAVY = 'heavy'
  SNIPER = 'sniper'
  SCOUT = 'scout'
  SOLDIER = 'soldier'
  DEMOMAN = 'demoman'
  MEDIC = 'medic'

  def __init__(self, max_players):
    self.class_name = class_name
    self.max_players = max_players
    self.players = []

  def add_player(self, player):
    if player in self.players:
      # Programming defensively.
      return True
    elif self.num_players() < self.max_players:
      self.players.add(player)
      return True
    return False

  def remove_player(self, player):
    try:
      self.players.remove(player)
      return True
    except ValueError:
      return False

  def num_players(self):
    """The number of players for this class."""
    return len(self.players)


class Team:
  """The players playing on a team."""

  def __init__(self, class_counts):
    self.max_players = sum(class_counts.itervalues())
    self.all_class_players = {}
    for class_name, class_count in class_counts.iteritems():
      self.all_class_players[class_name] = ClassPlayers(class_count)

  def add_player(self, player, class_name):
    # The player might be switching classes.
    self.remove_player(player)

    class_players = self.all_class_players.get(class_name, None)
    if class_players is None:
      # This class is not allowed.
      return False
    return class_players.add_player(player)
 
  def remove_player(self, player):
    for class_players in self.all_class_players.itervalues():
      if class_players.remove_player(player):
        return True
    return False

  def max_players(self):
    """Returns the maximum number of players on this team."""
    return self.max_players

  def num_players(self):
    """The number of players on this team."""
    return sum(class_players.num_players()
        for class_players in self.all_class_players.itervalues())


# The number of players allowed per class in sixes.
_SIXES_CLASS_COUNTS = {
    Class.MEDIC : 1,
    Class.DEMOMAN : 1,
    Class.SOLDIER: 2,
    Class.SCOUT: 2
}

def get_sixes_team():
  return Team(_SIXES_CLASS_COUNTS)
 
# The number of players allowed per class in Highlander.
_HIGHLANDER_CLASS_COUNTS = {
    Class.PYRO: 1,
    Class.MEDIC: 1,
    Class.ENGINEER: 1,
    Class.SPY: 1,
    Class.HEAVY: 1,
    Class.SNIPER: 1,
    Class.SCOUT: 1,
    Class.SOLDIER: 1,
    Class.DEMOMAN: 1,
}

def get_highlander_team():
  return Team(_HIGHLANDER_CLASS_COUNTS)


class PlayerStatus:
  """Base class for the status of a player."""

  def __init__(self, status, lobby):
    self.status = status
    self.lobby = lobby

class IdleStatus(PlayerStatus):
  """Status when a player is idling in a lobby."""

  STATUS = 'idle'

  def __init__(self, lobby):
    PlayerStatus.__init__(self, STATUS, lobby)

class JoinedTeamStatus(PlayerStatus):
  """Status when a player has joined a team in a lobby."""

  STATUS = 'joined_team'

  def __init__(self, lobby, team, class_name):
    PlayerStatus.__init__(self, STATUS, lobby)
    self.team = team
    self.class_name = class_name


ChatMessage = namedtuple('ChatMessage', ['player', 'message', 'timestamp'])

class Lobby:
  # Enumeration over both game types.
  SIXES = '6v6'
  HIGHLANDER = 'HL'

  # Enumeration over both teams.
  RED_TEAM = 'red'
  BLU_TEAM = 'blu'

  def __init__(self, lobby_type, name, private=False):
    self.lobby_type = lobby_type
    self.name = name
    self.private = private

    self.idle_players = []
    if lobby_type == SIXES:
      self.red_team = get_sixes_team()
      self.blu_team = get_sixes_team()
    elif lobby_type = HIGHLANDER:
      self.red_team = get_highlander_team()
      self.blu_team = get_highlander_team()
    else:
      raise ValueError("Invalid lobby type: %s" % lobby_type)
    self.chat_history = []

  def _get_team(self, team_name):
    if team_name == RED_TEAM:
      return self.red_team, self.blu_team
    elif team_name == BLU_TEAM:
      return self.blu_team, self.red_team
    else:
      raise ValueError("Invalid team name: %s" % team_name)

  def add_player(self, player):
    # Programming defensively.
    self.remove_player(player)
    self.idle_players.add(player)

  def join_team(self, player, team_name, class_name):
    team, other_team = self._get_team(team_name)
    # The player might be switching teams.
    other_team.remove_player(player)
    return team.add_player(player, class_name)

  def leave_team(self, player):
    self.red_team.remove_player(player)
    self.blu_team.remove_player(player)

  def remove_player(self, player):
    # TODO
    pass

  def append_message(self, player, message, now=None):
    if now is None:
      now = datetime.utcnow()
    self.chat_history.append(ChatMessage(player, message, now))

  def max_players(self):
    """Returns the maximum number of players in this lobby."""
    return self.blu_team.max_players() + self.red_team.max_players()

  def num_players(self):
    """The number of players in this lobby."""
    return self.blu_team.num_players() + self.red_team.num_players()

