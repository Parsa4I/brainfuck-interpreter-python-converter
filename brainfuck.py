import sys
import random


class Brainfuck:
    def __init__(self, program):
        self.program = program
        self.output = ""
        self.for_start_2_end = {}
        self.for_end_2_start = {}
        self.bracket_stack = []

    def evaluate(self):
        self.output = ""
        if not self.bracket_stacker():
            for _ in self.bracket_stack:
                self.add_to_output(f"\033[0;31mError\033[0m: You didn't close a '['.\n")
            self.add_err_msg()
        else:
            tape = [0 for _ in range(1000)]
            pointer = 0
            i = 0
            line_count = 1
            while i < len(self.program):
                char = self.program[i]

                if char == "<":
                    pointer -= 1
                    if pointer < 0:
                        self.add_to_output(
                            f"\033[0;31mError\033[0m: Index out of range at line {line_count}.\n"
                        )
                        self.add_err_msg()
                        break
                elif char == ">":
                    pointer += 1
                    if pointer >= 1000:
                        self.add_to_output(
                            f"\033[0;31mError\033[0m: Index out of range at line {line_count}\n"
                        )
                        self.add_err_msg()
                        break
                elif char == "+":
                    tape[pointer] += 1
                elif char == "-":
                    tape[pointer] -= 1
                elif char == ".":
                    self.add_to_output(chr(tape[pointer]))
                elif char == ",":
                    input_char = input()
                    tape[pointer] = ord(input_char[0])
                elif char == "[":
                    if tape[pointer] == 0:
                        i = self.for_start_2_end[i] + 1
                elif char == "]":
                    if tape[pointer] != 0:
                        i = self.for_end_2_start[i]
                elif char == "\n":
                    line_count += 1
                elif char == " ":
                    pass
                else:
                    self.add_to_output(
                        f"\033[0;31mError\033[0m: What the hell is a '{char}'?\n"
                    )
                    self.add_to_output(
                        "I see you're inventing a new language here. Unfortunately, it's not one I speak.\n"
                    )
                    break

                i += 1
        return self.output

    def bracket_stacker(self):
        i = 0
        self.bracket_stack = []
        line_count = 1
        while i < len(self.program):
            char = self.program[i]

            if char == "[":
                self.bracket_stack.append(i)
            elif char == "]":
                try:
                    start = self.bracket_stack.pop()
                    end = i
                    self.for_start_2_end[start] = end
                    self.for_end_2_start[end] = start
                except IndexError:
                    self.add_to_output(
                        f"\033[0;31mError\033[0m: You closed a loop you never opened at  line {line_count}!\n"
                    )
                    self.add_err_msg()
                    return False
            elif char == "\n":
                line_count += 1

            i += 1
        return False if self.bracket_stack else True

    def add_err_msg(self):
        messages = [
            "Coding is hard, isn't it?",
            "A fine attempt… if you weren't trying to write code.",
            "That is a f*** up of not-insignicant proportions.",
            "You're stupid of something?",
            "I'm not angry. Just… disappointed.",
            "Coding isn't for everyone after all.",
            "I've seen bugs. But this… this is something else entirely.",
            "Guess you're just having a bad day.",
        ]

        msg_index = random.randint(0, len(messages) - 1)
        self.output += messages[msg_index] + "\n"

    def add_to_output(self, new_output):
        self.output += new_output


if __name__ == "__main__":
    program = ""
    try:
        with open(sys.argv[1], "r") as f:
            for line in f:
                program += line
        bf = Brainfuck(program)
        output = bf.evaluate()
        print(output)
    except FileNotFoundError:
        print("\033[0;31mError\033[0m: File not found. Just like your brain.")
