# SDK-Python
Python version of a microservice Software Development Kit (SDK) for the Foundation System

## Overview

The goal of this project is to speed the development of an intelligent, automomous environment that looks after the well being of the severly disabled. The environment should constantly monitor, anticipate and adapt itself to the person's changing needs.

The intended technical environment is a network of smart things integrated using a central message queue. Every smart thing participating in the network must be capable of publishing and subscribing to a central message queue. Smart things must use messages to and from the queue to coordinate their actions. Each smart thing must be capable of making itself known to other participants in the network. They must also be capable of reading and contributing to the collective state of the network-- a shared world view. Every smart thing must be capable of taking action, communicating the success or failure of the action, and updating the shared world view based on the outcome of that acton.

The SDK provides (and hides from smart-thing developers) the infrastructure integration required of all smart things. The SDK takes care of publishing and subscribing to a central message queue. The SDK (specifically, the AI known as Highcliff) determines when to call an action. The SDK handles registering smart things and making them known in the network. It handles reading and updating the shared world view. With the SDK, the smart thing developer need only include the appropriate SDK classes and implement the appropriate custom behavior.

## Quick Start
1. Clone the repository
2. Run `\examples\quick_start_LOCAL.py`
3. You should see the following output:
```
Ask Peter if he's okay with raising the temperature in the room
Peter gave the okay to raise the room's temperature

[{'action_status': <ActionStatus.SUCCESS: 'success'>,
  'my_goal': {'is_room_temperature_change_authorized': True},
  'my_plan': [PlanStep(action=<__main__.SimulatedUserInterface object at 0x000001FA0D9578B0>, services={})],
  'the_world_state_after': {'is_room_temperature_change_authorized': True,
                            'is_room_temperature_comfortable': False},
  'the_world_state_before': {'is_room_temperature_change_authorized': False,
                             'is_room_temperature_comfortable': False}}]
```

### The Complete Quick Start Code

```
# needed to run a local version Highcliff
from highcliff.ai import AI

# the Highcliff action you wish to implement
from highcliff.exampleactions import AuthorizeRoomTemperatureChange

# needed to pretty-print the AI's execution logs
from pprint import pprint

# define the state of the world and the ai capabilities.
# when running a local version of Highcliff, use global variables to simulate underlying infrastructure
# these global variables will be replaced with urls in the production version
the_world_GLOBAL_VARIABLE = {"is_room_temperature_change_authorized": False, "is_room_temperature_comfortable": False}
capabilities_GLOBAL_VARIABLE = []


# build functionality by writing custom behavior for your selected actions
class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects


# launch functionality by instantiating the action
SimulatedUserInterface(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)


# run a local version of Highcliff
ai_life_span_in_iterations = 1
goals = {"is_room_temperature_change_authorized": True}
highcliff = AI(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE, goals, ai_life_span_in_iterations)

# check the execution logs
print()
pprint(highcliff.diary())
```

### Explaining the Quick Start

To use this SDK and run your solution on your local machine, start by importing the Highcliff AI and the specific Highcliff actions you intend to implement.

```
# needed to run a local version Highcliff
from highcliff.ai import AI

# the Highcliff action you wish to implement
from highcliff.exampleactions import AuthorizeRoomTemperatureChange

# needed to pretty-print the AI's execution logs
from pprint import pprint
```

Create global variables that represent the state of the world and the actions that the AI is capable of executing. These variables are used by the SDK to simulate a connection to a central infrastructure responsible for providing the same information.

```
the_world_GLOBAL_VARIABLE = {"is_room_temperature_change_authorized": False, "is_room_temperature_comfortable": False}
capabilities_GLOBAL_VARIABLE = []
```

Write the custom behavior for any action that you imported.

```
class SimulatedUserInterface(AuthorizeRoomTemperatureChange):
    def behavior(self):
        print("Ask Peter if he's okay with raising the temperature in the room")
        print("Peter gave the okay to raise the room's temperature")
        return self.effects
```

Instantiate your new action. When running locally, the action should be instantiated using the global variables that simulate central infrastructure.

```
SimulatedUserInterface(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE)
```

Instantiate and run the Highcliff AI. When running locally, the AI should be instantiated uising the global variables that simulate central infrastructure.

```
ai_life_span_in_iterations = 1
goals = {"is_room_temperature_change_authorized": True}
highcliff = AI(the_world_GLOBAL_VARIABLE, capabilities_GLOBAL_VARIABLE, goals, ai_life_span_in_iterations)
```

The AI will select a goal, create a plan, and (if properly configured) select and run your action. You should see the custom behavior you specified running locally.

```
Ask Peter if he's okay with raising the temperature in the room
Peter gave the okay to raise the room's temperature
```
