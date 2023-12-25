import Sheath

def a(x, y):
    print("a")
    print(x+y)

def b(x, y):
    print("b")
    print(x*y)

def c(y):
    print("c")
    print(y*y)

def d(x):
    print("d")
    print(x*x)

'''
The code below utilizes sheath the create and permutate a SM similar to the one graphed below
                      (a)
                      / \
                    (b) (c)
                    /
                  (d)


'''

sm = Sheath.Sheath()
sm.add("a", "b", b, [3, 2])
sm.add("a", "c", c, [2])
sm.add("b", "d", d, [3])
sm.states
sm.run(start_state="a", reset_function=a, args=[3,2])