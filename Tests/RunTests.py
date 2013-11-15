__author__ = 'robertv'


import StationInfoTests as sit
import StationTrainingDataTests as stdt
import PredictorTests as pt

print "Run Tests"
sit.test_construct()
sit.test_find_lat_lon()
sit.test_translate()

stdt.verify_cost_function_when_identical()
stdt.verify_cost_function_when_different_station()
stdt.verify_cost_function_when_different_times()

pt.test_data_averager()
pt.test_translator()
pt.test_fit_finder()
pt.test_fit_finder_for_two_in_set()
pt.test_cost_function_MAE_when_cost_zero()
pt.test_cost_function_MAE_when_cost_nonzero()


