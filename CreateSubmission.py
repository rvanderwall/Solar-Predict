from src.DataWriters import Submission
from src.Tests import verify_data_looks_ok as vd

__author__ = 'robertv'

import pickle
from src.DataReaders import StationTrainingData, StationInfo, GEFS_Data_Set
from src.Predictor import find_fit_parameters, get_prediction

show_plots=False
training_data_file = "Data/train.csv"
station_info_file = "Data/station_info.csv"
submission_file = 'MySubmission.csv'


def main():
    # Get Station data and make sure it looks OK
    station_info = StationInfo.StationInfo(station_info_file)
    solar_output_training_data = StationTrainingData.StationTrainingData(training_data_file, station_info)
    if show_plots:
        vd.show_output_vs_elevation(station_info, solar_output_training_data)

    (training_data_set, test_data_set) = GEFS_Data_Set.get_GEFS_data_from_files(solar_output_training_data, station_info)

    fitted_theta = read_theta(training_data_set, solar_output_training_data)
    print "Found fitting parameters:"
    print fitted_theta.shape
    print fitted_theta[0,:]
    vd.show_data_and_fit(training_data_set, "GEFS", station_info, solar_output_training_data, fitted_theta)

    #  See how well we predict known data
    prediction_of_training_data = get_prediction(fitted_theta, training_data_set, station_info)
    print "Predicting based on training data.  (Should be really close since it was used to train."

    # TODO:  Split data into train, test, cv so that this cost is meaningful
    cost = solar_output_training_data.cost(prediction_of_training_data[:,1:])
    print cost
    # 6886890.09966
    # 6684833.00742
    # 6003394.44515
    # 2858323.32509 #linear regression with one gefs dataset
    # 2784222.93992
    # 2606206.72594
    # 2448761.1464  #linear regression with all gefs datasets
    # 2477599.93918 #gradient Descent alpha = 100000, i = 500
    # 2477596       # GD alpha = 50000, i = 1000
    # 2410906.84649 # GD alpha = 50000, i = 2000
    # 2410911.57549 # GD alpha = 10000, i = 10000

    prediction_of_test_data = get_prediction(fitted_theta, test_data_set, station_info)

    sf = Submission.SubmissionFile(submission_file)
    sf.write(station_info.stations, prediction_of_test_data)

    #
    #[ -1.39487363e+08  -7.53558699e+04   4.10290422e+04  -1.30996173e+06
    #  -4.50835587e+05  -1.08752388e+06   2.55257619e+06   1.55099741e+05
    #   2.63289685e+04   1.31949752e+04  -6.03800973e+05   1.78944543e+03
    #  -5.05873758e+04   8.15503180e+07   2.16171762e+08  -2.00872280e+08]
    #
    #
    #[ -1.85632097e+08  -1.96099058e+04   2.88545698e+04   5.79631731e+04
    #   2.88024204e+04   7.96622909e+04   7.33714865e+04   1.02285957e+04
    #   1.50575069e+04   1.16820387e+05  -5.28453198e+05   1.12695994e+03
    #  -6.77953404e+04  -1.04709534e+08   4.86503753e+06   4.91656859e+06]


def find_fitting_theta(training_data_set, solar_output_training_data):
    fitted_theta = find_fit_parameters(training_data_set, solar_output_training_data)
    return fitted_theta

def read_theta(training_data_set, solar_output_training_data):
    try:
        print "read theta from pk files"
        with open('../theta.pk', 'rb') as input:
            theta = pickle.load(input)

    except IOError:
        theta = find_fitting_theta(training_data_set, solar_output_training_data)

        print "write theta to pk files"
        with open('../theta.pk', 'wb') as output:
            pickle.dump(theta, output, pickle.HIGHEST_PROTOCOL)

    print "theta retrieval complete"
    return theta


if __name__=="__main__":
   main()