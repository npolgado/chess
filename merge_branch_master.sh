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
# sleep 5
# git merge master
# sleep 5
# git push origin $BRANCH
# sleep 5
# git checkout master
# sleep 5
# git merge $BRANCH
# sleep 5
# git push origin master
# sleep 5

echo "This does nothing at the moment"