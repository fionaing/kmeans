# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 22:27:21 2020

@author: fionaing
"""
#I cen't run the code wihtout getting some empty centroids but i tried
#Should take between 20-30 iterations

from random import uniform
from math import sqrt
import csv


def clean(file): #cleans + formats file
    y = 0 #counter
    data = [] #list to put certain things from the txt file into
    for i in file: #removes \n from the file and splits up the vectors
        data.append(file[y].replace("\n","").split(" ",))
        y += 1
    del data[0] #gets rid of index at the beginning
    
    emojis = {} #turns data into dictionary, keys as the emojis, values as vectors
    for point in data:
        emojis[point[0]] = point[1:-1]
    return emojis

def make_centroids(): #makes 15 centroids with random dimensions
    centroid_vectors = [] 
    for z in range(299):  
        centroid_vectors.append(uniform(-.2,.2))
    return centroid_vectors

def find_distance(centroid, emoji): #finds distance between points and centroids
    distance = float(0)
    difference = []
    for i in range(299):#loops centroids and emojis through the distance formula
        difference.append((float(centroids[centroid][i]) - float(emojis[emoji][i]))**2) 
    for number in difference: 
        distance += number
    return sqrt(distance)

def average(assigned_centroid, assigned_emoji): #finds the average of the emojis dimensions for each emoji assigned to a centroid
    #assigned emoji is a list of all the emoji ids assigned to a centroid
    new_dimensions = []
    if assigned_emoji != []: 
        for counter in range(299):
            emoji_dimension = []
            new_dimension = 0 
            for a_emoji in assigned_emoji: #a_emoji is a single emoji id
                emoji_dimension.append(emojis[a_emoji][counter])
            for dimension in emoji_dimension:
                new_dimension += float(dimension)
            new_dimensions.append(new_dimension/299)
    if assigned_emoji == []:
        new_dimensions = centroids[assigned_centroid]
    return new_dimensions




def main_code(): #had to put everything in a function or else it doesn't work
    
    #opening and formating file into dictionary, emojis as keys and values as dimensions ----------
    file = open("emoji_dataset.txt", "r").readlines() #opens and reads the text file
    global emojis
    emojis = clean(file) #uses clean function to clean and format file into a dictionary

    #makes 15 random centroids ----------
    global centroids
    centroids = {}
    for x in range(15): 
        centroids[x] = make_centroids()

    #reads in tsv file, helps print emoji ids as actual emojis ----------
    emoji_tsv = {}
    tsv_file = open("emoji_lookup.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for row in read_tsv: #puts emoji id and actual emoji in a dictionary
        emoji_tsv[row[0]] = row[1]

    #Loop that assigns and moves centroids ----------
    global assigned_emojis    
    global new_centroids
    global min_centroid_distance
    global distance_difference
    global centroid_distances
    global total_difference
    new_centroids = {}
    emoji_symbol = []
    counter = 0
    number = 1
    while counter < 1:
        print(f"Iteration: {number}")
        number += 1
        if number > 149: #failsafe
            break
        
    #for every data point, figure out centroid closest, that point is assigned a centroid ----------
        distance_difference = {}
        for emoji in emojis:
            failsafe = 0
            centroid_distances = {}
            min_centroid_distance = {}
            total_difference = {}
            for centroid in centroids: 
                centroid_distances[centroid] = find_distance(centroid, emoji)
            for each_distance in centroid_distances.keys():
                if failsafe > 0:
                    break
                if centroid_distances[each_distance] == min(centroid_distances.values()):
                    min_centroid_distance[each_distance] = min(centroid_distances.values())
                    failsafe += 1
            distance_difference[emoji] = min_centroid_distance #adds dictionary with emoji id as values and distances from centroids as keys
 
    #assigns the emoji to the closest centroid ----------
        emoji_id = 0 
        emoji_distance = {}
        assigned_emojis = {}
        for counter1 in range(15): 
            emoji_list = []
            for emoji_id, emoji_distance in distance_difference.items():
                for min_distance in emoji_distance.keys():
                    if min_distance == counter1:
                        emoji_list.append(emoji_id)
            assigned_emojis[counter1] = emoji_list #dictionary has centroid as key its closest emojis as values

    #finds the average of the emoji values for each centroid, creates new dimensions for each centroid ----------
        new_centroids = {}
        for assigned_centroid, assigned_emoji in assigned_emojis.items():
            new_centroids[assigned_centroid] = average(assigned_centroid, assigned_emoji)
        
    #if the centroids stop moving, print the centroids and the emojis is has been assigned ----------
        if centroids == new_centroids: 
            for centroid_number in assigned_emojis:
                emoji_symbol = []
                for emoji_ids in assigned_emojis[centroid_number]:
                    emoji_symbol.append(emoji_tsv[emoji_ids[4:9]])
                print(f"Cluster: {centroid_number}\n{emoji_symbol}\n")
        centroids = new_centroids 
    return 

main_code()
