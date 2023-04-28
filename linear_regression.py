import numpy as np
import scipy.stats as stats


def linear_func(x, w, b):
    return float(w) * float(x) + float(b)


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
    return sum(cost_func(x[i], y[i], w, b) for i in range(m)) / (2.0 * m)


def gradient(x, y, w, b, max_grad=100.0):
    x = x.astype(np.float64)
    y = y.astype(np.float64)
    w = np.float64(w)
    b = np.float64(b)

    dw = (linear_func(x, w, b) - y) * x
    db = linear_func(x, w, b) - y

    # Clip gradients to maximum value to avoid exploding gradients
    dw = np.clip(dw, -max_grad, max_grad)
    db = np.clip(db, -max_grad, max_grad)

    return dw, db


def gradient_descent(x, y, alpha, iters, init_w=0, init_b=0):
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
    w = init_w
    b = init_b
    m = len(x)
    cost_vals = []
    for _ in range(iters):
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


def gradient_descent_returns_weights_and_biases(x, y, alpha=0.001, iters=100, init_w=0, init_b=0):
    w = init_w
    b = init_b
    m = len(x)
    x = x.astype(np.float64)
    y = y.astype(np.float64)
    cost_vals = []
    for _ in range(iters):
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

    return x_model, y_model, cost_vals, w, b