===============================
dgim
===============================

.. image:: https://badge.fury.io/py/dgim.png
    :target: http://badge.fury.io/py/dgim

.. image:: https://travis-ci.org/simondolle/dgim.png?branch=master
        :target: https://travis-ci.org/simondolle/dgim

.. image:: https://pypip.in/d/dgim/badge.png
        :target: https://pypi.python.org/pypi/dgim


Python implementation of the dgim algorithm: Compact datastructure to estimate the number of "True" in the last N elements of a boolean stream.

Features
--------

* Estimation of the number of "True" statements in the last N element of a boolean stream
* Low memory footprint.
* Configurable error rate

Installation
------------

At the command line::

    $ pip install dgim

Usage
-----

Sample code::

  from dgim import Dgim
  dgim = Dgim(N=32, error_rate=0.1)
  for i in range(100):
      dgim.update(True)
  dgim_result = dgim.get_count() # 30 (exact result is 32)


Documentation
-------------

https://dgim.readthedocs.org.


License
-------

The project is licensed under the BSD license.

Authors
-------

* Simon Dollé <simon.dolle@gmail.com>
* No other contributor yet. Why not joining?

How to contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

References
----------
- Datar, Mayur, et al. "Maintaining stream statistics over sliding windows."
  SIAM Journal on Computing 31.6 (2002): 1794-1813.
- Rajaraman, Anand, and Jeffrey David Ullman. Mining of massive datasets. Cambridge University Press, 2011. Chapter 4. http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
- Mining of Massive Datasets Coursera MOOC: http://infolab.stanford.edu/~ullman/mmds/ch4.pdf

.. _`the repository`: http://github.com/simondolle/dgim
.. _AUTHORS: https://github.com/simondolle/dgim/blob/master/AUTHORS.rst

