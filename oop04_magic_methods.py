#!/usr/bin/env python
# coding: utf-8

# Magic Method Code Exercise
# 
# Read through the code below and fill out the TODOs. You'll find a cell at the
# end containing unit tests. After you've run the code with the Gaussian 
# class, run the unit tests to check that the code functions as expected.
# 
# The unit tests expect a file in the same directory called 'oop04_numbers.txt'

import math
import matplotlib.pyplot as plt

class Gaussian():
    """ Gaussian distribution class for calculating and 
    visualizing a Gaussian distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file
            
    """
    def __init__(self, mu = 0, sigma = 1):
        
        self.mean = mu
        self.stdev = sigma
        self.data = []

    def calculate_mean(self):
        """Method to calculate the mean of the data set.
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        Description: Calculates the mean of the data set from self.data, changes
                     the value of the mean attribute to be the mean of the data 
                     set, and returns the mean.
        """
        total = 0
        if(len(self.data) == 0):
            self.mean = 0
            return self.mean
        for each in self.data:
            total += each
        self.mean = (total/float(len(self.data)))
        return self.mean

    def calculate_stdev(self, sample=True):

        """Method to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population
        
        Returns: 
            float: standard deviation of the data set
    
        """
        total = 0.0

        factor = len(self.data)
        if (sample == True):
            factor = (len(self.data)-1.0)

        if self.mean == 0:
            self.calculate_mean()
        for each in self.data:
            total += (float(each) - self.mean) ** 2

        mean_of_squared_differences = (total/factor)
        self.stdev = math.sqrt(mean_of_squared_differences)
        return self.stdev
        

    def read_data_file(self, file_name, sample=True):
    
        """
        Method to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute. 
        After reading in the file, the mean and standard deviation are calculated
                
        Args:
            file_name (string): name of a file to read from
        
        Returns:
            None
        """
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list
        self.calculate_mean()
        self.calculate_stdev(sample)
        return
        
    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.xlabel('Test1')
        plt.ylabel('Blue1')
        plt.title('Green3')
        plt.hist(self.data)
        plt.show()
        
    def pdf(self, x):
        """
        Probability density function calculator for the gaussian distribution.
        
        Args:
            x (float): point for calculating the probability density function
        
        Returns:
            float: probability density function output
        """
        
        # Calculate the probability density function of the Gaussian 
        # distribution at the value x. You'll need to use self.stdev and 
        # self.mean to do the calculation
        main = 1.0 / (self.stdev * math.sqrt(2*math.pi))
        second = math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
        return main * second

    def plot_histogram_pdf(self, n_spaces = 50):

        """Method to plot the normalized histogram of the data and a plot of the 
        probability density function along the same range
        
        Args:
            n_spaces (int): number of data points 
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """        
        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)
        
         # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        
        """Magic method to add together two Gaussian distributions
    
        Description:
            When summing two Gaussian distributions, the mean value is the sum
            of the means of each Gaussian.
        
            When summing two Gaussian distributions, the standard deviation is 
            the square root of (stdev_one ^ 2 + stdev_two ^ 2)

        Args:
            other (Gaussian): Gaussian instance
            
        Returns:
            Gaussian: Gaussian distribution
            
        """        
        result = Gaussian()
        
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt((self.stdev ** 2) + (other.stdev ** 2))

        return result

    def __repr__(self):
    
        """Magic method to output the characteristics of the Gaussian instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        
        # TODO: Return a string in the following format - 
        # "mean mean_value, standard deviation standard_deviation_value"
        # where mean_value is the mean of the Gaussian distribution
        # and standard_deviation_value is the standard deviation of
        # the Gaussian.
        # For example "mean 3.5, standard deviation 1.3"
        answer = 'mean ' + str(self.mean) + \
                 ', standard deviation ' + str(self.stdev)
        return answer

import unittest

class TestGaussianClass(unittest.TestCase):
    def setUp(self):
        self.gaussian = Gaussian(25, 2)

    def test_initialization(self): 
        self.assertEqual(self.gaussian.mean, 25, 'incorrect mean')
        self.assertEqual(self.gaussian.stdev, 2, 'incorrect standard deviation')

    def test_pdf(self):
        self.assertEqual(round(self.gaussian.pdf(25), 5), 0.19947,         'pdf function does not give expected result') 

    def test_meancalculation(self):
        self.gaussian.read_data_file('oop04_numbers.txt', True)
        self.assertEqual(self.gaussian.calculate_mean(),         sum(self.gaussian.data) / float(len(self.gaussian.data)), 'calculated mean not as expected')

    def test_stdevcalculation(self):
        self.gaussian.read_data_file('oop04_numbers.txt', True)
        self.assertEqual(round(self.gaussian.stdev, 2), 92.87, 'sample standard deviation incorrect')
        self.gaussian.read_data_file('oop04_numbers.txt', False)
        self.assertEqual(round(self.gaussian.stdev, 2), 88.55, 'population standard deviation incorrect')

    def test_add(self):
        gaussian_one = Gaussian(25, 3)
        gaussian_two = Gaussian(30, 4)
        gaussian_sum = gaussian_one + gaussian_two
        
        self.assertEqual(gaussian_sum.mean, 55)
        self.assertEqual(gaussian_sum.stdev, 5)

    def test_repr(self):
        gaussian_one = Gaussian(25, 3)
        
        self.assertEqual(str(gaussian_one), "mean 25, standard deviation 3")
        
tests = TestGaussianClass()

tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)

unittest.TextTestRunner().run(tests_loaded)


# In[ ]:




