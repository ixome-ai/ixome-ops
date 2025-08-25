#!/bin/bash
# Sync local branch with Heroku and deploy

# Pull remote changes from Heroku and rebase
git pull heroku main --rebase

# Push to Heroku
git push heroku main

# Check Heroku logs
heroku logs --tail --app ixome-smart-home