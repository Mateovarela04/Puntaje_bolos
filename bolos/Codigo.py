from abc import ABC, abstractmethod


class Game:
    def __init__(self):
        self.frames = []
        self.extra_roll = None

    def roll(self, pins: int):
        if self.extra_roll is not None:
            self.extra_roll.pins += pins
            self.extra_roll = None
        else:
            frame = self.frames[-1]
            if frame.is_strike():
                self.extra_roll = Roll(pins)
            else:
                frame.add_roll(pins)

    def score(self) -> int:
        total_score = 0
        for frame in self.frames:
            if frame.is_strike():
                total_score += 10
            elif frame.is_spare():
                total_score += 10 + frame.next_roll
            else:
                total_score += frame.roll1 + frame.roll2
        return total_score


class Frame(ABC):  # Clase abstracta
    def __init__(self):
        self.rolls = []

    @abstractmethod
    def add_roll(self, pins: int):
        pass

    @abstractmethod
    def score(self) -> int:
        pass

    def is_strike(self) -> bool:
        return self.rolls[0].pins == 10

    def is_spare(self) -> bool:
        return self.rolls[0].pins + self.rolls[1].pins == 10


class Roll:
    def __init__(self, pins):
        self.pins = pins


class Normal_frame(Frame):  # Hereda de la clase Frame
    def add_roll(self, pins: int):
        self.rolls.append(Roll(pins))

    def score(self) -> int:
        return sum(roll.pins for roll in self.rolls)


class Tenth_Frame(Frame):  # Hereda de la clase Frame
    def add_roll(self, pins: int):
        self.rolls.append(Roll(pins))
        if self.is_strike() and len(self.rolls) == 1:
            self.rolls.append(Roll(0))
        elif self.is_spare() and len(self.rolls) == 2:
            self.rolls.append(Roll(0))

    def score(self) -> int:
        return sum(roll.pins for roll in self.rolls)
