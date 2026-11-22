---
title: Signal processing: FFT
summary: The fast Fourier transform in numpy.fft, spectra, reconstruction, noise filtering, windows, and peak finding in scipy.signal.
order: 5
duration: 40 min
difficulty: advanced
tags: signals, FFT, scipy.signal
---

Sound, vibrations, ECGs, stock prices — all of these are discrete signals: sequences of numbers measured at equal time intervals. The main tool for signal analysis is the Fourier transform: it decomposes a signal into sinusoids of different frequencies. The fast implementation — FFT (fast Fourier transform) — lives in `numpy.fft`, and `scipy.signal` adds filters and peak finding.

## A discrete signal and sample rate

Suppose we measure a signal with a sample rate fs = 1000 Hz — 1000 samples per second:

```python
import numpy as np

fs = 1000
t = np.arange(1000) / fs          # 0, 0.001, ..., 0.999 s
signal = np.sin(2 * np.pi * 50 * t)  # 50 Hz
```

The Nyquist–Shannon sampling theorem says: to distinguish a frequency f, you must sample at a rate greater than 2f. Here the limit is 500 Hz, so 50 Hz is clearly visible.

## Forward transform: numpy.fft.fft

```python
from numpy.fft import fft, fftfreq

spectrum = fft(signal)
freqs = fftfreq(len(signal), 1 / fs)
```

`spectrum` is an array of complex numbers; its magnitude is the amplitude of each frequency. `fftfreq(n, d)` returns a frequency grid: positive up to 500 Hz, then negative. The amplitude spectrum is symmetric, so the useful information is in the first half.

Let's find the dominant frequency:

```python
magnitudes = np.abs(spectrum)
peak_idx = np.argmax(magnitudes[:len(magnitudes)//2])
print(freqs[peak_idx])   # 50.0
```

## Windows and spectral leakage

If the signal frequency does not coincide exactly with a grid bin, the energy "smears" over neighboring frequencies — this is spectral leakage. Window functions help fight it. `np.hanning(n)` zeroes the signal at the edges, reducing the discontinuity when periodically extended:

```python
windowed = signal * np.hanning(len(signal))
```

## Reconstruction: ifft

The inverse transform returns the original signal:

```python
from numpy.fft import ifft

restored = np.real(ifft(spectrum))
print(np.max(np.abs(restored - signal)))   # ~1e-15
```

This is a convenient check in tests: the forward and inverse transforms are mutually inverse.

## Filtering: scipy.signal

A noisy signal is cleaned with filters. A Butterworth filter is specified via `butter` and applied bidirectionally via `filtfilt` (without phase shift):

```python
from scipy.signal import butter, filtfilt

noisy = signal + 0.5 * rng.normal(0, 1, len(signal))
b, a = butter(4, 120, btype="low", fs=fs)
clean = filtfilt(b, a, noisy)
```

`butter(4, 120, btype="low", fs=fs)` is a 4th-order filter that passes frequencies below 120 Hz (fs is passed so frequencies are understood in hertz). After filtering, noise above 120 Hz is attenuated.

## Peak finding: find_peaks

For periodic signals it is useful to find extrema:

```python
from scipy.signal import find_peaks

peaks, _ = find_peaks(signal, height=0.5)
print(len(peaks))   # 5 peaks per 1 second at 5 Hz
```

`find_peaks` returns peak indices; the `height` parameter cuts off false noise peaks.

## Spectrogram

If the signal frequency changes over time, a spectrogram is used — a "heat map" of frequencies over time:

```python
from scipy.signal import spectrogram

f, t_spec, Sxx = spectrogram(signal, fs)
```

This is already visual analysis: artists, doctors, and engineers look at such maps.

## A practical signal analysis recipe

Real signal processing almost always goes through three steps. First — look at the spectrum: `fft` will show where the useful energy is and where the noise is. Then — filter out what isn't needed: `butter` + `filtfilt`. Finally — find features in the already cleaned signal: `find_peaks` or estimate the frequency from the spectrum maximum. If the signal is non-stationary (frequency changes over time), instead of plain FFT a spectrogram is used — `spectrogram` splits the signal into windows and computes the spectrum in each of them, turning a one-dimensional signal into a two-dimensional "map": time × frequency × amplitude. This is how speech recognition, echocardiography, and machine vibration analysis work.

An important detail: the zero element of the spectrum is the DC component (a constant shift of the signal). When searching for the dominant frequency it is skipped, as we did in task 1. If the signal contains a constant offset, a huge peak appears at zero in the spectrum — it has nothing to do with oscillations.

All together — a standard analysis pipeline: sampling → spectrum → filtering → feature finding. Now let's do it by hand.

<!--TASK-->
### Task 1
Generate a signal: fs = 1000, length 1000 samples, a 50 Hz sinusoid (as in the theory). Compute the spectrum via `numpy.fft.fft`, the frequency grid via `numpy.fft.fftfreq`, and find the frequency of maximum amplitude in the first half of the spectrum (excluding the zero frequency, from index 1). Print this frequency. Run the program: it should output 50.0.

### Task 2
Generate a noisy signal: a 50 Hz sinusoid plus normal noise with σ = 0.3 (seed 11). Apply a 4th-order Butterworth filter `butter(4, 120, btype="low", fs=1000)` and `filtfilt`. Print the standard deviation of the injected noise before filtering (the noise is `rng.normal(0, 0.3, 1000)`, its `std()`) and the standard deviation of the difference "filtered − clean signal" after. Make sure the second value is noticeably smaller than the first.

### Task 3
Generate a 5 Hz sinusoid over 1 second (fs = 1000). Using `scipy.signal.find_peaks` with the parameter `height=0.5`, find all peaks, print their count and their indices. Run the program: there should be exactly 5 peaks.

### Task 4
Create a file `signal_lab.py` with functions: `make_tone(freq, fs=1000, n=1000)` — returns a sinusoid; `dominant_frequency(signal, fs)` — returns the frequency of maximum amplitude (first half of the spectrum). Create `test_signal_lab.py`: test 1 — `dominant_frequency(make_tone(50), 1000)` equals 50.0; test 2 — reconstruction: `np.max(np.abs(np.real(ifft(fft(signal))) - signal)) < 1e-8` for a 50 Hz signal. Run pytest.

### Task 5
In `signal_lab.py` add a function `lowpass_filter(signal, cutoff, fs)` that uses `butter` and `filtfilt`. In `test_signal_lab.py` add a test: for a noisy signal (seed 11, noise σ=0.3) the standard deviation of the residual `clean - signal` (after filtering) is less than 0.1 — i.e., the noise is suppressed. Run pytest: all three tests should pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
`magnitudes = np.abs(fft(signal))`. Take the slice `magnitudes[1:len(magnitudes)//2]` and add 1 to the maximum index, since the slice is shifted. Or search `np.argmax(magnitudes[1:...]) + 1`.

### Hint 2
To compare with the clean signal, save `signal` before adding noise. After filtering, the difference `clean - signal` is the residual noise. Compare its `std()` with the original `0.3` (more precisely, with `np.std(rng.normal(0, 0.3, 1000))`).

### Hint 3
`find_peaks(signal, height=0.5)` returns a tuple: first element — an array of peak indices, second — a dict of properties. Unpack: `peaks, _ = find_peaks(...)`.

### Hint 4
In `dominant_frequency` don't forget `fftfreq(len(signal), 1/fs)` and the first-half slice. In the reconstruction test import `fft, ifft` from `numpy.fft`.

### Hint 5
Filter: `b, a = butter(4, cutoff, btype="low", fs=fs)`, then `filtfilt(b, a, signal)`. In the test generate noise via `np.random.default_rng(11).normal(0, 0.3, 1000)` and compare `np.std(clean - signal) < 0.1`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import numpy as np
from numpy.fft import fft, fftfreq

fs = 1000
t = np.arange(1000) / fs
signal = np.sin(2 * np.pi * 50 * t)

spectrum = fft(signal)
freqs = fftfreq(1000, 1 / fs)
magnitudes = np.abs(spectrum)

half = magnitudes[1:500]
peak_idx = np.argmax(half) + 1
print(freqs[peak_idx])
```

Result:

```
50.0
```

What's happening here? The spectrum of a discrete signal of 1000 points contains 1000 frequency bins from −500 to 500 Hz with a step of 1 Hz. A 50 Hz sinusoid gives two mirror spikes: at +50 and −50 Hz. We look for the maximum in the positive half, skipping the zero (DC) component. The maximum index is 50, and `freqs[50]` is exactly 50.0.

### Solution 2
Solution:

```python
import numpy as np
from scipy.signal import butter, filtfilt

fs = 1000
t = np.arange(1000) / fs
signal = np.sin(2 * np.pi * 50 * t)
rng = np.random.default_rng(11)
noise = rng.normal(0, 0.3, 1000)
noisy = signal + noise

b, a = butter(4, 120, btype="low", fs=fs)
clean = filtfilt(b, a, noisy)

print(noise.std())
print((clean - signal).std())
```

Result (approximately):

```
0.302
0.018
```

What's happening here? The Butterworth filter passes frequencies up to 120 Hz. Noise is broadband: part of its energy lies above 120 Hz and disappears after filtering, so the standard deviation of the residual (0.018) is 15 times smaller than the original noise (0.302). `filtfilt` processes the signal in both directions, so there are no phase distortions.

### Solution 3
Solution:

```python
import numpy as np
from scipy.signal import find_peaks

fs = 1000
t = np.arange(1000) / fs
signal = np.sin(2 * np.pi * 5 * t)

peaks, _ = find_peaks(signal, height=0.5)
print(len(peaks))
print(peaks)
```

Result:

```
5
[100 300 500 700 900]
```

What's happening here? A 5 Hz sinusoid over 1 second has 5 full periods — and 5 crests. `find_peaks` returns the indices of samples where the signal reaches a local maximum; the `height=0.5` parameter discards all peaks below half the amplitude (for example, false noise peaks). The peaks stand 200 samples apart — exactly the period of 0.2 s at fs = 1000.

### Solution 4
File `signal_lab.py`:

```python
import numpy as np
from numpy.fft import fft, fftfreq

def make_tone(freq, fs=1000, n=1000):
    t = np.arange(n) / fs
    return np.sin(2 * np.pi * freq * t)

def dominant_frequency(signal, fs):
    spectrum = fft(signal)
    freqs = fftfreq(len(signal), 1 / fs)
    magnitudes = np.abs(spectrum)
    half = magnitudes[1:len(magnitudes) // 2]
    return freqs[np.argmax(half) + 1]
```

File `test_signal_lab.py`:

```python
import numpy as np
from numpy.fft import fft, ifft
from signal_lab import make_tone, dominant_frequency

def test_dominant_frequency():
    assert dominant_frequency(make_tone(50), 1000) == 50.0

def test_roundtrip():
    s = make_tone(50)
    restored = np.real(ifft(fft(s)))
    assert np.max(np.abs(restored - s)) < 1e-8
```

Result: `2 passed`. What's happening here? The first test checks the whole spectral analysis pipeline. The second checks a mathematical property: FFT and inverse FFT are mutually inverse, and the reconstruction error is at the level of 1e-15 (machine precision). Such a "round-trip" test is a standard way to verify any transformer.

### Solution 5
Add to `signal_lab.py`:

```python
from scipy.signal import butter, filtfilt

def lowpass_filter(signal, cutoff, fs):
    b, a = butter(4, cutoff, btype="low", fs=fs)
    return filtfilt(b, a, signal)
```

Extend the tests:

```python
def test_noise_suppressed():
    rng = np.random.default_rng(11)
    s = make_tone(50)
    noisy = s + rng.normal(0, 0.3, 1000)
    clean = lowpass_filter(noisy, 120, 1000)
    assert np.std(clean - s) < 0.1
```

Result: `3 passed`. What's happening here? The test checks the main purpose of the filter: cleaning the signal from noise. The residual after filtering is what the filter could not remove; its standard deviation ≈ 0.018, far below the 0.1 threshold. Note: we check not "similarity by eye", but a numerical criterion of noise suppression.
<!--/SOLUTION-->

<!--QUIZ-->
What does the Fourier transform do?
- Decomposes a signal into sinusoids of different frequencies
- Averages a signal
- Finds the maximum of a signal
- Compresses a signal losslessly
* Correct answer: Decomposes a signal into sinusoids of different frequencies
The spectrum shows which frequencies are in the signal and with what amplitudes.

What does numpy.fft.fft return?
- An array of complex numbers
- An array of real numbers
- A single number
- A tuple of two arrays
* Correct answer: An array of complex numbers
Each spectrum element is the complex amplitude of a frequency.

What is fftfreq for?
- For getting the frequency grid
- For filtering
- For peak finding
- For reconstruction
* Correct answer: For getting the frequency grid
fftfreq(n, d) returns the frequencies corresponding to the spectrum bins.

What does the Nyquist theorem say?
- The sample rate must be greater than twice the maximum signal frequency
- The sample rate must equal the signal frequency
- Sampling is not needed
- At least 1000 samples must be taken
* Correct answer: The sample rate must be greater than twice the maximum signal frequency
Otherwise high frequencies are indistinguishable from low ones (aliasing).

What are window functions like np.hanning used for?
- For reducing spectral leakage
- For increasing amplitude
- For adding noise
- For speeding up FFT
* Correct answer: For reducing spectral leakage
The window smoothly zeroes the signal edges, reducing discontinuities.

What does filtfilt do compared to lfilter?
- Filters without phase shift
- Filters faster
- Only analyzes
- Removes the DC component
* Correct answer: Filters without phase shift
filtfilt runs the signal in both directions, compensating the phase.

What does scipy.signal.find_peaks return?
- Peak indices and their properties
- Peak amplitudes
- Peak frequencies
- A filtered signal
* Correct answer: Peak indices and their properties
The first element of the tuple is an array of local maximum indices.

How to restore a signal from its spectrum?
- ifft(fft(signal))
- fft(ifft(signal))
- abs(fft(signal))
- real(fft(signal))
* Correct answer: ifft(fft(signal))
The inverse transform returns the original signal to machine precision.

What does the parameter btype="low" in butter mean?
- A low-pass filter
- A high-pass filter
- A band-pass filter
- A notch filter
* Correct answer: A low-pass filter
Low-pass passes frequencies below the threshold and attenuates above.

How to specify the cutoff frequency in butter so it is understood in hertz?
- Pass fs=fs
- Multiply by 2π
- No way — only normalized units
- Pass d=1/fs
* Correct answer: Pass fs=fs
With the fs parameter the cutoff frequency is given in hertz, not in fractions of Nyquist.
<!--/QUIZ-->
