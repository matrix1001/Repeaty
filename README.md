# Repeaty

`Repeaty` is a python module designed for speeding up the re-execute of functions, with the backend of `pickle`, aiming at saving time.

The technique is quite easy to understand: Save the result of each function call, and reuse them in the same function call.

## feature

- speed up
- persistence support
  - store the data into a file and restore it in new process of python.

## limitation

- no support for those functions which use __global__ variables.
  - for example: time, random number, variables outside the funciton.
- does not care about the real meaning of the arguments.
  - for example: file name, object which may has changed.
- even slow it down when handling very simple functions.


# Dev log

## 2019/1/9 version 0.0.0

- very simple prototype