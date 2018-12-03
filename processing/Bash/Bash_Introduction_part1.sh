#!/bin/bash 
# Hashbang or Shebang (Interpreter Directive) + path to the Bash Executable

### Intro to Bash Scripting 
### Bash (Born Again Shell)
### Unix Shell == OS X Terminal == mimics Linux enviornmnet

############################## Single Commands ##############################

man "command"  # shows manual pages for that command
# press "q" to exit

# Expansions
# Tilda expansion
cd ~
# Brace expansion - when repeating 
touch {banana, apple, kiwi}
touch file_{1..1000}

# Zero Padding
touch file_{01..10}

# Specifying Range and Interval (only bash 4.0 or higher)
echo {1..10..2}
echo {a..z..2}

# Pipes
ls | wc -l # count of files
ls | more # page by page 

# grep : serach files for certain patterns
grep "serachword" "filename"
grep -i "searchword" "filename" | awk {'print $12'} # - i means case insenstive, print count 12th thing space deliminated

# Ping
ping -c 1 google.com # -c lets you print 1
ping -c 1 google.com | grep 'bytes from' | cut -d = -f 4 # cut slices up by 4th thing delimited by "="

############################## Bash Scripting ##############################

bash "filename.sh"
./"filename.sh" # if interpreter directive has been specified

echo "statement" # prints



















