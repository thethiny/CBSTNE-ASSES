from random import random, randint
from typing import List, Set, TypedDict
import sys

class AdjustDict(TypedDict):
    type: str
    start: int
    end: int


class SnakeNLadders():
    MAX_GRID_SIZE = 100

    def __init__(self, n_players: int, snakes: List[AdjustDict], ladders: List[AdjustDict]):
        self.__init_board__(snakes, ladders)
        self.__init_players__(n_players)
        self.cur_turn = 0

    def __init_players__(self, n_players: int):
        self.n_players = n_players
        self.pos = {
            n: 0 for n in range(n_players)
        }

    def __init_board__(self, snakes: List[AdjustDict], ladders: List[AdjustDict]):
        board = {}
        for snake in snakes:
            board[snake["start"]] = {"type": "s", "end": snake["end"]}
        for ladder in ladders:
            board[ladder["start"]] = {"type": "l", "end": ladder["end"]}

        self.board = board

    def calc_new_position(self, player_id: int, move_amt: int):
        player_pos = self.pos.get(player_id, 0)
        new_pos = player_pos + move_amt

        if new_pos > self.MAX_GRID_SIZE:
            return player_pos

        while new_pos in self.board: # Stepping on some snake/ladder
            new_pos = self.board[new_pos]["end"]

        return new_pos

    def get_player_pos(self, player_id: int):
        return self.pos.get(player_id)


    def play_round(self):
        for player_id in range(self.n_players):
            self.play_round_player(player_id)
            pos = self.get_player_pos(player_id)
            if pos == self.MAX_GRID_SIZE:
                return player_id

        return None

    def play_round_player(self, player_id: int):
        dice_roll = self.get_dice_roll()
        new_pos = self.calc_new_position(player_id, dice_roll)
        self.pos[player_id] = new_pos
    
    @classmethod
    def get_dice_roll(cls):
        dice_roll = random.randint(0, 6) # 0 -> 6
        return dice_roll

    def play(self):
        winner = self.play_round()
        while winner is None:
            winner = self.play_round()

        return winner

def _get_rand_pos(min=1,max=100):
    return random.randint(min,max)

def generate_random_adjustments(n_snakes: int, n_ladders: int):
    Snakes: List[AdjustDict] = []
    Ladders: List[AdjustDict] = []
    starts = set()
    # snake_starts = set()
    cur_snakes = cur_ladders = 0
    while cur_snakes < n_snakes:
        rand_start: int = _get_rand_pos()
        while \
            rand_start in starts or \
            rand_start == SnakeNLadders.MAX_GRID_SIZE or \
            rand_start <= 1:

            rand_start = _get_rand_pos()
        
        starts.add(rand_start)

        rand_end: int = _get_rand_pos(1, rand_start-1)

        adjust: AdjustDict = {
            "type": "s",
            "start": rand_start,
            "end": rand_end
        }

        Snakes.append(adjust)
        cur_snakes += 1

    while cur_ladders < n_ladders:
        rand_start = _get_rand_pos()
        while rand_start in starts or rand_start == SnakeNLadders.MAX_GRID_SIZE:
            rand_start = _get_rand_pos()
        
        starts.add(rand_start)

        regenerate = True
        regen_ctr = 0
        rand_end = _get_rand_pos(rand_start+1, SnakeNLadders.MAX_GRID_SIZE)
        reset_ladder = False
        while regenerate: # Refactor into path traversal
            if regen_ctr >= 3:
                reset_ladder = True
                break
            if rand_end in starts: # 
                for snake in Snakes:
                    if snake["end"] == rand_start: # Infinite loop
                        regenerate = True
                        rand_end = _get_rand_pos(rand_start+1, SnakeNLadders.MAX_GRID_SIZE)
                        regen_ctr += 1
                        continue
            regenerate = False
        if reset_ladder:
            continue
        
        adjust: AdjustDict = {
            "type": "l",
            "start": rand_start,
            "end": rand_end
        }

        Ladders.append(adjust)
        cur_ladders += 1

    return Snakes, Ladders
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please specify snake n ladder amts")
        exit(1)
    snakes, ladders = sys.argv[1:]
    snake_amt = random.randint(int(snakes))
    ladders_amt = random.randint(int(ladders))

    snakes, ladders = generate_random_adjustments(snake_amt, ladders_amt)
    game = SnakeNLadders(4, snakes, ladders)
    winner = game.play() # Game Loop
    print(f"The winner is Player #{winner}")