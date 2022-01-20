# SDK-Python
Python version of a microservice Software Development Kit (SDK) for the Foundation System

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
