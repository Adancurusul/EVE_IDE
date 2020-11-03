import re
import array

class change_into_bin(str):
    def __init__(self,str0):
        super().__init__(str0)
        self.prelist = [00,20,00,10,13]
        self.s = 0
        self.m = 0
        self.f = 0

    def change_and_return(self):
        head = {
            'fadd16':self.FADD16,
            'fsub16':self.FSUB16,
            'fmul16':self.FMUL16,
            'add16':self.ADD16,
            'sub16':self.SUB16,
            'and16':self.AND16,
            'or16':self.OR16,
            'xor16':self.XOR16,
            'lsh16':self.LSH16,

                }


    def FADD16(self):
        return '00000'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def FSUB16(self):
        return '00001'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def FMUL16(self):
        return '00010'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def ADD16(self):
        return '10000'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def SUB16(self):
        return '10001'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def AND16(self):
        return '10010'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def OR16(self):
        return '10011'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def XOR16(self):
        return '10100'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def LSH16(self):
        return '10101'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def RSA16(self):
        return '10110'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def RSL16(self):
        return '10111'+self.changeMASK(self.prelist[4])[0:2]+self.changeSS2(self.prelist[3])+self.changeSSD(self.prelist[2])+self.changeMASK(self.prelist[4])[2]+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])+self.changeMASK(self.prelist[4])[3:]+'11111'
    def FTI(self):
        return '0001000'+'00000'+self.changSS1(self.prelist[2])+str(0)+str(self.m)+str(self.s)+self.changeSD(self.prelist[1])