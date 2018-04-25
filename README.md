# pyrc-bot
An irc bot in Python, built around asyncio

## modules
Any modules in the `modules` directory will be loaded on startup. The file `template` in the `modules` directory provides a hello-world example; further insight can be gained by examining `module.py`.

## todo
* colours for terminal output (https://gist.github.com/martin-ueding/4007035)
* support deactivating modules from automatic loading
* report module load failure to owner
* Expectations (`util.py`) should be awaitable somehow
* `nowplaying` module's WHOIS check has been disabled temporarily
