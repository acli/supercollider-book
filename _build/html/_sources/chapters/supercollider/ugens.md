(sec-ugens)=
# Unit Generators

The server **scsynth** executes so called ``UGens`` (Unit Generators) for analysis, synthesis, and processing of audio ``ar`` and control signals ``kr``.

```{admonition} UGen
:name: def-ugen
A ``UGen`` represent calculations with a signal.

```

## Amplitude

In the description of the ``UGen`` called ``Amplitude`` we find the following statement:

>Tracks the peak amplitude of a signal.

I had a hard time to understand whats going on here, especially how one should deal with the arguments ``attackTime`` and ``releaseTime``.
Why this ``UGen`` is even helpful?
Isn't the amplitude of a signal $y(t)$ defined by $|y(t)|$?

Well THE amplitude is not defined instead we are dealing with different kinds of amplitudes.
For example, we say that the following signal 

```isc
(
{
	var freg = 400;
	var attackTime = 0.1;
	var releaseTime = 0.2;
	var env = EnvGen.ar(Env.perc(attackTime: attackTime, releaseTime: releaseTime));
	var sig = SinOsc.ar(freg) * env;
	sig
}.plot(0.4);
)
```

has an amplitude of ``1.0``.

```{figure} ../../figs/supercollider/amplitude/amplitude-sine.png
---
width: 200px
name: fig-amplitude-sine
---
A modulated amplitude of a sine wave. We say that this signal has an amplitude of 1.0.
```