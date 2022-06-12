# sleep_volume_timer
A simple python script controlling speaker volume during sleep. 

The script changes from a max to a min volume of a set amount of time (depending on how "late" it is). The volume resets back to max volume after the user clicks the mouse. By default the script is configured to go from a max to a min volume faster and faster after each reset the later it is.

# usage

NOTE: Use reasonable volume values to avoid hurting your ears. A minimum volume of 0 is reasonable if you want the volume to fade out entirely. The max volumes depend on your headphone/speaker setup. I used a value of 0.07 (%7) max volume which was reasonably quiet for bedtime.

Configure the volume settings in sleep_volume_timer.py:

`EARLY_MAX_VOLUME`: Early max volume (0-1)

`LATE_MAX_VOLUME`: Late max volume (0-1)

`EARLY_MIN_VOLUME`: Early min volume (0-1)

`LATE_MIN_VOLUME`: Late min volume (0-1)

`EARLY_TO_LATE_SECONDS`: Early to late seconds

`EARLY_MAX_TO_MIN_SECONDS`: Early max to min volume duration in seconds

`LATE_MAX_TO_MIN_SECONDS`: Late max to min volume duration in seconds

