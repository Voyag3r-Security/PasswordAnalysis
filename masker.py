#!/usr/bin/python3
# Author: Voyag3r
# Date: 11/27/2023
# Purpose: Analyze a list of passwords, one per line, and provide an analysis of the the passwords into a hashcat-like mask

import itertools, argparse

def main():
    # Take user input for the file location and how many of the top masks you'd like to see
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest = "file", default = "/usr/share/wordlists/rockyou.txt", help = "File to analyze; Default is Kali location of rockyou.txt")
    parser.add_argument("-n", "--number", dest = "number", default = "3", help = "How many top most common masks you'd like to output; If you'd like to output all of them, enter 0")
    parser.add_argument("-e", "--encoding", dest = "encoding", default = "utf-8", help = "Encoding to use for the file, default is utf-8; If you get a UnicodeDecode error try using 'latin-1'")
    parser.add_argument("-l", "--length", dest = "length", default = "0", help = "Only analyze passwords of the specified length or greater; Defaults to analyzing all passwords")
    args = parser.parse_args()

    maskArray = [] # Array to hold all the masks
    occurrences = { } # Dictionary to hold the masks and the corresponding number of occurrences

    # Open the password file and use latin-1 enoding (rockyou.txt doesn't like utf-8 encoding for some reason)
    with open(args.file, encoding = args.encoding) as wordlist:
        for line in wordlist:
            stripline = line[:-1] # Remove trailing newline
            # If args.length does not equal zero, analyze passwords of the specified length or greater
            if int(args.length) != 0:
                if len(stripline) >= int(args.length):
                    password = list(stripline) # Convert password to list to iterate through each character
                    mask = "" # Empty to string to fill in with the mask
                    # Determine which category each character belongs to
                    # Should cover more cases using non-American English characters than regexes
                    for i, char in enumerate(password):
                        if char.isdigit():
                            password[i] = "?d"
                        elif char.islower():
                            password[i] = "?l"
                        elif char.isupper():
                            password[i] = "?u"
                        else:
                            password[i] = "?s"

                    mask = mask.join(password) # Convert the character list to a string and store it in a mask
                    maskArray.append(mask) # Append the mask into the maskArray

            # If args.length is 0 (default), analyze all passwords
            else:
                password = list(stripline) # Convert password to list to iterate through each character
                mask = "" # Empty to string to fill in with the mask
                # Determine which category each character belongs to
                # Should cover more cases using non-American English characters than regexes
                for i, char in enumerate(password):
                    if char.isdigit():
                        password[i] = "?d"
                    elif char.islower():
                        password[i] = "?l"
                    elif char.isupper():
                        password[i] = "?u"
                    else:
                        password[i] = "?s"

                mask = mask.join(password) # Convert the character list to a string and store it in a mask
                maskArray.append(mask) # Append the mask into the maskArray
    # Determine and store the number of occurrences of each mask 
    for value in maskArray:
        if value in occurrences:
            occurrences[value] = occurrences[value] + 1
        else:
            occurrences[value] = 1

    # Sort the masks and print the three most used (default)
    print("Top " + args.number+ " Password Masks")
    print("---------------------")
    if int(args.number) == 0:
        for entry in list(sorted(occurrences, key=occurrences.get, reverse=True)):
            print(occurrences[entry],"\t:\t", entry)
    else:
        for entry in list(sorted(occurrences, key=occurrences.get, reverse=True)[0:int(args.number)]):
            print(occurrences[entry],"\t:\t",entry)

main()
