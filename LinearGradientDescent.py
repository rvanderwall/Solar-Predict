__author__ = 'robertv'
__author__ = 'rlv'
import numpy as np
from src.GradientDescentCoreHelpers import prepend_column_of_ones, check_data_types_and_shapes

def linear_cost_function_MAE(X, y, theta, l):
    """
        MAE - Mean Average Error
        Computes the cost function of a linear regression
        Cost is sum of squares of differences between predicted and actual
        The lambda parameter is for regularization to prevent overfitting
    :param X: input array, prepended with X0
    :param y: output array, actual values
    :param theta: parameters for h()
    :return: cost
    """
    (m, n) = check_data_types_and_shapes(X, y, theta)

    predictedValues = predict_linear_value(X, theta)
    error = predictedValues - y
    err = np.abs(error)
    J = (1.0 / m) * np.sum(err)
    regularize_term = (l / (2*m)) * np.sum(theta)

    J = J + regularize_term
    return J

def derivative_of_linear_cost_function_MAE(X, theta, predictor_func, y):
    (m, n) = check_data_types_and_shapes(X, y, theta)
    predict = predictor_func(X, theta)
    error = predict - y
    error[error < 0] = -1
    error[error > 0] = 1
    sumProd = np.dot(error.T, X).T
    gradient = (1.0/m) * sumProd
    return gradient

def linear_cost_function_MES(X, y, theta, l):
    """
        Computes the cost function of a linear regression
        Cost is sum of squares of differences between predicted and actual
        The lambda parameter is for regularization to prevent overfitting
    :param X: input array, prepended with X0
    :param y: output array, actual values
    :param theta: parameters for h()
    :return: cost
    """
    (m, n) = check_data_types_and_shapes(X, y, theta)

    predictedValues = predict_linear_value(X, theta)
    error = predictedValues - y
    errSquared = np.square(error)
    J = (1.0 / (2*m)) * np.sum(errSquared)
    regularize_term = (l / (2*m)) * np.sum(theta)

    J = J + regularize_term
    return J

def derivative_of_linear_cost_function_MES(X, theta, predictor_func, y):
    (m, n) = check_data_types_and_shapes(X, y, theta)
    predict = predictor_func(X, theta)
    error = predict - y
    sumProd = np.dot(error.T, X).T
    gradient = (1.0/m) * sumProd
    return gradient

def predict_linear_value(X, theta):
    h = X.dot(theta)
    return h


def linear_gradient_descent(x, y, theta, alpha, num_iters):
    """
        performs a GradientDescent minimization on the data in x, y, using theta as start params
    :param x: raw input data, not normalized, not pre-pended with a 1 column
    :param y: label data
    :param theta:
    :param alpha:
    :param num_iters:
    :return:
    """
    X = prepend_column_of_ones(x) # feature_0 is '1'
    (m, n) = check_data_types_and_shapes(X, y, theta)
    (theta, J_History) = _gradient_descent_with_X0_set(X, y, theta, alpha, num_iters, predict_linear_value)
    return theta, J_History


# Returns theta, J_History
def _gradient_descent_with_X0_set(X, y, theta, alpha, num_iters, predictor_func):
    (m, n) = check_data_types_and_shapes(X, y, theta)

    J_History = np.zeros((num_iters,1))
    for iter in range(0, num_iters):

        gradient = derivative_of_linear_cost_function_MAE(X, theta, predictor_func, y)
        theta = theta - alpha * gradient

        # Save the cost J in every iteration
        J_History[iter] = linear_cost_function_MAE(X, y, theta, 0);

    return theta, J_History



