from memsim.environment import build_environment
from memsim.agents import StackProgram, MonitorProgram


def test_stack_program():
    env = build_environment(128)

    StackProgram(env, action_chance=0.1)
    MonitorProgram(env)

    env.run(until=100)


