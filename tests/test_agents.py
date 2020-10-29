from memsim.environment import build_environment
from memsim.agents import StackProgram, MonitorProgram, LinkedListProgram


def test_stack_program():
    env = build_environment(2**10)

    sp1  = StackProgram     (env, action_chance=0.5                , suicide_chance=0.0001 )
    sp2  = StackProgram     (env, action_chance=0.1                , suicide_chance=0.0001 )
    sp3  = StackProgram     (env, action_chance=0.9                , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    llp1 = LinkedListProgram(env, action_chance=0.1, block_size=1  , suicide_chance=0.0001 )
    # llp1 = LinkedListProgram(env, action_chance=0.05, block_size=2 , suicide_chance=0.0001 )
    # llp2 = LinkedListProgram(env, action_chance=0.03, block_size=4 , suicide_chance=0.0001 )
    # llp4 = LinkedListProgram(env, action_chance=0.01, block_size=2 , suicide_chance=0.0001 )
    # llp2 = LinkedListProgram(env, action_chance=0.005, block_size=8, suicide_chance=0.0001 )
    mp = MonitorProgram(env, record_every=100)

    env.run(until=300000)
    mp.visualize_memory()


