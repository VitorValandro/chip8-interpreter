from random import random


class CPU:
    def __init__(self, renderer, keyboard, speaker):
        self.renderer = renderer
        self.keyboard = keyboard
        self.speaker = speaker

        self.memory = [0] * 4096
        self.v = [0] * 16
        self.i = 0
        self.pc = 0x200
        self.stack = [0] * 16
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.paused = False
        self.speed = 10

        self.opcode = 0
        self.x = 0
        self.y = 0

        self.instructions = {
            0x0000: self.CLS,
            0x000e: self.RET,
            0x1000: self.JUMP_addr,
            0x2000: self.CALL,
            0x3000: self.SE_vx_byte,
            0x4000: self.SNE_vx_byte,
            0x5000: self.SE_vx_vy,
            0x6000: self.LD_vx_byte,
            0x7000: self.ADD_vx_byte,
            0x8000: self.LD_vx_vy,
            0x8001: self.OR_vx_vy,
            0x8002: self.AND_vx_vy,
            0x8003: self.XOR_vx_vy,
            0x8004: self.ADD_vx_vy,
            0x8005: self.SUB_vx_vy,
            0x8006: self.SHR_vx,
            0x8007: self.SUBN_vx_vy,
            0x800e: self.SHL_vx,
            0x9000: self.SNE_vx_vy,
            0xa000: self.LD_I_addr,
            0xb000: self.JP_v0_addr,
            0xc000: self.RND_vx_byte,
            0xd000: self.DRW_vx_vy,
            0xe09e: self.SKP_vx,
            0xe0a1: self.SKNP_vx,
            0xf007: self.LD_vx_DT,
            0xf00a: self.LD_vx_K,
            0xf015: self.LD_DT_vx,
            0xf018: self.LD_ST_vx,
            0xf01e: self.ADD_I_vx,
            0xf029: self.LD_F_vx,
            0xf033: self.LD_B_vx,
            0xf055: self.LD_I_vx,
            0xf065: self.LD_vx_I,
        }

    def load_data(self, file, offset):
        data = open(file, 'rb').read()
        for index, byte in enumerate(data):
            self.memory[offset + index] = byte

    def load_sprites(self):
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for i in range(len(sprites)):
            self.memory[i] = sprites[i]

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
    
    def play_sound(self):
        if self.sound_timer > 0:
            self.speaker.play();
        else:
            self.speaker.stop();

    def CLS(self):
        # limpa a tela
        self.renderer.clear()

    def RET(self):
        # retorna de uma subrotina
        self.pc = self.stack.pop()

    def JUMP_addr(self):
        # pula o contador de programa para o endereço nnn
        self.pc = (self.opcode & 0xFFF)

    def CALL(self):
        # chama a subrotina do endereço nnn
        
        # primeiro, armazena a execução atual no topo da pilha
        self.stack.append(self.pc)
        # depois, pula para a execução da subrotina em nnn
        self.pc = (self.opcode & 0xFFF)

    def SE_vx_byte(self):
        # pula a próxima instrução se vx == byte
        # byte = nn, os últimos 2 nibbles, como em 0x00FF
        if self.v[self.x] == (self.opcode & 0xFF):
            self.pc += 2

    def SNE_vx_byte(self):
        # pula a próxima instrução se vx != byte
        # byte = nn, os últimos 2 nibbles, como em 0x00FF
        if self.v[self.x] != (self.opcode & 0xFF):
            self.pc += 2

    def SE_vx_vy(self):
        # pula a próxima instrução se vx == vy
        if self.v[self.x] == self.v[self.y]:
            self.pc += 2

    def LD_vx_byte(self):
        # atribui o valor de vx para o valor de byte
        # byte = nn, os últimos 2 nibbles, como em 0x00FF
        self.v[self.x] = (self.opcode & 0xFF)

    def ADD_vx_byte(self):
        # soma o valor de byte com o atual valor de vx
        # byte = nn, os últimos 2 nibbles, como em 0x00FF
        self.v[self.x] += (self.opcode & 0xFF)
        self.v[self.x] %= 256

    def LD_vx_vy(self):
        # atribui o valor de vx para o valor de vy
        self.v[self.x] = self.v[self.y]

    def OR_vx_vy(self):
        # armazena o valor da operação (vx OU vy) em vx
        self.v[self.x] |= self.v[self.y]

    def AND_vx_vy(self):
        # armazena o valor da operação (vx E vy) em vx
        self.v[self.x] &= self.v[self.y]

    def XOR_vx_vy(self):
        # armazena o valor da operação (vx XOR vy) em vx
        self.v[self.x] ^= self.v[self.y]

    def ADD_vx_vy(self):
        # soma o valor de vy com o atual valor de vx
        self.v[0xF] = 0
        total = self.v[self.x] + self.v[self.y]

        # se a soma for maior que 8 bits, atribui VF = 1
        # senão, VF continua 0
        if total > 255:
            self.v[0xF] = 1
            total -= 256
        self.v[self.x] = total

    def SUB_vx_vy(self):
        # subtrai de vx o valor de vy, armazena o resultado em vx
        self.v[0xF] = 1
        difference = self.v[self.x] - self.v[self.y]

        # se o resultado for negativo, atribui VF = 0
        # senão, VF continua 1
        if difference < 0:
            self.v[0xF] = 0
            difference += 256
        self.v[self.x] = difference

    def SHR_vx(self):
        # guarda em VF o valor do bit menos significativo de Vx
        self.v[0xF] = (self.v[self.x] & 0x1)

        # depois, divide Vx por 2
        self.v[self.x] = self.v[self.x] >> 1

    def SUBN_vx_vy(self):
        # subtrai de vy o valor de vx, armazena o resultado em vx
        self.v[0xF] = 1
        difference = self.v[self.y] - self.v[self.x]

        # se o resultado for negativo, atribui VF = 0
        # senão, VF continua 1
        if difference < 0:
            self.v[0xF] = 0
            difference += 256
        self.v[self.x] = difference

    def SHL_vx(self):
        # guarda em VF o valor to bit mais significativo de vx
        self.v[0xF] = (self.v[self.x] >> 7) & 1

        # depois, multiplica vx por 2
        self.v[self.x] = self.v[self.x] << 1

    def SNE_vx_vy(self):
        # pula a próxima instrução se vx != vy
        if self.v[self.x] != self.v[self.y]:
            self.pc += 2

    def LD_I_addr(self):
        # atribui o valor de nnn no registrador I
        self.i = (self.opcode & 0xFFF)

    def JP_v0_addr(self):
        # pula o contador de programa para nnn + valor do registrador 0 (v0)
        self.pc = (self.opcode & 0xFFF) + self.v[0x0]

    def RND_vx_byte(self):
        # gera um número aleatório entre 0 e 255;
        # realiza a operação de AND com o valor de nn;
        # guarda o resultado em vx
        rand = int(random() * 256)
        self.v[self.x] = rand & (self.opcode & 0xFF)

    def DRW_vx_vy(self):
        # desenha na tela um sprite de n bytes começando em I
        # deve-se atribuir VF = 1 se um pixel foi apagado
        width = 8
        height = (self.opcode & 0xF)
        self.v[0xF] = 0

        for row in range(height):
            sprite = self.memory[self.i + row]

            for col in range(width):
                if (sprite & 0x80) != 0:
                    if (
                        self.renderer.setPixel(
                            self.v[self.x] + col,
                            self.v[self.y] + row
                        )
                    ):
                        self.v[0xF] = 1
                sprite = sprite << 1

    def SKP_vx(self):
        # pula a próxima instrução se a tecla guardada em vx está pressionada
        if self.keyboard.isKeyPressed(self.v[self.x]):
            self.pc += 2

    def SKNP_vx(self):
        # pula a próxima instrução se a tecla guardada em vx NÃO está pressionada
        if not self.keyboard.isKeyPressed(self.v[self.x]):
            self.pc += 2

    def LD_vx_DT(self):
        # atribui à vx o valor atual de delay_timer
        self.v[self.x] = self.delay_timer

    def LD_vx_K(self):
        # para a execução do programa até alguma tecla ser pressionada
        # quando pressionada, armazena o valor da tecla em vx

        def storeAndResume(key):
            self.v[self.x] = key
            self.paused = False

        self.paused = True
        self.keyboard.onNextKeyPress = storeAndResume

    def LD_DT_vx(self):
        # atribui ao delay_timer o valor guardado em vx
        self.delay_timer = self.v[self.x]

    def LD_ST_vx(self):
        # atribui ao sound_timer o valor guradado em vx
        self.sound_timer = self.v[self.x]

    def ADD_I_vx(self):
        # soma vx ao valor de I
        self.i += self.v[self.x]

    def LD_F_vx(self):
        # atribui I para o endereço do sprite guardado em vx
        self.i = self.v[self.x] * 5

    def LD_B_vx(self):
        # pega o valor decimal de vx;
        # armazena as centenas no endereço I
        # armazena as dezenas no endereço I+1
        # armazena as unidades no endereço I+2

        # centenas
        self.memory[self.i] = self.v[self.x] // 100

        # dezenas
        self.memory[self.i + 1] = (self.v[self.x] // 10) % 10

        # unidades
        self.memory[self.i + 2] = self.v[self.x] % 10

    def LD_I_vx(self):
        # copia e guarda os valores dos registradores v0 até vx em memória,
        # começando do endereço I
        for i in range(0, self.x + 1):
            self.memory[self.i + i] = self.v[i]

    def LD_vx_I(self):
        # lê os valores da memória começando em I e guarda nos registradores v0 até vx
        for i in range(0, self.x + 1):
            self.v[i] = self.memory[self.i + i]

    def x0_last_bits(self, dirty_opcode):
        opcode = dirty_opcode & 0x000F
        derived_opcodes = {
            0x0000: opcode,
            0x000E: opcode
        }

        return derived_opcodes.get(opcode)

    def xF00F_bitmask(self, dirty_opcode):
        opcode = dirty_opcode & 0xF00F
        derived_opcodes = {
            0x8000: opcode,
            0x8001: opcode,
            0x8002: opcode,
            0x8003: opcode,
            0x8004: opcode,
            0x8005: opcode,
            0x8006: opcode,
            0x8007: opcode,
            0x800e: opcode,
        }

        return derived_opcodes.get(opcode)

    def xF0FF_bitmask(self, dirty_opcode):
        opcode = dirty_opcode & 0xF0FF
        derived_opcodes = {
            0xE09E: opcode,
            0xE0A1: opcode,
            0xF007: opcode,
            0xF00A: opcode,
            0xF015: opcode,
            0xF018: opcode,
            0xF01E: opcode,
            0xF029: opcode,
            0xF033: opcode,
            0xF055: opcode,
            0xF065: opcode,
        }

        return derived_opcodes.get(opcode)

    def decode(self, opcode):
        first_nibble = opcode & 0xF000
        derived_opcodes = {
            0x0000: self.x0_last_bits(opcode),
            0x8000: self.xF00F_bitmask(opcode),
            0xE000: self.xF0FF_bitmask(opcode),
            0xF000: self.xF0FF_bitmask(opcode),
        }

        return derived_opcodes.get(first_nibble, first_nibble)

    def execute(self, opcode):
        self.pc += 2

        self.x = (opcode & 0x0F00) >> 8

        self.y = (opcode & 0x00F0) >> 4

        self.opcode = opcode
        decoded_opcode = self.decode(opcode)

        instruction = self.instructions.get(decoded_opcode)
        instruction()

    def cycle(self):
        for i in range(self.speed):
            if not self.paused:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.execute(opcode)

        if not self.paused:
            self.update_timers()

        self.play_sound()
        self.renderer.render()
