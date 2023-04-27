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
    cost = 0

    for i in range(m):
        cost += cost_func(x[i], y[i], w, b)
    cost = cost / (2.0 * m)

    return cost


# def gradient(x, y, w, b):
#     dw = (linear_func(x, w, b) - y) * x
#     db = linear_func(x, w, b) - y
#     return dw, db


def gradient(x, y, w, b, max_grad=100.0):
    # Cast input data and parameters to float64
    x = x.astype(np.float64)
    y = y.astype(np.float64)
    w = np.float64(w)
    b = np.float64(b)

    # Compute gradients
    dw = (linear_func(x, w, b) - y) * x
    db = linear_func(x, w, b) - y

    # Clip gradients to maximum value
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


def gradient_descent_returns_weights_and_biases(x, y, alpha, iters, init_w=0, init_b=0):
    w = init_w
    b = init_b
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

    return x_model, y_model, cost_vals, w, b


def mean_squared_error(y_true, y_pred):
    """
    Calculate the mean squared error between true and predicted values.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated target values.

    Returns
    -------
    mse : float
        Mean squared error.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    if y_true.shape != y_pred.shape:
        raise ValueError("Input arrays must have the same shape.")

    mse = np.mean((y_true - y_pred) ** 2)
    return mse


def calc_correlation_p_value(x, y):
    if len(x) != len(y):
        raise ValueError("Input arrays must have the same length.")

    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    x_diff = x - x_mean
    y_diff = y - y_mean

    numerator = np.sum(x_diff * y_diff)
    denominator = np.sqrt(np.sum(x_diff ** 2) * np.sum(y_diff ** 2))

    if denominator == 0:
        raise ValueError(
            "The denominator is zero, Pearson correlation coefficient cannot be calculated.")

    correlation_coefficient = numerator / denominator

    t_score = correlation_coefficient * \
        np.sqrt((n - 2) / (1 - correlation_coefficient ** 2))
    p_value = (1 - stats.t.cdf(np.abs(t_score), n - 2)) * 2

    return correlation_coefficient, p_value
