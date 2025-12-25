class AI:
    def __init__(self, target_board, difficulty="Medium"):
        """
        target_board: Board instance representing opponent (player) board the AI will shoot at
        difficulty: "Easy", "Medium", or "Hard"
        """
        self.board = target_board
        self.difficulty = difficulty
        self.previous_guesses = set()
        self.hit_positions = []
        self.sunk_ships = []

    def make_guess(self):
        """Return a guess (row,col) according to difficulty and current hit info."""
        if self.difficulty == "Easy":
            # almost pure random — no targeting follow-up
            guess = self._random_guess()
            self.previous_guesses.add(guess)
            return guess

        if self.difficulty == "Medium":
            # basic behavior: follow-up on hits, otherwise random
            if self.hit_positions:
                guess = self._target_surroundings()
                if guess is not None:
                    self.previous_guesses.add(guess)
                    return guess
            guess = self._random_guess()
            self.previous_guesses.add(guess)
            return guess

        # Hard difficulty: smarter guessing strategy
        # 1) If have known hits, pursue them (try to determine orientation and finish ship)
        # 2) Otherwise use parity / probability: prefer cells on a checkerboard to find ships faster
        if self.difficulty == "Hard":
            if self.hit_positions:
                # try to finish off current cluster first
                guess = self._target_surroundings(prefer_along_line=True)
                if guess is not None:
                    self.previous_guesses.add(guess)
                    return guess
            # parity-based hunt: choose cells where (r+c) % 2 == 0 first
            guess = self._parity_guess()
            self.previous_guesses.add(guess)
            return guess

    def _random_guess(self):
        import random
        while True:
            guess = (random.randint(0, self.board.size - 1), random.randint(0, self.board.size - 1))
            if guess not in self.previous_guesses:
                return guess

    def _target_surroundings(self):
        # try neighbors of the most recent hit(s)
        return self._target_surroundings(prefer_along_line=False)

    def _target_surroundings(self, prefer_along_line=False):
        # try neighbors of known hits. If prefer_along_line=True, try to continue in the inferred orientation.
        if not self.hit_positions:
            return None
        # if multiple hit positions, try to infer orientation
        if len(self.hit_positions) >= 2:
            hs = sorted(self.hit_positions)
            # if aligned in a row (same r) or column (same c)
            if hs[0][0] == hs[-1][0]:
                r = hs[0][0]
                cols = [c for (_, c) in hs]
                # try extend left/right
                left = (r, min(cols) - 1)
                right = (r, max(cols) + 1)
                for guess in (left, right):
                    if self.board.is_within_bounds(guess) and guess not in self.previous_guesses:
                        return guess
            if hs[0][1] == hs[-1][1]:
                c = hs[0][1]
                rows = [r for (r, _) in hs]
                up = (min(rows) - 1, c)
                down = (max(rows) + 1, c)
                for guess in (up, down):
                    if self.board.is_within_bounds(guess) and guess not in self.previous_guesses:
                        return guess

        # fallback: try neighbors around most recent hit(s)
        for last_hit in reversed(self.hit_positions):
            potential_guesses = [
                (last_hit[0] + 1, last_hit[1]),
                (last_hit[0] - 1, last_hit[1]),
                (last_hit[0], last_hit[1] + 1),
                (last_hit[0], last_hit[1] - 1)
            ]
            for guess in potential_guesses:
                if self.board.is_within_bounds(guess) and guess not in self.previous_guesses:
                    return guess
        return None

    def _parity_guess(self):
        # choose a random cell on parity grid (checkerboard) not previously guessed
        import random
        candidates = []
        for r in range(self.board.size):
            for c in range(self.board.size):
                if (r + c) % 2 == 0 and (r, c) not in self.previous_guesses:
                    candidates.append((r, c))
        if not candidates:
            return self._random_guess()
        return random.choice(candidates)

    def record_result(self, guess, result):
        if result == "hit":
            # track hit for follow-up
            if guess not in self.hit_positions:
                self.hit_positions.append(guess)
        elif result == "sunk":
            # clear known hits (ship finished)
            self.sunk_ships.append(guess)
            self.hit_positions = []