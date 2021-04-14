"""
PS2000a Demo.

By: Marko Manninen, based on Colin O'Flynn and Mark Harfouche's software.

This is a demo of how to use AWG with the PicoScope 2405a USB2.0 version.

Connect AWG (Arbitrary Wave Generator) to the channel A with a probe as 
shown in the PicoScope user manual.

"""

import time
from picoscope import ps2000a
import pylab as plt
import numpy as np

if __name__ == "__main__":

    print("Attempting to open PicoScope 2000a models...")

    ps = ps2000a.PS2000a()

    print("Found the following picoscope:")
    print(ps.getAllUnitInfo())

    waveform_desired_duration = 50E-6
    obs_duration = 3 * waveform_desired_duration
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = ps.setSamplingInterval(sampling_interval, obs_duration)

    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    # the setChannel command will chose the next largest amplitude
    channelRange = ps.setChannel('A', 'DC', 2.0, 0.0, enabled=True, BWLimited=False)

    print("Chosen channel range = %d" % channelRange)

    ps.setSimpleTrigger('A', 1.0, 'Falling', timeout_ms=100, enabled=True)
    ps.setSigGenBuiltInSimple(offsetVoltage=0, pkToPk=1.2, waveType="Sine", frequency=50E3)
    ps.runBlock()
    ps.waitReady()

    print("Waiting for AWG to settle.")

    time.sleep(2.0)

    ps.runBlock()
    ps.waitReady()

    print("Done waiting for trigger.")

    dataA = ps.getDataV('A', nSamples, returnOverflow=False)

    dataTimeAxis = np.arange(nSamples) * actualSamplingInterval

    ps.stop()
    ps.close()

    plt.figure()
    plt.plot(dataTimeAxis, dataA, label="Clock")
    plt.grid(True, which='major')
    plt.title("Waveforms from PicoScope")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Time (ms)")
    plt.legend()
    plt.show()
