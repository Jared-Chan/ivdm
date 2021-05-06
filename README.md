# IVDM -- 4-Dimensional Music

We listen to music in one order -- from start to finish. This program makes music that at any moment, you can hear parts of a song, from the beginning to the end, all at once. IVDM lets you enjoy music not sequentially but as a whole. The music created can be looped seamlessly, making a cycle where the beginning and end can be anywhere. A 4-minute song is no longer 4-minute, but it is at the same time always 4-minute.

## Requirements
- `librosa`
- `soundfile`
- `numpy`
- `scipy`


## How it works

IVDM analyses the tempo of a piece of music and divides it into segments spanning a specified number of beats. These segments each repeated to the length of the original piece of music. The volume of each repetition is adjusted so that it is loudest at the time that segment originally comes from. Finally, all these looped segments are combined and the 4-Dimensional song is made.

Example using Rhapsody in Blue by George Gershwin:
![Spectrogram example](./examples/rhapody_in_blue_spectrogram.png)
