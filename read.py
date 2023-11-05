f = open("wordlist.10000.txt", "r")
words = f.read().split()
words+=','+'\''+'\"'+'.'+'+'+'1'+'2'+'3'+'4'+'5'+'6'+'7'+'8'+'9'+'0'+' '+'-'
print(words)