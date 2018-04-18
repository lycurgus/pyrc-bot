# pyrc-bot
An irc bot in Python, built around asyncio

## modules
Any modules in the `modules` directory will be loaded on startup. The file `template` in the `modules` directory provides a hello-world example; further insight can be gained by examining `module.py`.

## todo
* condition matching for module functions needs to be simplified
* module loading can likely be simplified too as a result of the above
* colours for terminal output (https://gist.github.com/martin-ueding/4007035)
* support deactivating modules from automatic loading
* when channel join is denied due to nickserv registration, add the channel to a list to then join when registration comes in
* report module load failure to owner
