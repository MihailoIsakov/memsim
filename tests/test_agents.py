from memsim.environment import build_environment
from memsim.agents import StackProgram, MonitorProgram, LinkedListProgram, StableLinkedListProgram


def test_stack_program():
    env = build_environment(2**10)

    suicide_chance = 0

    sp1  = StackProgram     (env, action_chance=0.5                , suicide_chance=suicide_chance)
    sp2  = StackProgram     (env, action_chance=0.1                , suicide_chance=suicide_chance)
    sp3  = StackProgram     (env, action_chance=0.9                , suicide_chance=suicide_chance)
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=suicide_chance)
    llp1 = LinkedListProgram(env, action_chance=0.06, block_size=4  , suicide_chance=suicide_chance)
    llp1 = LinkedListProgram(env, action_chance=0.03, block_size=16  , suicide_chance=suicide_chance)
    # llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=suicide_chance)
    # llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=suicide_chance)
    # llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=suicide_chance)
    # llp1 = LinkedListProgram(env, action_chance=0.05, block_size=2 , suicide_chance=suicide_chance)
    # llp2 = LinkedListProgram(env, action_chance=0.03, block_size=4 , suicide_chance=suicide_chance)
    # llp4 = LinkedListProgram(env, action_chance=0.01, block_size=2 , suicide_chance=suicide_chance)
    # llp2 = LinkedListProgram(env, action_chance=0.005, block_size=8, suicide_chance=suicide_chance)

    # for i in range(20):
       # StableLinkedListProgram(env, action_chance=1, mean_blocks=100, var_blocks=100, block_size=1, suicide_chance=0.01)

    mp = MonitorProgram(env, record_every=100)

    env.run(until=200000)
    mp.visualize_memory()


