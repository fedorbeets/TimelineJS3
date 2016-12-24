#!/bin/bash
#download timeline
wget -qO timeline.csv https://docs.google.com/spreadsheets/d/1LGbyhHGEHSRtIkmPs8AaIOGBUnGLQTfsjrVKQpscm9k/pub?output=csv
#convert csv timeline to JSON
python timeline.py
