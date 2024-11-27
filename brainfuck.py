import random
import argparse


class Brainfuck2Python:
    def __init__(self, program):
        self.program = program
        self.code = ""
        self.loop_start_2_end = {}
        self.loop_end_2_start = {}
        self.bracket_stack = []
        self.errors = ""
        self.indent = 0

    def compile(self):
        self.code = "tape = [0 for _ in range(1000)]\npointer = 0\n\n"
        if not self.bracket_stacker():
            self.add_error(f"\033[0;31mError\033[0m: You didn't close a '['.\n")
            return self.errors
        else:
            i = 0
            pointer = 0
            while i < len(self.program):
                char = self.program[i]

                if char == "<":
                    pointer_move = -1
                    pointer -= 1
                    j = i + 1
                    while True:
                        if pointer >= 1000 or pointer < 0:
                            self.add_error(
                                f"\033[0;31mError\033[0m: Index out of bound at {j}"
                            )
                            break

                        if self.program[j] == "<":
                            pointer_move -= 1
                            pointer -= 1
                        elif self.program[j] == ">":
                            pointer_move += 1
                            pointer += 1
                        else:
                            break

                        j += 1
                    i = j - 1
                    self.add_code(f"pointer += {pointer_move}")
                elif char == ">":
                    pointer_move = 1
                    pointer += 1
                    j = i + 1
                    while True:
                        if pointer >= 1000 or pointer < 0:
                            self.add_error(
                                f"\033[0;31mError\033[0m: Index out of bound at {j}"
                            )
                            break

                        if self.program[j] == "<":
                            pointer_move -= 1
                        elif self.program[j] == ">":
                            pointer_move += 1
                        else:
                            break

                        j += 1
                    i = j - 1
                    self.add_code(f"pointer += {pointer_move}")
                elif char == "+":
                    addition = 1
                    j = i + 1
                    while True:
                        if self.program[j] == "+":
                            addition += 1
                        elif self.program[j] == "-":
                            addition -= 1
                        else:
                            break
                        j += 1
                    i = j - 1
                    self.add_code(f"tape[pointer] += {addition}")
                elif char == "-":
                    addition = -1
                    j = i + 1
                    while True:
                        if self.program[j] == "+":
                            addition += 1
                        elif self.program[j] == "-":
                            addition -= 1
                        else:
                            break
                        j += 1
                    i = j - 1
                    self.add_code(f"tape[pointer] += {addition}")
                elif char == ".":
                    self.add_code("print(chr(tape[pointer]), end='')")
                elif char == ",":
                    self.add_code("tape[pointer] = ord(input()[0])")
                elif char == "[":
                    self.add_code("while tape[pointer] != 0:")
                    self.indent_in()
                elif char == "]":
                    self.indent_out()
                elif char == "\n" or char == " ":
                    pass
                else:
                    # Error
                    pass
                i += 1

        if self.errors:
            return self.errors
        return self.code

    def add_code(self, new_line):
        self.code += ("\t" * self.indent) + new_line + "\n"

    def indent_in(self):
        self.indent += 1

    def indent_out(self):
        self.indent -= 1

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
                    self.loop_start_2_end[start] = end
                    self.loop_end_2_start[end] = start
                except IndexError:
                    self.add_error(
                        f"\033[0;31mError\033[0m: You closed a loop you never opened at line {line_count}!\n"
                    )
                    return False
            elif char == "\n":
                line_count += 1

            i += 1
        return False if self.bracket_stack else True

    def add_error(self, new_error):
        self.errors += new_error + "\n"


class BrainfuckInterpreter:
    def __init__(self, program):
        self.program = program
        self.output = ""
        self.loop_start_2_end = {}
        self.loop_end_2_start = {}
        self.bracket_stack = []

    def run(self):
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
                        i = self.loop_start_2_end[i] + 1
                elif char == "]":
                    if tape[pointer] != 0:
                        i = self.loop_end_2_start[i]
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
                    self.loop_start_2_end[start] = end
                    self.loop_end_2_start[end] = start
                except IndexError:
                    self.add_to_output(
                        f"\033[0;31mError\033[0m: You closed a loop you never opened at line {line_count}!\n"
                    )
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
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="run | compile")
    parser.add_argument("file", help="path to the program file")
    parser.add_argument("-o", "--output", help="path to output file")

    args = parser.parse_args()

    command = args.command
    file_path = args.file
    output_file = args.output

    program = ""

    try:
        if command == "run":
            with open(file_path, "r") as f:
                for line in f:
                    program += line
                bf = BrainfuckInterpreter(program)
                output = bf.run()

                if output_file:
                    with open(output_file, "w") as o:
                        o.write(output)
                else:
                    print(output)
        elif command == "compile":
            with open(file_path, "r") as f:
                for line in f:
                    program += line
                bf = Brainfuck2Python(program)
                output = bf.compile()

                if output_file:
                    with open(output_file, "w") as o:
                        o.write(output)
                else:
                    print(output)
        else:
            parser.print_help()
    except FileNotFoundError:
        print("\033[0;31mError\033[0m: File not found. Just like your brain.")
