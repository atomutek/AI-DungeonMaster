import json
import os
import numpy as np
from generator import StoryGenerator
from story_tracker import StoryTracker
import tensorflow as tf
from utils import *

"""
Story flow:
1. Initial prompt seeds first story block
2. With story block (plus past additions) generate action possibilities
3. Using selected action (plus past additions) generate new story block
4. Repeat from 2

AI DM file handles high level interface functionality.
StoryTracker keeps track of story and action blocks, it can return the action prompt and the story block prompt

Dev Notes:
- It seems anecdotally that a top_k of 40 actually is better. Would be good to experiment with it more though.


"""

with tf.Session(graph=tf.Graph()) as sess:

    generator = StoryGenerator(sess)
    story_tracker = StoryTracker()
    
    # Print intro
    print("\n"+"=" * 40 + "  "+ "=" * 40) 
    story_block = generator.generate_story_block(story_tracker.start_prompt)
    print(story_tracker.start_prompt + story_block)
    
    while(True):
        
        # Get action prompt and generate possible actions
        action_prompt = story_tracker.get_action_prompt(story_block)
        action_phrases = story_tracker.get_action_phrases()
        options = generator.generate_action_options(action_prompt, action_phrases)
        
        print("\nOptions:")
        for i, option in enumerate(options):

            print(str(i)+") ", option)
            
        choice = input("Which do you choose? (0/1/2/3) ")
        print(" ")
        
        
        # TODO handle invalid selections
        if "custom" in choice:
            choice = input("What custom action would you like to take? ")
            print("")
            chosen_action = choice
        else: 
            chosen_action = options[int(choice)]
            
        print(chosen_action)
        print(" ")
        
        
        # Get next story_block based on selected action
        story_prompt = story_tracker.get_story_prompt(chosen_action)
        story_block = generator.generate_story_block(story_prompt)
        print(story_block)
        
