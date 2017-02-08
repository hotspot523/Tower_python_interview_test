========================
Tower Python coding test
========================


Background
~~~~~~~~~~

A team at tower is implementing the infrastructure for automatic trading strategies.
They make the following design decision: a strategy is any class that implements a method called 'handle_tick'.
The method 'handle_tick' behaves as follows:

- take a Tick as argument
- returns None if no actions must be taken
- returns an Order object if we need to buy or sell a stock.

A Tick is the representation of an order being executed on the market. 
An Order is the representation of an order being sent to the market by our strategy.

The team creates the data objects (Order and Tick) and the interface for a strategy (the Strategy class).

The team then proceeds to implement their first strategy: scalping.

The scalping strategy, implemented in the ScalpingStrategy class, is very simple: 

- it buys stocks after certain conditions are met
- it sells positions on stocks if their price sinks below a certain threshold (the loss limit) 
- it sells positions on stocks if their price rises over a certain threshold (the scalp threshold) 

Being good at their job, the team members decide to use TDD and create a test case to verify the behavior of the ScalpingStragegy class before they start implementing it.


Your task
~~~~~~~~~

Implement the ScalpingStrategy class and make all the test cases pass.

How to run the tests
~~~~~~~~~~~~~~~~~~~~

Simply run the test module file:

  python tests/scalping_strategy_tests.py


Note: the test file must not be modified. Tick, Order and Strategy classes must not be modified either.
Feel free to add new modules, classes, or to modify the ScalpingStrategy class in any way possible.


