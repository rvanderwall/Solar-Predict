__author__ = 'robertv'

__author__ = 'robertv'

import numpy as np
import numpy.matlib


def feature_normalization_constants(X):
    """
        normalize_features(X) returns a normalized version of X where
        the mean value of each feature is 0 and the standard deviation
        is 1.
        returns mu and sigma so values can be renormalized.
    :param X:
    :return: mu, sigma
    """
    assert isinstance(X, np.ndarray)
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    sigma[sigma == 0] = 1 # If sigma is 0, all elements are the same, just use as is.
    return (mu, sigma)

def normalize_features(X, mu, sigma):
    m = X.shape[0]
    muV = np.matlib.repmat(mu,m,1)
    sigmaV = np.matlib.repmat(sigma, m, 1)
    X_norm = (X - muV) / sigmaV
    return X_norm

def normalize_one_value(x, mu, sigma):
    x_norm = (x - mu) / sigma
    return x_norm

def restore_one_value_from_normalized_value(x_norm, mu, sigma):
    x = (x_norm * sigma) + mu
    return x

def reconstruct_theta(theta, mu, sigma):
    """
        rebuild theta so that it can be applied to the original unnormalized values
        theta0 = theta0 - sum(mu * theta / sigma)
        theta i = theta i / sigma

        also, mu and sigma won't have the 1's column since normalization was done before it is prepended
    @param theta:
    @param mu:
    @param sigma:
    @return:
    """
    rebuilt_theta = np.zeros(shape=theta.shape)
    rebuilt_theta[0] = theta[0]
    for feature in range(1,theta.shape[0]):
        rebuilt_theta[feature] = theta[feature] / sigma[feature - 1]
        rebuilt_theta[0] = rebuilt_theta[0] - rebuilt_theta[feature] * mu[feature - 1]

    return rebuilt_theta


def prepend_column_of_ones(x):
    columnOfOnes = np.ones((x.shape[0],1))
    return np.append(columnOfOnes, x, 1) # feature_0 is '1'


def check_data_types_and_shapes(X, y, theta):
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert isinstance(theta, np.ndarray)
    m = y.shape[0]
    n = X.shape[1]
    assert X.shape[0] == m
    assert theta.shape[0] == n
    return m, n


def map_features(X1, X2, degree):
    """
%   Returns a new feature array with more features, comprising of
%   X1, X2, X1.^2, X2.^2, X1*X2, X1*X2.^2, etc..

    :param X:
    :param degree:
    """
    m = X1.shape[0]
    out = None
    for i in range(1,degree+1):
       for j in range (0,i+1):
         newFeature = np.multiply(np.power(X1,(i-j)), np.power(X2,j))
         if out == None:
             out = newFeature.reshape((m,1))
         else:
             out = np.append(out, newFeature.reshape((m,1)), 1)
    return out


