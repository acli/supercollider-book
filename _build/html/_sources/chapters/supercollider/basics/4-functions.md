(sec-functions)=
# Functions

In ``sclang``, functions are first-class objects.
Therefore, a function can be an argument of another function.
The language drives the programmer to use this fact in various ways.
For example, control structures in ``sclang`` are functions.

## Definition

To define a function, we encapsulate its content by curly brackets.
To execute it, we call ``value`` on it:

```isc
(
~func = {
  var x = 10;
  x;
};
~func.value();   // returns 10
)
```

We can omit ``value`` to call a function:

```isc
~func.();   // returns 10
```

This looks a little bit weird, but it works just fine.

In ``sclang`` there is no ``return`` keyword.
We only have to call ``func.value`` for functions and not for methods of an object or class.
A function always returns the content of the last evaluated statement, in this case ``x``.
In my personal opinion, an additional keyword can make the code more readable.

To see what I mean by making use of functions as first-class objects, we can look at the [control structures](https://doc.sccode.org/Reference/Control-Structures.html).
``if`` is in fact, a function that takes three arguments:

1. the condition
2. a function that is executed if the condition is ``true``
3. a function that is executed if the condition is ``false``
   
Compare the following code that returns ``10`` if the argument of ``func`` is ``10`` and a random integer between 0 and 19 (20 excluded).

```isc
(
var func = {
    arg input;
    if(input == 10, {
        input;
    }, {
        rand(20);
    });
};
func.(11).postln;
func.(11).postln;
func.(11).postln;
)
```

It is important to understand, that the function ``{rand(20);}`` is evaluated each time we call ``func.value(11);``.
Again, we can either write ``rand(20);`` or ``20.rand;``.

## Closures

If we want the ``func`` to return the same randomly chosen value each time it is called, we can use a [Closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)).
In short, a [Closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)) is a function combined with a set of variables that are neither defined within the function nor are arguments of the functions.

```isc
(
var r = rand(20);
var func = {
    arg input;
    if(input == 10, {
        input;
    }, {
        r;
    });
};
func.(11).postln;
func.(11).postln;
func.(11).postln;
)
```

Of course, we can do the same without using a [Closure](https://en.wikipedia.org/wiki/Closure_(computer_programming))

```isc
(
var val = rand(20);
var func = {
    arg input, r;
    if(input == 10, {
        input;
    }, {
        r;
    });
};
func.(11, val).postln;
func.(11, val).postln;
func.(11, val).postln;
)
```

but since functions are first-class objects it is often convenient to use a [Closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)).

## Arguments

Let's look at another example:

```isc
(
var add = {
    arg a = 5, b;
    a + b;
};
add.(a: 6, b: 11) // returns 17
add.(b: 11) // returns 16
)
```

Similar to ``Python``, one can define a default value for each argument, and we can ignore the order if we add the names.
To define a specific argument in the function call, we have to use ``:`` instead of ``=``.
Furthermore, there is another rather strange shortcut:

```isc
(
var add = {|a = 5, b|
    a + b;
};
add.(b: 11) // returns 16
)
```

If your arguments are the elements of an array you can also call the function and unpack the array using the ``*`` operator:

```isc
(
var values = [2, 9];
var add = {|a, b|
    a + b;
};
add.(*values) // returns 11
)
```

## Duplicating

To test for the first ``n`` prime numbers starting from zero to ``n-1`` there is a very short expression one can use:

```isc
(
var n = 10;
// [ false, false, true, true, false, true, false, true, false, false ]
{|k|k.isPrime}!n;
)
```

This can be even shortened:

```isc
(
var n = 10;
// [ false, false, true, true, false, true, false, true, false, false ]
_.isPrime!n;
)
``````

The ``!`` operator functions identically to the ``.dup`` method.
It returns an [Array](sec-array) consisting of the results from ``n`` evaluations of the given function. 
If the function has a single argument, it will utilize values within the range from 0 to ``n-1``.
If the function has multiple arguments, this still holds true, but we must duplicate it via an array with an equivalent number of arguments.

```isc
{|x,y|(x+y)}.dup([3,3]); // [ [ 0, 1, 2 ], [ 1, 2, 3 ], [ 2, 3, 4 ] ]
{|x,y|(x+y)}![3,3];      // [ [ 0, 1, 2 ], [ 1, 2, 3 ], [ 2, 3, 4 ] ]
```

Later we will utilize ``dup`` to construct a complex graph consisting of many [unit generators](sec-ugens) with a few lines of code, a technique that is called [multichannel expension](sec-mce).

(sec-function-composition)=
## Compositions

In ``sclang`` the mathematical operation of composing functions, i.e., $f \circ g$ is approxiated by the ``<>`` operator.

```isc
f = {arg x; x*x};
g = {arg x; 2*x};

f.(5); // 25
g.(5); // 10

h = f <> g;
h.(5); // f(g(5)) = (2*5)^2 = 10 * 10 = 100
```

## A Common Pitfall

A common error to make, which is hard to spot, is when we generate multiple duplicates, but we want to duplicate the evaluation of a function rather than its return value.
For example, let us create an [Array](sec-array) with five random values:

```isc
// all values are identical
Array.fill(5, 1.0.rand);
```

That's different from what we wanted.
``fill`` expects a function to be evaluated, but we define as a second argument a random value.
This value gets copied five times.
The following is even more dangerous:

```isc
// all values are identical
(
a = Array.fill(5, []);
a[0] = a[0].add(1)
a // [ [ 1 ], [ 1 ], [ 1 ], [ 1 ], [ 1 ] ]
)
```

The same problem occurs.
We only create one subarray ``[]``, which gets copied **by reference**!
To fix both problems, we have to use a function instead:

```isc
Array.fill(5, {1.0.rand}); // all values are different
Array.fill(5, {[]});       // all subarrays are different
```