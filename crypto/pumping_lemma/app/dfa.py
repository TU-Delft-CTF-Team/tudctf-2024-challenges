class Dfa:
    def __init__(self, states: set[str], alphabet: str, transitions: dict[(str, str), str], start_state: str, accepting_states: set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states
        if not self.verify():
            raise ValueError('Invalid DFA')
    
    def verify(self) -> bool:
        return self.accepting_states.issubset(self.states) and self.start_state in self.states and self.verify_transitions()
    
    def verify_transitions(self) -> bool:
        for ((s, c), t) in self.transitions.items():
            if s not in self.states or c not in self.alphabet or t not in self.states:
                return False
        return True
    
    def accepts(self, word: str) -> bool:
        if any([c not in self.alphabet for c in word]):
            return False
        current_state = self.start_state

        for c in word:
            current_state = self.transitions.get((current_state, c))
            if current_state is None:
                return False
        return current_state in self.accepting_states
