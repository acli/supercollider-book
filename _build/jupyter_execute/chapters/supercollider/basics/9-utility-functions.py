#!/usr/bin/env python
# coding: utf-8

# # Utility Functions
# 
# Since SuperCollider is used to generate sound and music, it has built-in functions that are special to the field of audio processing.
# I will introduce some of these functions which I think are most important and useful.
# 
# We perceive the frequency and the loudness of sound on a logarithmic scale.
# For example, doubling the frequency pushes the pitch, one, not two, octaves higher.
# However, we often want to deal with linear measures since humans are certainly imperfect at grasping non-linear relationships intellectually.
# Therefore, musicians use semitones instead of frequencies, see section [Notes & Midi Notes](sec-notes).
# 
# ## Frequency and Semitones
# 
# The function ``x.midiratio`` computes the factor to multiply a frequency $f$ such that it will be changed by ``x`` semitones.
# 
# The function ``y.midicps`` converts a [midi note](sec-midi-notes) into the respective frequency (assuming a twelve-tone equal temperament tuning (12-TET)).
# 
# The function ``z.cpsmidi`` is the inverse of ``midicps``.
# It transforms the frequency ``z`` into a midi note (possibly a floating point number). 
# 
# The function ``w.ratiomidi`` is the inverse of ``midiratio``.
# It transforms ``w`` the factor to multiply a frequency with into the semitones added to the pitch to have the same effect.
# 
# ```isc
# 60.midicps                      // 261.6255653006
# 1.midiratio                     // 1.0594630943591
# 1.0594630943591.ratiomidi       // 0.99999999999681 (almost 1)
# 
# 261.6255653006 * 1.midiratio    // 277.18263097681
# 277.18263097681.cpsmidi         // 60.999999999996 (almost 61)
# ```
# 
# Especially if we defines a [synth definition](sec-synths), we want to deal with frequencies.
# The [pattern library](sec-playing-events) takes care of many value conversions such that we can use midi notes, degrees of a scale etc out of the box.
# However, if we introduce more specific arguments we can not rely on that comfort.
# It is handy to offer tonal arguments such as ``detune`` in a measure of semitones because the linear scale is more meaningful to us.
# To be able to still use measures in frequency we use, for example, ``midicps``.
# 
# ## Amplitude and Decibel
# 
# To use decibal instead of amplitude, where 0 decibal is equivalent to 1.0 amplitude, we can make use of the built-in functions ``x.ampdb`` and ``y.dbamp``.
# ``x.ampdb`` converts a loudness value in amplitude into decibal.
# ``y.dbamp`` is the inverse operation.
# 
# ```isc
# -3.dbamp        // 0.70794578438414
# -3.dbamp.ampdb  // -3.0
# ```
# 
# ## Mappings
# 
# Transforming amplitude to decibal and vice verca is an application of a mapping, that maps one range of values into another.
# Such a mapping can be very useful in many other situations and ``sclang`` provides us with some useful utility functions such that we do not have to compute these mappings by ourselves.
# These utility function are functional operators, mapping a function to another function.
# 
# + ``linlin`` maps one linear function to another linear function
# + ``linexp`` maps a linear function to an exponential function
# + ``explin`` maps a exponential function to a linear function
# + ``expexp`` maps an exponential function to a linear function
# + ``lincurve`` like ``linexp`` but you can define the stepness of the exponential curve
# + ``curvelin`` line ``explin`` but you can define the stepness of the exponential curve
# 
# In the following I use a finite linear signal and a finite exponential signal generated by ``Line`` and ``XLine`` respectively to demonstrate the effect of all four transformations.
# 
# ```isc
# (
# var dur = 0.01;
# {Line.ar(dur: dur)}.plot(dur);
# {XLine.ar(dur, 1, 0.01)}.plot(dur);
# {Line.ar(dur: dur).linlin(
# 	inMin: 0, inMax: 1, outMin: 0, outMax: -1)}.plot(dur);
# {Line.ar(dur: dur).linexp(
# 	inMin: 0, inMax: 1, outMin: 0.01, outMax: 1)}.plot(dur);
# {XLine.ar(dur, 1, 0.01).explin(
# 	inMin: 0.01, inMax: 1, outMin: 0, outMax: 1)}.plot(dur);
# {XLine.ar(dur, 1, 0.01).expexp(
# 	inMin: 0.01, inMax: 1, outMin: -0.01, outMax: -1)}.plot(dur);
# )
# ```
# 
# Note that the argument ``outMax`` does not have to be the actual maximum of the function.
# ``inMin: 0.01, inMax: 1, outMin: -0.01, outMax: -1``
# means that the value ``0.01`` will be mapped to ``-0.01`` and the value ``1`` to ``-1``.
# If ``outMin`` > ``outMax`` the curve is mirrored.
# 
# 
# ```{figure} ../../../figs/supercollider/basics/mappings-plot.png
# ---
# width: 600px
# name: fig-mappings-plot
# ---
# The resulting plots of the code above.
# ```
# 
# ``lincurve`` and ``curvelin`` gives us a litte bit more control over the shape of the transformation.
# A positive ``curve`` value results in a convex, a negative value in a concave function.
# 
# ```isc
# (
# var dur = 0.01;
# {Line.ar(dur: dur).lincurve(
#   inMin: 0, inMax: 1, outMin: 0, outMax: 1, curve: 1)}.plot(dur);
# {Line.ar(dur: dur).lincurve(
#   inMin: 0, inMax: 1, outMin: 0, outMax: 1, curve: 5)}.plot(dur);
# {Line.ar(dur: dur).lincurve(
#   inMin: 0, inMax: 1, outMin: 0, outMax: 1, curve: -5)}.plot(dur);
# 
# {XLine.ar(0.01, 1, dur).curvelin(
#   inMin: 0.01, inMax: 1, outMin: 0, outMax: 1, curve: 1)}.plot(dur);
# {XLine.ar(0.01, 1, dur).curvelin(
#   inMin: 0.01, inMax: 1, outMin: 0, outMax: 1, curve: 10)}.plot(dur);
# {XLine.ar(0.01, 1, dur).curvelin(
#   inMin: 0.01, inMax: 1, outMin: 0, outMax: 1, curve: -5)}.plot(dur);
# )
# ```
# 
# ```{figure} ../../../figs/supercollider/basics/mappings-plot-2.png
# ---
# width: 600px
# name: fig-mappings-plot-2
# ---
# The resulting plots of the code above.
# ```
# (sec-utility-distributions)=
# ## Random Distributions
# 
# ``sclang`` offers many useful functions to generate pseudorandom values.
# This is especially useful in the domain of algorithmic composition, since variations comes often not from human input but random variables.
# For example, if we want to generate random [midi notes](sec-midi-notes) but we want to use much more low notes than high ones we could use ``exprand``.
# 
# ```isc
# {exprand(40, 80).floor}!10
# ```
# 
# Another neat function to use is ``nearestInScale`` which transforms a number to the nearest number in a specific scale.
# For exampe, the following code gives us [midi notes](sec-midi-notes) which belong to the [C major scale](sec-diatonic-scale).
# 
# ```isc
# {exprand(36, 59).nearestInScale(Scale.major)}!10
# ```
# 
# We need the brackets to evaluate the function multiple times.
# The following build-in sampling functions can be used, where the receiver ``x`` is a number:
# 
# + ``coin(x)``: returns ``true`` with the probability of ``x`` and ``false`` with the probability ``x-1``.
# + ``rand(x)``: uniformly distributed number from ``0`` up to ``x`` (exclusive).
# + ``rand2(x)``: uniformly distributed number from ``-x`` up to ``x``.
# + ``rrand(a, b)``: a random number in the interval ]``a``, ``b``[.
# + ``linrand(x)``: a linearly distributed random number from zero to ``x``.
# + ``bilinrand(x)``: a bilateral linearly distributed random number from ``-x`` to ``x``.
# + ``sum3rand(x)``: a random number from ``-x`` to ``x`` is the result of summing three uniform random generators to yield a bell-like distribution.
# + ``gauss(x, sigma)``: a gaussian distributed random number with the standard deviation ``sigma``.
# + ``exprand(a, b)``: an exponentially distributed random number in the interval ]``a``, ``b``[.
# 
# The following code generates histograms for some of the random generators.
# 
# ```isc
# (
# ~histogram = {
# 	arg values, steps = 500;
# 	var histogram;
# 	histogram = values.histo(steps: steps).normalizeSum;
# 	histogram;
# };
# 
# ~histogram.( values: {rand(4.0)}!1000000, steps: 100 ).plot(name: "uniform");
# ~histogram.( values: {linrand(4.0)}!1000000, steps: 100 ).plot(name: "linear");
# ~histogram.( values: {bilinrand(4.0)}!1000000, steps: 100 ).plot(name: "bilinear");
# ~histogram.( values: {sum3rand(4.0)}!1000000, steps: 100 ).plot(name: "pseudo gauss");
# ~histogram.( values: {gauss(0.0, standardDeviation: 1.0)}!1000000, steps: 100 ).plot(name: "gauss");
# ~histogram.( values: {exprand(4.0, 0.5)}!1000000, steps: 100 ).plot(name: "exp");
# )
# ```
# 
# ```{figure} ../../../figs/plot-dists.png
# ---
# width: 800px
# name: fig-plot-dists
# ---
# Plot of a histogram of ``rand(x)``, ``linrand(x)``, ``exprand(a, b)``, ``bilinrand(x)``, ``sum3rand(x)``, ``gauss(x, sigma)``.
# ```
# 
# On the **serve-side** there are corresponding unit generators such as
# 
# + ``Rand``,
# + ``LinRand``, and
# + ``ExpRand``.
# 
# 
# ## Example
# 
# In the following example we use frequency for ``\freq``, amplitude for ``\amp`` and semitones for ``\detune``.
# Furthermore, we convert -7 decibals into amplitude and make use of ``k.reciprocal`` which computes ``1/k``.
# 
# The sound is generated by three sine waves at frequency ``\freq``, ``\freq`` + 0.01 semitone and ``\freq`` - 0.01 semintone.
# Since the detuning is very small we can hear the sine wave going in and out of phase.
# 
# ```isc
# (
# SynthDef(\detune_sines, {
#     arg freq=440, detune=0.2, amp = 0.5;
#     var sig, env;
#     sig = SinOsc.ar(freq * [0.0, detune, (-1)*detune].midiratio);
#     sig = sig * amp * 3.reciprocal;
#     sig = Splay.ar(sig);
#     Out.ar(0, sig);	
# }).add;
# )
# 
# Synth(\detune_sines, [\freq, 440, \amp, -7.dbamp, \detune: 0.01]);
# ```

# In[1]:


import IPython.display as ipd
audio_path = '../../../sounds/detune-sines.mp3'
ipd.Audio(audio_path)

