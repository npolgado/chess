#!/bin/bash

# Merge dev branch into master

# get name of current branch
BRANCH=$(git symbolic-ref --short HEAD)

# git pull --rebase origin master
# git checkout master
# git pull --rebase origin master
# git merge $BRANCH
# git push origin master


# # alternatively

# git pull
# git merge master
# git push origin $BRANCH
# git checkout master
# git merge $BRANCH
# git push origin master

echo "This does nothing at the moment"