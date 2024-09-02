#!bin/bash
git branch | grep -v "main\|master" | xargs git branch -D
