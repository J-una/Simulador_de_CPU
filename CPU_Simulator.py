class CPU:
    def __init__(self):
        self.registradores = [0] * 8  # 8 registradores de uso geral
        self.memoria = [0] * 256      # 256 bytes de memória
        self.pc = 0                   # Contador de Programa
        self.executando = True        # Estado de execução da CPU

    def carregar_programa(self, programa):
        self.memoria[:len(programa)] = programa

    def buscar(self):
        instrucao = self.memoria[self.pc]
        self.pc += 1
        return instrucao

    def decodificar_executar(self, instrucao):
        opcode = instrucao >> 4        # 4 bits superiores
        operando = instrucao & 0x0F    # 4 bits inferiores

        if opcode == 0x0:  # HLT: Parar
            self.executando = False
        elif opcode == 0x1:  # LDA: Carregar Acumulador
            self.registradores[0] = self.memoria[operando]
        elif opcode == 0x2:  # ADD: Somar ao Acumulador
            self.registradores[0] += self.memoria[operando]
        elif opcode == 0x3:  # SUB: Subtrair do Acumulador
            self.registradores[0] -= self.memoria[operando]
        elif opcode == 0x4:  # STA: Armazenar Acumulador
            self.memoria[operando] = self.registradores[0]
        elif opcode == 0x5:  # LDI: Carregar Imediato
            self.registradores[0] = operando
        elif opcode == 0x6:  # JMP: Pular para Endereço
            self.pc = operando
        elif opcode == 0x7:  # JC: Pular se Houver Carry
            if self.registradores[1]:  # Supondo que o registrador 1 seja a flag de carry
                self.pc = operando
        elif opcode == 0x8:  # JZ: Pular se Zero
            if self.registradores[0] == 0:
                self.pc = operando
        else:
            print(f"Instrução desconhecida: {instrucao}")

    def executar(self): # Essa função executa o programa que foi alocado na classe
        while self.executando:
            instrucao = self.buscar()
            self.decodificar_executar(instrucao)
            self.imprimir_estado()

    def imprimir_estado(self):
        print(f"PC: {self.pc}")
        print(f"Registradores: {self.registradores}")
        print(f"Memoria: {self.memoria[:16]}")
        print("------")

# Programa de exemplo para carregar na memória
# Este é um programa simples que carrega 42 no acumulador,
# adiciona 10 a ele e depois armazena o resultado na memória na posição 10.
programa = [
    0x30 + 42,  # LDI 42
    0x20 + 10,  # ADD M[10]
    0x40 + 10,  # STA 10
    0x00        # HLT
]

cpu = CPU()
cpu.carregar_programa(programa)
cpu.executar()
