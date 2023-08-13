This repository contains the code used to generate the gravitational wave models here: https://www.thingiverse.com/thing:2886889

I wrote the code back in 2018, this is just a straight dump of the code from back then. No guarantees that it's complete or even works anymore, and I don't remember much of what I did back then.

AFAIK the way it works was
* For events where LIGO published template strain data (e.g. GW150914) take that and scale it to a reasonable magnitude (`process_template_final.ipynb`).
* For events without strain data, generate strains using pycbc `generate_waveform.ipynb`, and process them `process_template_final_generated_waveform.ipynb`
* Use the [Fusion 360](https://www.autodesk.co.uk/products/fusion-360) script in `fusion360_script` to create the 3D model
* Export to STL and print