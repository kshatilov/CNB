# Deep Learning EMG Gesture Recognition for Intuitive Control of Robotic Prosthesis

## Overview
8 channel Electromyography (EMG, electrodiagnostic technique for evaluating and recording the electrical activity produced by skeletal muscles) signal was used for real time gesture recognition. Recording hardware – commercial MYO band – detects the electric potential generated by muscle cells with 200 Hz frequency (200 samples per second). Convolutional neural network (CNN, a class of deep, feed-forward artificial neural networks) was deployed for classification of signals. Developed classifier enabled us to capture certain patterns in fixed size windows of temporal EMG data with minimum amount of preprocessing and feature selection. Combination of deep neural network and signal processing techniques alongside with carefully tuned parameters and architecture allowed us to achieve (close to the state of the art) accuracy of 89% of 5 label gesture recognition. 
### Gestures being recognized: 
Palm (rested state),
 
Fist (grab),

Point (pressing buttons, social interaction),

Thumb Up (for social interaction),

Middle Finger (for social interaction)


## Online gesture recognition GUI overview
![Alt text](https://github.com/kshatilov/CNB/blob/master/ExpApp/datacore/EMG/doc/GUI_overview.JPG)

## Dataflow illustration
![Alt text](https://github.com/kshatilov/CNB/blob/master/ExpApp/datacore/EMG/doc/EMG_DF.png)