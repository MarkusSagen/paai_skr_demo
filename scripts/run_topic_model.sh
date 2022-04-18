#!/bin/bash


# # kb - swedish
# python topicmodel.py --model_name kb --num_topics 10 --calculate_probabilities True
# python topicmodel.py --model_name kb --num_topics 30 --calculate_probabilities True
# python topicmodel.py --model_name kb --num_topics 50 --calculate_probabilities True

# mp
python topicmodel.py --model_name mp --num_topics 10 --calculate_probabilities True
python topicmodel.py --model_name mp --num_topics 30 --calculate_probabilities True
python topicmodel.py --model_name mp --num_topics 50 --calculate_probabilities True

# minilm
python topicmodel.py --model_name minilm --num_topics 10 --calculate_probabilities True
python topicmodel.py --model_name minilm --num_topics 30 --calculate_probabilities True
python topicmodel.py --model_name minilm --num_topics 50 --calculate_probabilities True
