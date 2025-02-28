#1
#abc exist, so we get abc
#2
#"a.c" in text(. is some symbol), so our program give result axc
#3
# ^ match the begining of the text, so we get abc
#4
#$ matches the end of the string, so we get abc and ['abc']
#5
#[] is the list of chars that may be in our text, so in first example we get e and in second example we get ['e','o','o']
#6
#0-9 contain all elements from 0 to 9 including so we get 1 (search finds first existing element) and ['1', '2', '3', '4', '5', '6', '7', '8', '9']
#7
# * shows corresponding begining 
#8
#in first example our text starts with ac so it doesnot correspond, in second example our text starts with abc (it is right)
#9
#? compares each element individually
#10
#() matches exact elements in the parentheses
#11
#| is like OR operation
#12
#\ finds special symbol, so we get . and ['.','.']