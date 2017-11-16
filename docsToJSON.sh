#!/bin/bash
#download timeline
wget -qO timeline.csv https://docs.google.com/spreadsheets/d/e/2PACX-1vRPn8FauZPaqlxWSbtd5HlgjkQ4losr7mouZvUJklSUIMGQ1T-A7fcAEe9eqUP938ig2ST2XfOIU2rv/pub?output=csv
#convert csv timeline to JSON
python timeline.py
