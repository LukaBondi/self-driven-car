# World Robot Olympiad Thailand 2023
<div align="center">
    <img align="center" src="images/logo_EasyKids.png" alt="Image" width="65%" />
</div>

## Table of Contents
- [1. Team introduction](#1-team-introduction)
- [2. Robot Design](#2-robot-design)
- [3. Program structure and Techniques used](#3-program-structure-and-techniques-used)
- [4. Problem solving & Solutions](#4-problem-solving--solutions)
- [5. Discussion](#5-discussion)
- [6. Summary](#6-summary)
- [7. Special thanks](#7-special-thanks)

## 1. Team introduction

### About Us


We are from Team **EasyKids-Janjam**. Our members are **Petch**, **Luka**, and **Tonkla**. We met each other at our robotics institution, **EasyKidsRobotics**. Despite each of us coming from different schools, we still came to meet each other through our love and passion for robotics at this very institute. We've been given the opportunity to develop programming and robotics skills together, enabling us to understand the strengths of each team member. This has allowed us to efficiently allocate tasks based on individual aptitudes
like the saying "Put the right man on the right job." As a result, we've achieved successful outcomes in our projects and integrated our efforts for this competition.

### Our roles

**1. The Mechanic (Petch):**
He is the one who conceives the robot's design, then troubleshoots, and assembles the robot. He tackles issues that arise during the assembly of the robot. He conceptualizes the assembly process from the very beginning, including the initial design, all the way to the latest iteration.

**2. The Programmer (Luka):** 
He will be responsible for designing the robotics program, testing the written code, and rectifying any errors in the program. Moreover, he will work on refining the program to achieve the best possible outcomen.

**3. The Documentarian (Tonkla):** 
He will be responsible for documenting various tasks undertaken, including assembly processes, errors encountered, lessons learned, and information about equipment usage.
____

## 2. Robot Design
### Initial Design

<div align="center">
    <img align="center" src="initial_all.png" alt="Image" width="65%" />
</div>

- **The chassis:** The chassis is derived from a 1/28 scale RC car, which has been modified to incorporate a customised steering kit. Instead of using a linking mechanism, we connect the servo directly to the steering axle. This way we can gain more range of motion, faster steering response for stability and it forces both wheels to turn at the same angle. 

	As for our drivetrain, we chose to use the rear wheel drivetrain to achieve the maximum steering angle possibl, allowing for tighturns
	in confined spaces. The propulsion system is placed at the front to prevent interference between the steering and propulsion components during operation.

- **The Base:** Our initial plan was to pursue a minimalist-style robot and utilize 3D-printed parts as sparingly as possible. Therefore, we decided to use the lidar sensor as our front base, while the electronics at the back are supported by a pillar part.

- **Main Board/Processor:** The brains of the robot is the Raspberry Pi which is coupled with the Derivmotor Shield tp ensure safe power distribution to components, safeguarding the Raspberry Pi from potential wiring errors. In layman's terms, the Derivmotor Shield manages the electronic components, while the Raspberry Pi issue commands to the robot

- **Sensors:** 
	
	- **The Lidar** module is integrated as a control component, collaborating with a camera system. The camera system is designed to rotate, allowing for a comprehensive view in all directions. All these subsystems are coordinated and controlled by a Raspberry Pi, which also manages the motor control.

		The reason for using the Lidar sensor is because it can detect objects, walls, and elements in a 360-degree field of view with high accuracy. However, there are a few limitations to using the lidar. Firstly it cannot be used at very high speeds. This may hinder us in the qualifiers when the goal is to go as fast as possible. Secondly the layout has black edges which does not reflect light well and goes against the mechanics of the lidar.

	- **The camera** is connected to a servo motor, so that we can extend of camera's field of view. The reason for using a rotating camera is that it can capture images and objects from all directions, allowing you to select the desired orientation for object detection.

	- **Gyroscope** is helps improve the stability of object and line detection in OpenCV.But the Gyroscope is that we couldn't find the required library.

- **The power supply:** The power supply system employs a 3-cell battery connected to a step-down converter to lower the voltage to 11.2 Volts. This adjustment ensures a consistent power supply, safeguarding the electronics
against potential power shortages. Subsequently, this voltage is directed to the Deriv Motor Shield, which regulates the voltage to prevent any damage to the Raspberry Pi. The 5V power output from the Deriv Motor Shield serves to power both the motor and ultrasonic components.


### Final design
<div align="center">
    <img align="center" src="images/cool_view.png" alt="Image" width="65%"/>
</div>

In this version, we removed the lidar and gyroscope. The lidar was replaced by the ultrasonics at the front. After some testing with the lidar it occured to us that the lidar didn't perform very well because of the dark edges on the field. We also wanted our robot to be fast so we opted to change the lidar to ultrasonics instead.

Ultrasonics use sound waves for distance detection   


The reason for choosing Ultrasonic over Lidar is that while Lidar can detect objects, walls, and elements in a 360-degree field of view with high accuracy, it may struggle to detect dark-colored surfaces effectively. This limitation led to the decision to switch to Ultrasonic technology. Ultrasonic sensors utilize sound waves for detection, which doesn't significantly affect their ability to detect objects, walls, and elements. This makes Ultrasonic sensors more suitable for accurate object detection and obstacle avoidance, regardless of the color of the surfaces.

The reason we removed the Gyroscope is that we couldn't find the required library, which caused us to waste time. We decided to address the issue by removing it.

## 3. Program structure and Techniques used

### Program structure
We have gained inspiration for coding from the 'Doggy Car' project, such as the practice of code modularization.
### Color Detection

Match that color to the orange and blue lines and the red and green objects.By grasping which color that represents, we will be able to measureThe HSV values ​​of orange-blue-yellow with this red begin to decompose into the following colors. Then write the program if you know what color.is any color all the time the motor.To turn and go forward starting from the line we hold the orange and blue to count the lines.how many rounds It will allow us to complete three laps.and the part of capturing red and green objects in order to know what color Red should turn right and green should turn left.

- H(Hue): This determines the type of color, such as red, green, blue, and so on. Adjusting the Hue value changes the color in a circular manner (color wheel), starting from red and looping back to red again.

- S(Saturation): This represents the intensity or vividness of a color. Higher Saturation values result in more vibrant colors, while lower values make colors appear more muted.

- V(Value): This defines the brightness of a color. Adjusting the Value value changes the brightness without altering the base color.

### The PID Controller 

The PID controller is a tool for monitoring and adjusting values ​​based on system feedback. so that the lessons match the target results by calculating the difference between
the target value and the current state of the process. Then use this difference to make adjustments using three main parts: 

- P adjusts the value up and down according to the closeness of the error value.
- I accumulates past error values. and eliminate consecutive outliers due to external disturbances. 
- D Predict future errors by considering the rate of change.

of error prevents the target from being exceeded. By tuning these components, the PID controller can be adjusted to be more stable and reasonable in the situation.
various

### Threading

Threading refers to the simultaneous execution of multiple tasks in a program, where each task is divided into thread that works for each part
But all threads share resources, for example, by dividing complex computational tasks into threads so that they can run simultaneously. or using separate threads to work
Frequency I/O (Input/Output) with the same anti-wait in a single thread.

## 4. Problem solving & Solutions
### Qualifiers

Ultrasonic sensors on the left and right sides are used to detect objects and walls. Then, the left and right ultrasonic sensors are input into a PID control loop. This is done to make the robot walk straight, stay centered, and maintain the most stable posture possible.

### Finals
For the final round, we used the principles of OpenCV to detect objects and lines for the purpose of implementing a PID equation to perform color detection on the object.


## 5. Discussion
To enhance the technique, various strategies can be employed, such as fine-tuning the ultrasonic sensors for improved accuracy and stability, implementing OpenCV for optimized performance, and incorporating other techniques to further refine and enhance its capabilities.

## 6. Summary

The modification of a 1/28 scale RC car into a robotic system with a custom 
steering kit, propulsion system, and integrated ultrasonic sensor. 
The Raspberry Pi, step-down converter, and camera system are key components 
of the system's control and functionality. OpenCV enhances the camera's object 
detection capabilities

### What  have learned
learned the importance of mutual assistance and knowledge exchange in 
collaborative projects. You've gained experience in problem-solving and 
design thinking. You've also realized the significance of selecting 
appropriate sensors, managing energy efficiently, integrating components 
effectively, and dealing with the complexities of programming behaviors 
as needed. This experience will serve as a foundation for further exploration 
and development in the fields of robotics and automation.

## 7. Special thanks 🙇‍♂️
We would like to express our gratitude to our parents, teachers, and all the supporters who have been with us throughout this journey. Thank you for your continuous support on this journey.
