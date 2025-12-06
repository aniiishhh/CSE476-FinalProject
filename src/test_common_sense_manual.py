from src.planning import solve_planning_problem

def test_planning():
    print("=== Test 1: Feast/Succumb Domain ===")
    example_1 = """
    I am playing with a set of objects. Here are the actions I can do Attack object Feast object from another object Succumb object Overcome object from another object I have the following restrictions on my actions: To perform Attack action, the following facts need to be true: Province object, Planet object, Harmony. Once Attack action is performed the following facts will be true: Pain object. Once Attack action is performed the following facts will be false: Province object, Planet object, Harmony. To perform Succumb action, the following facts need to be true: Pain object. Once Succumb action is performed the following facts will be true: Province object, Planet object, Harmony. Once Succumb action is performed the following facts will be false: Pain object. To perform Overcome action, the following needs to be true: Province other object, Pain object. Once Overcome action is performed the following will be true: Harmony, Province object, Object Craves other object. Once Overcome action is performed the following will be false: Province other object, Pain object. To perform Feast action, the following needs to be true: Object Craves other object, Province object, Harmony. Once Feast action is performed the following will be true: Pain object, Province other object. Once Feast action is performed the following will be false:, Object Craves other object, Province object, Harmony. [STATEMENT] As initial conditions I have that, object b craves object d, object c craves object a, object d craves object c, harmony, planet object a and province object b. My goal is to have that object a craves object d and object d craves object c.
    """
    plan_1 = solve_planning_problem(example_1)
    print(f"Plan 1 Output:\n{plan_1}\n")

    print("=== Test 2: Logistics Domain ===")
    example_2 = """
    I have to plan the logistics of transporting crates between a number of depots and distributors via trucks that are loaded by hoists. Depots and distributors are directly connected by roads (trucks can drive between any two depots or distributors). A depot is a type of place. A distributor is a type of place. A pallet is a type of surface. A crate is a type of surface. Here are the actions that can be performed: Drive a truck from one place to another place. Use a hoist to lift a crate from a surface at a place. Use a hoist to drop a crate to a surface at a place. Use a hoist to load a crate into a truck at a place. Use a hoist to unload a crate from a truck at a place. The following are the restrictions on the actions: A truck can be driven from one place to another place only if the truck is at the origin place. Once a truck has been driven from one place to another, it is not at the origin place and is at the destination place. A crate can be lifted by a hoist only if the hoist is at the same place as the crate, the hoist is available, and the crate is clear. Once a crate has been lifted by a hoist from a surface at a place, the crate is not at the place, the hoist is lifting the crate, the hoist is not available, the surface is clear, and the crate is not on the surface. A crate can be dropped by a hoist to a surface only if the hoist and surface are both at the place, the surface is clear, and the hoist is lifting the crate. Once a crate has been dropped by a hoist to a surface at a place, the hoist is available, the hoist is not lifting the crate, the crate is at the place, the surface is not clear, the crate is clear, and the crate is on the surface. A crate can be loaded by a hoist onto a truck at a place only if the hoist is at the same place, the truck is at the same place, and the hoist is lifting the crate. Once a crate has been loaded by a hoist onto a truck at a place, A crate can be unloaded by a hoist from a truck at a place only if the hoist is at the same place as the truck, the hoist is available, and the crate is in the truck. Once a crate has been unloaded by a hoist from a truck at a place, the crate is not in the truck, the hoist is not available, and the hoist is lifting the crate. [STATEMENT] As initial conditions I have that, crate0 is at depot2, crate1 is at depot2, crate2 is at depot2, hoist0 is at depot0, hoist1 is at depot1, hoist2 is at depot2, hoist3 is at distributor0, pallet0 is at depot0, pallet1 is at depot1, pallet2 is at depot2, pallet3 is at distributor0, truck0 is at distributor0, truck1 is at depot1, truck2 is at depot2, hoist0 is available, hoist1 is available, hoist2 is available, hoist3 is available, crate2 is clear, pallet0 is clear, pallet1 is clear, pallet3 is clear, crate0 is on pallet2, crate1 is on crate0 and crate2 is on crate1. My goal is to have that crate0 is on pallet2, crate1 is on pallet1 and crate2 is on pallet0.
    """
    plan_2 = solve_planning_problem(example_2)
    print(f"Plan 2 Output:\n{plan_2}\n")

    print("=== Test 3: Feast/Succumb Domain (Variant) ===")
    example_3 = """
    I am playing with a set of objects. Here are the actions I can do
    Attack object
    Feast object from another object
    Succumb object
    Overcome object from another object
    I have the following restrictions on my actions:
    To perform Attack action, the following facts need to be true: Province object, Planet object, Harmony.
    Once Attack action is performed the following facts will be true: Pain object.
    Once Attack action is performed the following facts will be false: Province object, Planet object, Harmony.
    To perform Succumb action, the following facts need to be true: Pain object.
    Once Succumb action is performed the following facts will be true: Province object, Planet object, Harmony.
    Once Succumb action is performed the following facts will be false: Pain object.
    To perform Overcome action, the following needs to be true: Province other object, Pain object.
    Once Overcome action is performed the following will be true: Harmony, Province object, Object Craves other object.
    Once Overcome action is performed the following will be false: Province other object, Pain object.
    To perform Feast action, the following needs to be true: Object Craves other object, Province object, Harmony.
    Once Feast action is performed the following will be true: Pain object, Province other object.
    Once Feast action is performed the following will be false:, Object Craves other object, Province object, Harmony.
    [STATEMENT]
    As initial conditions I have that, object a craves object b, object c craves object a, harmony, planet object b and province object c.
    My goal is to have that object b craves object c and object c craves object a.
    """
    plan_3 = solve_planning_problem(example_3)
    print(f"Plan 3 Output:\n{plan_3}\n")

    print("=== Test 4: Paltry/Sip Domain ===")
    example_4 = """
    I am playing with a set of objects. Here are the actions I can do
    Paltry object_0 object_1 object_2.
    Sip object_0 object_1 object_2.
    Clip object_0 object_1 object_2.
    Wretched object_0 object_1 object_2 object_3.
    Memory object_0 object_1 object_2.
    Tightfisted object_0 object_1 object_2.
    I have the following restrictions on my actions:
    To perform paltry action, the following facts need to be true: hand object_0, cats object_1, texture object_2, vase object_0 object_1, and next object_1 object_2
    Once paltry is performed the following facts will be true: next object_0 object_2
    Once paltry is performed the following facts will be false: vase object_0 object_1
    To perform sip action, the following facts need to be true: hand object_0, cats object_1, texture object_2, next object_0 object_2, and next object_1 object_2
    Once sip is performed the following facts will be true: vase object_0 object_1
    Once sip is performed the following facts will be false: next object_0 object_2
    To perform clip action, the following facts need to be true: hand object_0, sneeze object_1, texture object_2, next object_1 object_2, and next object_0 object_2
    Once clip is performed the following facts will be true: vase object_0 object_1
    Once clip is performed the following facts will be false: next object_0 object_2
    To perform wretched action, the following facts need to be true: sneeze object_0, texture object_1, texture object_2, stupendous object_3, next object_0 object_1, collect object_1 object_3, and collect object_2 object_3
    Once wretched is performed the following facts will be true: next object_0 object_2
    Once wretched is performed the following facts will be false: next object_0 object_1
    To perform memory action, the following facts need to be true: cats object_0, spring object_1, spring object_2, and next object_0 object_1
    Once memory is performed the following facts will be true: next object_0 object_2
    Once memory is performed the following facts will be false: next object_0 object_1
    To perform tightfisted action, the following facts need to be true: hand object_0, sneeze object_1, texture object_2, next object_1 object_2, and vase object_0 object_1
    Once tightfisted is performed the following facts will be true: next object_0 object_2
    Once tightfisted is performed the following facts will be false: vase object_0 object_1
    [STATEMENT]
    As initial conditions I have that, cats object_0, collect object_10 object_2, collect object_5 object_1, collect object_6 object_1, collect object_7 object_1, collect object_8 object_2, collect object_9 object_2, hand object_11, hand object_12, hand object_13, hand object_14, next object_0 object_8, next object_11 object_10, next object_12 object_5, next object_13 object_7, next object_14 object_9, next object_3 object_6, next object_4 object_9, sneeze object_3, sneeze object_4, spring object_5, spring object_8, stupendous object_1, stupendous object_2, texture object_10, texture object_5, texture object_6, texture object_7, texture object_8 and texture object_9.
    My goal is to have that next object_11 object_9, next object_12 object_8, next object_13 object_5 and next object_14 object_7.
    """
    plan_4 = solve_planning_problem(example_4)
    print(f"Plan 4 Output:\n{plan_4}\n")

if __name__ == "__main__":
    test_planning()
