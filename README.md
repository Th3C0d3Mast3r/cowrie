# Cowrie

The following is a custom version of Cowrie, that I am making- its docker image for direct pull and run will be available here

> [!IMPORTANT]
> Keep in mind, this cowrie image is not in track with the updates with respect to the actual cowrie. To see the real and updated cowrie repo, check out the real repo present here => [cowrie/cowrie](https://github.com/cowrie/cowrie) 

So yes, **real creds to the Maintainer of Cowrie and the collaborators of cowrie.** 

I cannot be called as a **CONTRIBUTOR** as am not contributing some new feature there, but am contributing my version of real interactive version of cowrie - *(well, if this was a feature of real cowrie- then am sorry, but the real cowrie maintainers wrote some sloppy documentation where I couldn't find such things!)*

Also, check this [README.rst](./README.rst) -  the actual README that was written by the makers of `cowrie` -  I had to change the readme, because, tbh, it seemed kinda too long. This is my version of cowrie  ;)

## CUSTOMIZING YOUR OWN VERSION
Well, I edited the actual repo of `cowrie` to get the current version. Finding what to do where took hell lot of time, but well, it won't now for you. This is what I found out, and well, if this is known, ig, you won't have to spend more time for the same again- so yes, read this carefully to understand **WHAT GOES WHERE, AND WHAT TO DO WHERE**:
- `docker/Dockerfile`:- [explanation goes here]
- `etc/cowrie.cfg`:- [explanation goes here]

(and more)


## BUIDLING CUSTOM IMAGE

## CHANGELOG
Checkout the changelog. Every version here, would also be there on DockerHub. So check that out- that is, to pull it, just go to your terminal and type:- `docker pull dcodemaster/cowrie:<version>`

- `v0.1` [1st May, 2026] => Proper working `top` with `lscpu`, and other commands showing realistic server format
- `v0.2` [TBA] => `nano`, and other interactive commands simulated.

## YOUR VERSION OF COWRIE
Well, if you make some similar version of cowrie, where you have added some more things and stuff, and wish to share, write it in `Issues` so other peeps can see it and use it - even ur docker image can be pulled if u wish to make it public! 