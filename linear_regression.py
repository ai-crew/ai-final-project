def linear_func(x, w, b):
    return w * x + b


def cost_func(x, y, w, b):
    return (linear_func(x, w, b) - y) ** 2


def total_cost(x, y, w, b):
    """
    Computes the total cost of a linear regression model
    with parameters w and b.
    Arguments:
    x: an array of the input values of each point
    y: an array of the corresponding output values
    w: the slope of the linear model
    b: the y-intercept of the linear model
    Returns:
    cost: a float denoting the total cost
    """
    m = len(x)
    cost = 0

    for i in range(m):
        cost += cost_func(x[i], y[i], w, b)
    cost = cost / (2.0 * m)

    return cost


def gradient(x, y, w, b):
    dw = (linear_func(x, w, b) - y) * x
    db = linear_func(x, w, b) - y
    return dw, db


def gradient_descent(x, y, alpha, iters):
    """
    Performs gradient descent and returns the final x and y
    values of the estimation model.
    Arguments:
    x: an array of the input values of each point
    y: an array of the corresponding output values
    alpha: the learning rate
    iters: the number of times gradient descent is performed
    Returns:
    x_model: an array of the input values of each point
    y_model: an array of the corresponding output values returned from the final model
    cost_vals: an array that records the total cost of the linear model at each iteration
    """
    w = 0
    b = 0
    m = len(x)
    cost_vals = []
    for i in range(iters):
        dw = 0.0
        db = 0.0
        for j in range(m):
            dw_curr, db_curr = gradient(x[j], y[j], w, b)
            dw += dw_curr
            db += db_curr
        dw = dw / m
        db = db / m

        w = w - alpha * dw
        b = b - alpha * db
        cost_vals.append(total_cost(x, y, w, b))

    x_model = []
    y_model = []
    for i in range(m):
        x_model.append(x[i])
        y_model.append(linear_func(x[i], w, b))

    return x_model, y_model, cost_vals
