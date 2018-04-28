#!/bin/bash 

a=Hello
b="Good Morning"
c="16"

echo $a
echo $b
echo $c

# Double quotations can take variables & special characters
echo "$b! I have $c (apples)."
# Single quotations can take special characters but not variables
echo '$b! I have $c (apples).'
# regular echo takes variables but not special characters, i can remedy that with backslashes
echo $b! I have $c \(apples\).


# Adding speical attributes to variable
#declare -i d =123 # cast integer
#declare -r e =456 # cast read-only
#declare -l # lowercase
#declare -u # uppercase


# Command Sustitution
d=$(pwd)
echo $d

e=$(ping -c 1 google.com | grep 'bytes from' | cut -d = -f 4)
echo "the ping was $e"

# Arithmatic Operations
f=2
g=$((f+2))
echo $g

# Concatenate Strings
h=$b$c
echo $h

# Length of String
echo ${#a}

# Extract substring 
i=${b:3} # starting at the 3 character
j=${b:3:5} # from 3rd to 5th character
k=${b: -4} # last 4 characters (space needed)
l=${b: -4:3} # last 3 characters starting from the last 4th character
echo $i
echo $j
echo $k
echo $l

# replace strings
echo ${b/Good/love} #replace first instance of "GOOD" in string "b" with "love"
echo ${b//Good/love} #replace all instances of "GOOD"
# Couple other modifiers "#" and "%"
echo ${b/#Good/love} #replace first instance of "GOOD" only if it's the first thing
echo ${b/%Good/love} #replace first instance of "GOOD" only if it's the last thing




# array
a=()
b=("apple" "kiwi" "cherry")
echo ${b[1]}

# put value in specific location of array
b[5]="kiwi"
echo ${b[@]}

# put value at the end of an array
b+=("mango") #need double quotations to put it at the end, otherwise end up after 0 index
echo ${b[@]}

# Associative Arrays, Key:Value (bash 4.0 or above)
#declare -A myarray
#myarray[color]=blue
#myarray["office building"]="HQ West"
#echo ${myarray["office building"]} is ${myarray[color]}



# files
# add text in a file
echo "some text" > file.txt
cat file.txt

# deltet things in a file
> file.txt
cat file.txt

# add (append) thing at the end of a file
echo "some more text" >> file.txt
cat file.txt

# writing multiple lines using while loop
# read command
# reads the file.txt into variable "f" line by line
i=1
while read f; do
	echo "Line $i: $f"
	((i++))
done < file.txt


# comparisons
#[[ expression ]] returns 0 (success) or 1 (success)
[[ "cat" == "cat" ]]
echo $?

[[ 20 -gt 100 ]]
echo $?
# -z null
# -n not null

# Conditoinals
#if [ expression ]
#if [[ expresion ]]
#if expression

"""
if expression; then
	echo "True"

if expression
then
	echo "True"
elif expresion2; then
	echo "False"
fi
"""

a=2
if [ $a -gt 5 ]; then
	echo $a is greater than 4!
else
	echo $a is not greater than 4!
fi

# Using regular expression (=~: regular expression match
b="this is my string!"
if [[ $b =~ [0-9]+ ]]; then # extended test notation
	echo "tehre are numbers in the string: $b"
else 
	echo "there are no noumbers in the string!"
fi


# while and until loops
# while
i=0
while [ $i -le 10 ]; do # integer comparison less than equal to
	echo i:$i
	((i+=1))
done

j=0
until [ $j -ge 10 ]; do
	echo j:$j
	((j+=1))
done

# for loops
for i in 1 2 3; do
	echo $i
done

for i in {1..100}; do
	echo $i
done

# increments
for (( i=1; i<=10; i++ )); do # bash 4 or above
	echo $i
done

# looping through array
arr=("apple" "kiwi" "orange")
for i in ${arr[@]}; do
	echo $i
done

#Asscoiative Arrays(Key:Value Dictionary)
declare -A arr
arr["name"]="Scott"
arr["id"]="123"
for i in "${!arr[@]}"; do
	echo "$i: ${arr[$i]}"
done

#Command Substitution
for i in $(ls); do
	echo "$i"
done

### Case: to test values against series of values
a="cat"
case $a in
	cat) echo "Feline";; #testing the word cat against dog, semicolons to terminate this test
	dog|puppy) echo "Canine";; #keep adding test conditions, pipe condition for list of things to match (dog or puppy)
	*) echo "No match!";; #to catch no match
esac
	


###Functions - not to repeat the same command (maintenable and orgnized)
function greet {
	echo "hi there!, $1! what a nice $2!" #represents a first argument passed into a function
}

greet david day
greet julie night


function numberthings {
	i=1
	for f in $@; do #@ is special array variable that represents all arguments passed into function
		echo $i: $f
		((i+=1))
	done
}

numberthings $(ls)
numberthings david julie mom dad


### Arguments
echo $1
echo $2

# More than 2 arguments
for i in $@; do
	echo $i
done

echo there are $# number of arguments

# Flags
# put ":" in the beggining, specfies unknown flags 
#	:u:p
# 	?) echo "unknown flag"
# put ab at the end w/o ":", specifies whether or not its being used
# 	u:p:ab
#	a) echo "using A flag"
while getopts u:p: option; do
	case $option in
		u) user=$OPTARG;; # looking for -u flag
		p) pass=$OPTARG;; # looking for -p flag
	esac
done

echo "User: $user / Pass: $pass"


# input during exeution of script
echo "what is your name?"
#read name # prompts input

echo "what is your password?"
#read -s pass # prompts silent input(won't show input)

#read -p "what's your favorite animal?" animal #prompts input in the same line
#echo name: $name, pass: $pass, animal: $animal

select anmial in "cat" "dog" "bird" # prompt list of selections to put in "animal" variable
do 
	echo "you selected $animal"
	break
done

select option in "cat" "dog" "tiger" "quit"
do
	case $option in 
		cat) echo "cats like to sleep";;
		dog) echo "dogs love people";;
		tiger) echo "tigers are strong";;
		quit) break;;
		*) echo "no match";;
	esac
done

# Building Error Tolerance
read -p "Favorite food? [fish tacos] " a #fish tacos is the assume answer when there is no user input
while [[ -z "$a" ]]; do # -z option checks if input is not empty
	a="fish tacos"
done
echo "$a was selected"

read -p "what year [nnnn] " a
while [[ ! $a =~ [0-9]{4} ]]; do # check if user input is 4 number digits
	read -p "Four digits please! [nnnn] " a
done
echo "Selected year: $a"