# Open Anime Tracker

This is a project meant to solve 2 issues in the Anime Community.
1. Fix the issue of newly aired shows usurping the highest rated anime on the site and then subsequently dropping off after 2 episodes.
2. Give those anime a fighting chance at passing the highest rated anime by going against what most anime trackers do: Splitting series up into seasons and never congregating them together, having them stand on their own against complete 1 season shows and movies.

Python version: ```3.11```

Node version: ```20.11.1```

## For Linux Users:

You will have to install packages depending on your distro as this uses sqlalchemy with postgresql.
```psycopg2```

## For Ubuntu (and derivatives) 22.04 users:
You will have to install 3.11 via a ppa.

### How to set up the environment:

The easiest way is to use Pycharm to get it going.

Make sure the drop the PATH variable in your .zshrc/.bashrc file located in the ```home``` directeory.

https://www.jetbrains.com/help/pycharm/poetry.html

### Running the Environment:
```flask --app main run``` To run the backend, use ```--debug``` to have the server reload dynamically as you make changes.

```npm start``` Is to start the frontend in dev mode.

```npm build``` Is to build the frontend for the server to send upon request. (Currently not implemented serverside.)