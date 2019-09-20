# PCP

Prototyping Connected Products

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
