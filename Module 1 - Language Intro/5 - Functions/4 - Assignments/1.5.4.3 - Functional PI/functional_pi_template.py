import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """
    a = 1
    b = (1/(math.sqrt(2)))
    t = (1/4)
    p = 1

    error = math.inf
    while error >= target_error:
    #for i in range(1,10):
        a_next = (a+b)/2
        b_next = math.sqrt(a*b)
        p_next = 2*p
        t_next = (t)-(p*(((a_next)-a)**2))
        a = a_next
        b = b_next
        p = p_next
        t = t_next
        pi_estimate = ((a+b)**2)/(4*t)
        error = abs(math.pi - pi_estimate)
    

    # change this so an actual value is returned
    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
