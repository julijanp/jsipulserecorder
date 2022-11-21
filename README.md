# JSI pulse recorder
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
In most water-cooled nuclear reactors, except zero-power reactors, Cherenkov radiation is present. It is due to energetic charged particles traveling faster than the speed of light in a dielectric medium. In open pool reactors, Cherenkov radiation can be observed as a blue glow around the reactor core. Since the intensity of the Cherenkov light produced in the reactor cooling water is in principle proportional to the neutron flux during a reactor pulse, an alternative method to measure the time dependence of the reactor power based on Cherenkov light intensity measurements is implemented at the JSI TRIGA research reactor.

The Cherenkov Pulse Recorder is based on a closed tube in order to avoid interference from external light sources and radiation damage experienced by optical fibers. The system consists of an aluminium tube with an inner diameter of 36 mm positioned in the reactor core periphery, containing 0.65 l of water (filling the height of the reactor core in the tube). The water serves as the source of Cherenkov radiation in the measurement system. The Cherenkov light intensity in the channel is measured by silicon photo multiplier (SiPM) based detector linked with Redpitaya data acquisition system. With the use of neutral-density filters (ND filters), located in front of the SiPM dynamic range of the detector, is adjusted.

## Technologies
Project is created with:
* Python 3.8
	
## Setup
To run this project, copy repository to your computer and start it with:

$python3 app_test_mac.py
