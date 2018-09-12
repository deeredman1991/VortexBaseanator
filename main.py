import math
# base num = { 0, ..., num-1}

import pic_mker as pm

def bases(num):
    for i in range(1, num):
        if i > 9:
            yield chr(i+55)
        else:
            yield i
    
def doubler(dinpt):
    #1, 2, 4, 8, 16, 32, 64, 128, 512
    
    num = 1
    
    for i in bases(dinpt+1):
        yield num
        num *= 2
        
def doAdding(ninpt, iinput, base):
    i = ninpt
    num_list = [i]
    found_repeater = False
    while not found_repeater:
        i += iinput
        i = ((i-1) % (base-1))+1

        if i in num_list:
            found_repeater = True

        num_list.append(i)
    return num_list
        
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]
    
def main():
    while True:
        inpt = input('>')
        
        num, base, start_adder, adder = inpt.split(' ')
        num, base, start_adder, adder = int(num), int(base), int(start_adder), int(adder)
        sequence = []
        found_repeater = False
        if base > 1:
            print('Printing {0} doubles in Base {1}.'.format(num, base))
            print('M = value MOD base-1')
            print('{0} : {1} : {2} : {3}'.format('Iter'.rjust(5, ' '), 'Number in Base {0}'.format(base).rjust(30, ' '), 'M', 'Number in Decimal'))
            for index, i in enumerate( doubler(num) ):
                based_number = numberToBase(i, base)
                vortexed_based_number = based_number[:]
                
                for x in range(len(based_number)):
                    based_number[x] = str(based_number[x]) if based_number[x] <= 9 else chr(based_number[x]+55)
                print('{0} : {1} : '.format(str(index+1).rjust(5,' '), ''.join(based_number).rjust(30,' ')), end='')
                
                while len(vortexed_based_number) > 1:
                    vortexed_based_number = numberToBase(sum(vortexed_based_number), base)
                    
                vortexed_based_number = vortexed_based_number[0] if vortexed_based_number[0] <= 9 else chr(vortexed_based_number[0]+55)
                print('{0} : {1}'.format(vortexed_based_number, i))
                
                if found_repeater == False:
                    if vortexed_based_number in sequence:
                        found_repeater = True
                    sequence.append(vortexed_based_number)
                    
            
            non_repeat_sequence = []
            repeat_sequence = []
            
            found_repeater = False
            for i in range(len(sequence)):
                if sequence[i] == sequence[-1]:
                    found_repeater = True
                    non_repeat_sequence.append(sequence[i])
                if found_repeater:
                    repeat_sequence.append(sequence[i])
                else:
                    non_repeat_sequence.append(sequence[i])
                
            adder_sequence = doAdding(start_adder, adder, base)
                    
            pm.make_picture(base, [adder_sequence, non_repeat_sequence, repeat_sequence], ['blue', 'red', 'green'])
            #pm.make_picture(b, [sequence], ['green'])

if __name__ == '__main__':
    #double_base(16, 100)
    main()
    