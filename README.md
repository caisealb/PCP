# PCP
IP adress Raspberry Pi: 145.94.173.147

TESTING

Prototyping Connected Products

test test test 

By Cais, Kiki and Yu


“While the population of wheelchair users is growing worldwide, it becomes urgent to design supportive technologies that fit their needs. We aim to develop products for improvement of the wheelchair users’ wellbeing. This design is a connected product that collects data from sensors, processes it in order to actuate user interactions embedded in the wheelchair.”

Building upon this brief, we envision our target user group as (either full- or part-time) manual wheelchair users aiming to work towards or maintain a healthier, more active lifestyle. Features of our connected product will include distance and activity tracking (such as GPS and accelerometer), with sensory feedback and an app-based UX interface.

Sensors:
1) accelerometer
  An accelerometer can be used as a pedometer, and in the case of a wheelchair, a measure of movement or effort exerted via pushing the chair's wheels manually.
  Pros: Simple to use and program
  Cons: Data cannot be used directly as-is

2) GPS
  GPS can be used to track location and distance travelled, allowing a wheelchair user to plan routes and track their activity.
  Pros: Widely supported in UX/UI; data is understandable and meaningful for users
  Cons: Doesn't indicate speed or activity/effort

3) Rotation sensor
  Rotation sensors can be used to measure rotation of wheelchair wheels - i.e. the number of times the wheels spin. In a manual wheelchair, this could help to indicate effort exerted by the user.
  Pros: Simple calculation to convert to distance
  Cons: Reversing complicates data

4) Pressure sensor
  Can be used on a single point on the wheel to indicate that the wheel has made contact with the ground, i.e. completed a single rotation.
  Pros: Simple data and indication of movement
  Cons: Can be triggered by partial rotations

5) Vibration sensor
  Can be used to indicate when user is travelling on rough terrain, which might then result in a motor (actuator) helping to push a manual wheelchair forward.
  Pros: Simple data and easy to set threshold
  Cons: Susceptible to noise

6) Inclinometer
  Can be used to indicate when user is travelling uphill, again resulting in a motor aiding their movement.
  Pros: Many different potential applications
  Cons: External influences on data and unforeseen triggers


Actuators:
1) vibration motor
  Can be used to indicate progress, motivate and support user in activity
  Pros: direct haptic feedback and simple to program
  Cons: Could be irritating with repeated use

2) LEDs
  Can be used to indicate state change or progress towards daily activity goals.
  Pros: Visible for user and gives direct visual feedback
  Cons: Could be uncomfortably inconspicuous

3) Screen
  Can be used to visually represent relevant data and communicate progress towards goals.
  Pros & Cons: Very open format - lots of potential but requires extensive testing

4) Speaker
  Can be used to indicate state change or progress towards daily activity goals.
  Pros: Visible for user and gives direct visual feedback
  Cons: Could be uncomfortably inconspicuous or irritating

5) motor
  Can be used to support user movement, i.e. pushing wheels manually (in combination with tilt sensor and/or vibration sensor)


Things that need to be tested:
Accelerometer - how does it work? What kind of data can we get from it?
Motor - can we get a motor powerful enough to meaningfully help a user?
Inclinometer - how does it work and what does the data look like?
Screen - what does the app look like and how would it receive/communicate data?

THING_ID=my-wheelchair-960d
THING_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Njk1NjY2NjMsImV4cCI6MTg4NTE0NjI2MywiYXVkIjoiaHR0cHM6Ly9kd2QudHVkZWxmdC5ubDo0NDMvYXBpIn0.do5XB2iEkEfkqIt-3aUQpQPaudnsrE_AslXKkf6I_WzlP_n64YWJgjSWEYV5IRPmyDIl_cfUTTy4RgSH7YZUc6oFJl7_DSQhiKRxHRfWnc9ns-3AX9pVjVybjVWUO2uivvCRQzXP3gb9_V7Ip-3R75Owb2KTa2Ov1GcGM9Vmcz_d3WvqNvnqgAbLDbX3ZTvZX-Zl7dclqIPBWc0yT6eBAsadsKv0IwLEL9_a6WZJ4TfjpDk6aRoTrYA7w24ggmjtJURxjK4j7kercInPg1ArmpSTS_5lFrDq81KOaiO4w-FXSria9RiEk_AlIAl7VPqh_EJQfWpM99a3-SjGbDGHd8PVxiY8BWlOC6MLY19kEtMUyHSXvNRIn-leO3SRdPs-mf9zU80rWx_3PdS9g6Qb3_Ie3AV00jg5jqELmT-q2asg4jmzoPSrOdfj7eYuatGOpVlOQNOjXRM44WjURzoft3qfnEurFQ8JwLXAi-t_dUiG5r_h_oN_0fIaQDUE2qPPw3oji4y8XMtmmF6raMHT374YoccSN7dUHhNvoY0IuvhdVQY1tA8-_uu5WrgRB04UTIZnI5T13lJsQvQyWtO6kmMCckDsXRNwFuC5KstP8-Y887ZzQLddiO-lK22S5PaxLmUfpvapHZKqrZMTpKikE3uPR2IddTt3xTLTAttn7RI


color palette:
grey: #282e3a
yellow/orange: #eca72c
Green: #2dcb74
red: #ad343e
Lightgrey: #bcabae
