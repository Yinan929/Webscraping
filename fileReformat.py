#!/usr/bin/python

from sets import Set

src = open("missingData.txt", "r")
target = open("dataMissingAtc.txt", "a")

allWords = src.readlines()[0].split(" ")

s = Set([])
for word in allWords:
	if (len(word) > 8):
		atc = word[:-8]
		if (word[-8:] == "possible"):
			if (atc not in s):
				target.write(atc + "\n")
				s.add(atc)

