#!bin/zsh
git branch | grep -v "main\|master" | xargs git branch -D
