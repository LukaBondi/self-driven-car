# Self-driven-car
This repo contains the source code for Thailand's WRO future engineers tournament.

# How it works

To go around the track, we need to first find noticeable features that would allow the car to turn, just like in real life situations where we need to recognise different parts of the road to realise that we need to turn. We used a camera to get images that can be used to detect different features just like how a human would percieve the road in front of him as he drives. 

We chose the blue and orange lines on the corners as features that would be signals for the car to turn. First the car would see either an orange or blue line, then we can steer accordingly to line we detected until the car sees the other line that it didn't detect or we could time our steer and stop when the car is heading straight. The first solution seems more promising than the second but both solutions have its own flaws. 


We also have 2 distance sensors on the front to help the car stay on track and not to crash into the edges.

## Line detection
To recognize the blue and orange lines, we have to filter out all the other colors that may cause confusion in an image. We can do this by using a threshold to limit our color boundaries to focus on only on the blue and orange colour, but before we apply the threshold to our image.



