# CHIP-8 Interpreter

This was my first experience writing an interpreter and studying real low-level programming, emulation and basics concepts of operation systems and computer science.

## About the project

I made this interpreter after see some videos of retro videogames emulators and how was gaming programming in the old devices with limited hardware. I got curious, so I did a little digging and noted that writing a CHIP-8 interpreter was the "hello world" of emulators programming. Willing to learn more about computer science and OS fundamentals, I decided to program my very own CHIP-8 interpreter using python.

#### CHIP-8

From the [Cowgod's CHIP-8 technical reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#2.2):
<cite>
Chip-8 is a simple, interpreted, programming language which was first used on some do-it-yourself computer systems in the late 1970s and early 1980s. The COSMAC VIP, DREAM 6800, and ETI 660 computers are a few examples. These computers typically were designed to use a television as a display, had between 1 and 4K of RAM, and used a 16-key hexadecimal keypad for input. The interpreter took up only 512 bytes of memory, and programs, which were entered into the computer in hexadecimal, were even smaller.
</cite>

As an interpreted language, CHIP-8 runs on a virtual machine responsible to offer computer resources and translate the <i>.ch8</i> binary files to native instructions that can be executed by the computer. The virtual machine has 16 8-bit data registers, one call stack, two timers (one for delay and other for sounds), 4Kb of memory and must have access to I/O devices such as keyboard for input and graphics/sound for output.

#### The interpreter

My interpreter is pretty simple: the virtual machine CPU stores a <i>.ch8</i> ROM in memory, then reads every pair of bytes (because each opcode is 2 bytes long) starting at 0x200 address (the first 512 bytes of memory were reserved for the original interpreter, then the actual programs start after 0x200) and map the instruction hex identifier (called as opcode) with an function that implements the specification for that opcode.

All the 35 original opcodes of Chip-8 have their implementations written in python, and for those that need input/output support I used the [pygame](ttps://www.pygame.org) module.

## How to install & use

#### Requirements

- python3
- pip

#### Setup

Clone the repository

```bash
git clone https://github.com/VitorValandro/chip-8-interpreter
```

Go to project's root directory and install the dependencies (if you want to, create a virtualenv before):

```bash
pip install -r requirements.txt
```

#### Usage

To run the interpreter, just run the `main.py` file. The default ROM is the game `breakout`, which the `.ch8` file path is mocked in the code.

There are a couple ROMs ready in the `/roms` dir, but you can download any `.ch8` ROM and then just update the file path in the `main.py` file. [Here is a source of chip-8 games and programs.](https://github.com/kripod/chip8-roms)

### Project finished

This interpreter works fine and I'm satisfied with the final result, so I don't think that is anything I'd like to add that will be of great impact. I really learned a lot about interpreters, operation systems and emulators, and now I can finally say that I actually understand the difference of compiled and interpreted programming languages.

After having so much fun programming this, I intend to level up and program a more complex emulator or a compiler in the future.

###### Vitor Matheus Valandro da Rosa. July 2022.
