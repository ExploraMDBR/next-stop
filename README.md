# Next stop explora
<img width="200" alt="project logo" src="images/logo.png">

[![ExploraBadge](https://img.shields.io/badge/-Explora-eb5c2f)](https://mdbr.it/en/) [![Interactive](https://img.shields.io/badge/-Interactive_installation-55ca7c)](https://en.wikipedia.org/wiki/Interactive_art)
[![ExploraHat](https://img.shields.io/badge/-Explora_hat-d80000)](https://github.com/ExploraMDBR/explora-hat)

*Next stop explora* is a an application that emulates some of the functioning of a train cockpit throug a simplified console and simplified outputs.

- [Introduction](#introduction)
- [Development](#development)
- [Project additional infos](#infos)


## <a name="introduction"></a>Introduction
*Next stop explora* features a physical console that relies on **buttons** and **magnetic sensors** for users inputs and **displays and led strips as output**. The buttons and the sensors on the console are associated to typical actions to be performed as a train driver and influences what happens in the display and the leds behaviour.
The displays feature both video (pre-rendered or a camera output) and images.


## <a name="development"></a>Development

### Dependencies:
- [explora.display](https://github.com/ExploraMDBR/explora-display)
- [jQuery](https://github.com/jquery/jquery) 
  
jQuery dependency already comes with the repository (in `./public` folder). Just clone it and run `main.py` :

```bash
# Clone repo
git clone https://github.com/ExploraMDBR/next-stop.git

# Install explora.display
pip install -i https://test.pypi.org/simple/ explora-display --extra-index-url https://pypi.org/simple

# Start local server
python3 treno_controller.py # prints localhost:8080 to console (port number is randomly generated each launch)

# The application is now running and can be accessed at localhost:8080
```


## <a name="infos"></a>Project additional infos

### Project purpose
*Next stop explora* is designed to be an installation. A full size train cockpit features a display and a basic console.
 
**Two versions** of the installation have been presented: 
- The first one was displaying a video recorded in real time by a camera placed on topo of small toy train controlled through a reley and activated during “Running” state. The train rails were installed above the installation
area, being visible from all the visitors.
- The second relied on a pre rendered video paused and played accordingly with application states.

![Project image](images/example.png)

### Related Explora's project

- [Il buono prima di tutto]()




