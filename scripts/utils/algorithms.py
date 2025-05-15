#!/usr/bin/env python
#!/usr/bin/python3

# The Galilean Model
class Galilean:
    def __str__(self) -> str:
        return "Galilean Model"

def calc_x_trajectory(v1:float, t:float)->float:
    """
    Calculate horizontal trajectory based on given parameters.

    Keyword Arguments:
    - v1 (float): starting horizontal velocity (metric units - m/s)
    - t (float): time in seconds
    """
    return v1 * t

def calc_y_trajectory(v1:float=None, v2:float=None, t:float=None, x:float=None, a:float=-9.81)->float:
    """
    Calculate the vertical trajectory based on given parameters.

    Keyword Arguments:
    - v1 (float): starting horizontal velocity (metric units - m/s)
    - v2 (float): starting vertical velocity (metric units - m/s)
    - t (float): time in seconds
    - x (float): horizontal position
    - a (float): constant downward acceleration due to gravity [default: 9.81] (metric units)
    """
    y = None

    # TODO: continue here -- test
    # vertical trajectory in relation to horizontal position:
    if v1 is not None and v2 is not None and x is not None:
        # y = ((v2/v1) * x) + ((a * (x**2)) / (2*(v1**2)))
        y = (v2/v1)*x + ((a * (x**2)) / (2 * (v1**2)))

    return y


def plot_trajectory(v1:float=None, v2:float=None, x:float=None, y:float=None, a:float=-9.81):
    import matplotlib.pyplot as plt
    xs = [x/100 for x in list(range(201))]  # [0.0, 0.01, 0.02, 0.03 ... 1.97, 1.98, 1.99, 2.0]

    # calculate vertical trajectory
    if y is None and v1 is not None and v2 is not None and len(xs):
        ys = [calc_y_trajectory(v1=v1, v2=v2, x=x, a=a) for x in xs]
    else:
        ys = [x/100 for x in list(range(201))]  # [0.0, 0.01, 0.02, 0.03 ... 1.97, 1.98, 1.99, 2.0]

    plt.plot(xs,ys)
    plt.title('The Trajectory of a Thrown Ball')
    plt.xlabel('Horizontal Position of Ball')
    plt.ylabel('Vertical Position of Ball')
    plt.axhline(y = 0)
    plt.show()
    return

if __name__ == '__main__':

    # plot trajectory of a thrown ball with:
    v1 = 0.99 # horizontal speed => 0.99 meters per second
    v2 = 9.9  # vertical speed   => 9.9 meters per second
    plot_trajectory(v1=v1, v2=v2)
