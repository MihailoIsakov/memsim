from memsim.environment import build_environment
from memsim.agents import StackProgram, MonitorProgram


def test_stack_program():
    env = build_environment(2**10)

    sp1 = StackProgram(env, action_chance=0.1)
    sp2 = StackProgram(env, action_chance=0.1)
    sp3 = StackProgram(env, action_chance=0.1)
    mp = MonitorProgram(env, record_every=20)

    env.run(until=100000)
    mp.visualize_memory()


