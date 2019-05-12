import random
from .exceptions import *


class GuessAttempt(object):
    def __init__(self, character, miss=None, hit=None):
#         self.game = game
        
        if miss and hit:
            raise InvalidGuessAttempt('Invalid Attempt')
        
        self.character = character
        self.miss = miss
        self.hit = hit
        
    def is_miss(self):
        return bool(self.miss)
        
    def is_hit(self):
        return bool(self.hit)
        

class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException('Please enter a word')
    
        self.answer = word.lower()
        self.masked = self._mask_word(self.answer)
    
    def perform_attempt(self, character):
        self.character = character.lower()
        if len(self.character) > 1:
            raise InvalidGuessedLetterException('That letter is invalid.')
            
        unmasked = self.masked
        if self.character in self.answer:
            for idx, char in enumerate(self.answer):
                if self.character == char:
                    unmasked = self.masked[:idx] + char + self.masked[idx+1:]
                self.masked = unmasked.lower()
            return GuessAttempt(character, hit=True)
        else:   
            return GuessAttempt(character, miss=True)

    def _mask_word(self, word):
        if not word:
            raise InvalidWordException('That word is invalid.')
        return '*' * len(self.answer)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']    
    
    def __init__(self, word_list=None, number_of_guesses=5):
        self.number_of_guesses = number_of_guesses
        
        if not word_list:
                word_list = self.WORD_LIST
        
        self.word = GuessWord(self.select_random_word(word_list))
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
    
    def is_won(self):
        return self.word.masked == self.word.answer
    
    def is_lost(self):
        return self.word.masked != self.word.answer and self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    def guess(self, character):
        self.character = character.lower()
        
        if self.character not in self.previous_guesses:
            self.previous_guesses.append(self.character)
        else:
            raise InvalidGuessedLetterException()
        
        if self.is_finished():
            raise GameFinishedException('Game over.')
            
        attempt = self.word.perform_attempt(self.character)
        
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException('You won!')
            
        if self.is_lost():
            raise GameLostException('You lose!')
        
        return attempt
       
    @classmethod
    def select_random_word(cls, word_list=None):
        if not word_list:
            raise InvalidListOfWordsException('Must enter a word')

        return random.choice(word_list)
      
