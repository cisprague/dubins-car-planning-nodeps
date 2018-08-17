# Christopher Iliffe Sprague
# sprague@kth.se

from dubins import Car

''' <<< write your code below >>> '''

# Dynamics window planning;
# among the simplest of methods.

from math import pi

def predict(car, x, y, theta, phi, T):

    '''
    Returns the trajectory of the Dubin's car with the steering angle
    phi for duration T, from a given state (x, y, theta).
    '''

    # seed time
    t = 0

    # list of states, control, and times
    xl     = []
    yl     = []
    thetal = []
    phil   = []
    tl     = []

    # simulate for prescribed time
    while t < T:
        x, y, theta = car.step(x, y, theta, phi)
        t += car.dt
        xl.append(x)
        yl.append(y)
        thetal.append(theta)
        phil.append(phi)
        tl.append(t)

    return xl, yl, thetal, phil, tl

def obstacle_cost(car, xl, yl):

    '''
    Returns cost related to the trajectory's proximity to obstacles.
    Minimising this cost will result in minimising proximity to obstacles.
    '''

    # minimum distance
    dmin = float("inf")

    # iterate through each state
    for x, y in zip(xl, yl):
        # iterate through each obstacle
        for ob in car.obs:
            # relative position
            xr = ob[0] - x
            yr = ob[1] - y
            # distance to obstacle
            d = (xr**2 + yr**2)**0.5
            # if colliding with obstacle
            if d <= ob[2] + 0.3:
                return float("inf")
            elif d < dmin:
                dmin = d

    # if there wasn't a collision
    return 1.0/dmin

def target_cost(car, x, y, theta):

    '''
    Returns cost related to a point's proximity to the target.
    Minimsing this cost will minimise distance to target.
    '''

    # relative position to target
    x = car.xt - x
    y = car.yt - y

    # distance to target
    d = (x**2 + y**2)**0.5

    # return cost
    return d

def boundary_cost(car, xl, yl):

    # closest distance
    dmin = float("inf")

    # iterate through states
    for x, y in zip(xl, yl):
        if x < car.xlb or y > car.yub  or y < car.ylb:
            return float("inf")

    # if no obstacles were encountered
    return 0.0

def control(car, x, y, theta, T):

    # best cost)
    costmin = float("inf")

    # Dubin's proved, through Pontryagin's maximum principle, that
    # the optimal steering angle is one the extreme or zero.
    for phi in [-pi/4.0, 0.0, pi/4.0]:

        # predict trajectory
        xl, yl, thetal, phil, tl = predict(car, x, y, theta, phi, T)

        # compute cost
        cost1 = target_cost(car, xl[-1], yl[-1], thetal[-1])
        cost2 = obstacle_cost(car, xl, yl)
        cost3 = boundary_cost(car, xl, yl)
        cost = cost1 + cost2 + cost3

        # record minimum cost
        if cost <= costmin:
            costmin = cost
            xlmin     = xl
            ylmin     = yl
            thetalmin = thetal
            philmin   = phil
            tlmin     = tl

    return xlmin, ylmin, thetalmin, philmin, tlmin

def run(car):

    # lists
    xl     = [car.x0]
    yl     = [car.y0]
    thetal = [0]
    phil   = []
    tl     = [0]

    safe, done = True, False
    while safe and not done:

        # best steering angle
        xll, yll, thetall, phill, tll = control(car, xl[-1], yl[-1], thetal[-1], 1)
        phi = phill[-1]

        # step with that control
        x, y, theta = car.step(xl[-1], yl[-1], thetal[-1], phi)
        #print("x", x, "y", y, "theta", theta)

        for ob in car.obs:
            if ((ob[0]-x)**2 + (ob[1]-y)**2)**0.5 <= ob[2]:
                safe = False
                break

        if ((car.xt-x)**2 + (car.yt-y)**2)**0.5 <= 0.1:
            done = True

        # records states
        xl.append(x)
        yl.append(y)
        thetal.append(theta)
        phil.append(phi)
        tl.append(tl[-1] + car.dt)

    # return lists
    return xl, yl, thetal, phil, tl


''' <<< write your code below >>> '''

def solution(car):

    ''' <<< write your code below >>> '''

    pxl, yl, thetal, phil, tl = run(car)
    controls = phil
    times = tl

    ''' <<< write your code below >>> '''
    return controls, times

if __name__ == "__main__":

    from dubins import evaluate
    # random obstacles (student)
    car, xl, yl, thetal, ul, tl, done = evaluate(solution, "E", random=True)
    print(done)
    # precomputed obstacle 1 (student)
    car, xl, yl, thetal, ul, tl, done = evaluate(solution, "E", random=False)
    print(done)
    # provide obstacles (teacher)
    car, xl, yl, thetal, ul, tl, done = evaluate(solution, "E", obs=[(5, 5, 1), (1.5, 1.5, 1)])
    print(done)
