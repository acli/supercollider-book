# Simpler Filters

A signal can also be filtered by smoothening it.
For example, let $\text{in}[0], \ldots, \text{in}[n]$ be the discrete (input) signal of a [sawtooth waves](sec-sawtooth-wave) and $\text{out}[0], \ldots \text{out}[n]$ be the filtered (output) signal.
If 

\begin{equation}
    \begin{split}
    \text{out}[0] &\leftarrow 0.5 \cdot \text{in}[0]\\
    \text{out}[i] &\leftarrow 0.5 \cdot \text{in}[i] - 0.5 \cdot \text{in}[i-1]
    \end{split}
\end{equation}

the result is the difference quotient divided by sample rate.
All values of $\text{out}$ are almost zero except at the parts which are not differentiable.

To achieve this effect we can use the [OneZero](sec-onezero)-filter.

```isc
{[LFSaw.ar(10), OneZero.ar(LFSaw.ar(10), -0.5)]}.plot(2/10)
```

```{figure} ../../../figs/sounddesign/filters/canceled-saw-onezero-filter.png
---
width: 600px
name: fig-canceled-saw-onezero-filter
---
Canceling a sawtooth wave by applying a ``OneZero``-filter. You can see peaks at values where the sawtooth is not differentiable.
```

This works so well because the rate of change of a sawtooth wave is constant almost everywhere.

The integral of one phase of a sine wave is zero.
Consequently, by averaging the discrete signal to accomplish the respective sum will cancel out the sine wave, i.e., a specific frequency.
[OnePole](sec-onepole) computes an (weighted) average via a feedback cycle resulting in an exponential drop of weights.

(sec-onezero)=
## OneZero

[OneZero](https://doc.sccode.org/Classes/OneZero.html) extends from [Filter](https://doc.sccode.org/Classes/Filter.html) thus it is a filter.
I had a hard time understanding what this filter actually does to its input signal $\text{in}$, since the documentation is very minimal.
But I think I could reverse engineer its behaviour.

The documentation states that a one zero filter implements the formula:

\begin{equation}
\text{out}[i] \leftarrow (1 - |\alpha|) \cdot \text{in}[i] + \alpha \cdot \text{in}[i-1]
\end{equation}

with $-1 \leq \alpha \leq 1$.
$\text{in}[i]$ is actually the $i$-th sample of the discrete input signal.
Therefore, ``OneZero`` as well as ``OnePole`` depend on the sample rate / audio rate!

Let us use $\alpha = -0.5$ and we a differentiator!
Let $y(t)$ be our signal, then we basically compute

\begin{equation}
    \frac{y(t) - y(t - h)}{2}.
\end{equation}

To compute the difference quotient, we have to figure out what $h$ is.
In other words, what is the time between $\text{in}[i]$ and $\text{in}[i-1]$.
The answer is $1/a_\text{rate}$ where $a_\text{rate}$ is the audio rate.

To compute the difference quotient we use the following formula:

\begin{equation}
    \frac{y(t) - y(t - h)}{2} \cdot \frac{2}{h}.
\end{equation}

Using the discrete input signal $\text{in}$ gives us:

\begin{equation}
    \frac{\text{in}[i] - \text{in}[i-1]}{2} \cdot \frac{2}{a_\text{rate}}.
\end{equation}

To test this result, let us compute the cosine using ``SinOsc`` and a ``OneZero``.
Remember

\begin{equation}
    \frac{d\sin(2\pi \cdot f \cdot t)}{dt} = 2 \pi \cdot f \cdot \cos(2\pi \cdot f \cdot t) 
\end{equation}

```isc
({
    var freq = 220;
    var sample_rate = 48000;
    var dt = sample_rate.reciprocal;
    [OneZero.ar(SinOsc.ar(freq), -0.5) * 2 / dt / (2 * pi * freq), SinOsc.ar(freq)]
}.plot(1/220)
)
```

```{figure} ../../../figs/sounddesign/filters/sin_deviation.png
---
width: 400px
name: fig-all-sin_deviation
---
At the top the cosine generated by the bottom signal and a ``OneZero``-``UGen``.
```

````{admonition} Slope UGen
:class: sc
The [Slope](https://doc.sccode.org/Classes/Slope.html)-``UGen`` can also be used to compute the slope of a signal.

```isc
Slope.ar(SinOsc.ar(freq)) / (2 * pi * freq);
```

gives us the cosine.
````

If we use $\alpha = 1.0$ we generate a single sample delay and for -1.0 we additionally mirror the signal at the $x$-axis.

(sec-onepole)=
## OnePole

Another ``UGen`` I have a hard time get my head around is ``OnePole``.
The documentation states that a one pole filter implements the formula:

```{math}
:label: eq:onepole
    \text{out}[i] \leftarrow (1 - |\alpha|) \cdot \text{in}[i] + \alpha \cdot \text{out}[i-1]
```

with $-1 \leq \alpha \leq 1$.
I assume 

\begin{equation}
\text{out}[0] \leftarrow (1 - |\alpha|) \cdot \text{in}[0]
\end{equation}

holds. $\text{out}$ is the resulting signal and $\text{in}$ the input signal of ``OnePole``.
Let us assume $1 \geq \alpha \geq 0$, then we can rearrange Eq. {eq}`eq:onepole`:

```{math}
:label: eq:onepole2
    \text{out}[i] \leftarrow \text{in}[i] + \alpha \cdot (\text{out}[i-1] - \text{in}[i])
```

or 

```{math}
:label: eq:onepole3
    \text{out}[i] \leftarrow \text{out}[i-1] + \beta \cdot (\text{in}[i] - \text{out}[i-1])
```

with $\beta = 1-\alpha$.
If $\beta$ is small, ($\alpha$ is large respectively), then output samples $\text{out}[0], \ldots \text{out}[n]$ respond more slowly to a change in the input samples $\text{in}[0], \ldots \text{in}[n]$. For example,

\begin{equation}
\begin{split}
\text{out}[2] & \leftarrow \text{out}[1] + \beta \cdot (\text{in}[2] - \text{out}[1]) \\
  & = \text{in}[2] \cdot \beta + \text{in}[1] \cdot (\beta - \beta^2) + \text{in}[0] \cdot (\beta - 2\beta^2 + \beta^3)\\
  & = \beta \cdot (\text{in}[2] + \text{in}[1] \cdot (1 - \beta) + \text{in}[0] \cdot (1 - \beta)^2) \\
  & = (1-\alpha) \cdot (\text{in}[2] + \text{in}[1] \cdot \alpha + \text{in}[0] \cdot \alpha^2)
\end{split}
\end{equation}

and in general we get

\begin{equation}
\begin{split}
\text{out}[i] \leftarrow (1-\alpha) \cdot \sum\limits_{k=0}^{i} \alpha^{i-k} \cdot \text{in}[k].
\end{split}
\end{equation}

The change from one filter output to the next is proportional to the difference between the previous output and the next input.
Therefore, the signal is smoothen exponentially, which matches the exponential decay seen in the continuous-time system.
The exponential decay is depicted in {numref}`Fig. {number} <fig-lag-and-onepole>`.

```{admonition} OnePole
:name: remark-one-pole-lowpass
:class: remark
``OnePole`` is a [lowpass filter](sec-lowpass-filter).
```

Compare. for example, the following similar sounding signals of a [sawtooth wave](sec-sawtooth-wave), first filtered by the low-pass filter ``LPF`` and then filtered by ``OnePole`` using a large $\alpha$:

```isc
{LPF.ar(Saw.ar(440), 400) * 0.25;}.play
{OnePole.ar(Saw.ar(440), coef: 0.98) * 0.25;}.play
```

``OnePole`` simulates a simple (analog/electrical) RC-filter (resistance, capacity).
In the [Wikipedia article](https://en.wikipedia.org/wiki/Low-pass_filter) about low-pass filters, you can find some additional explanations regarding the relationship between the continuous electrical and discrete digital filter.