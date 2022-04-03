### Using BPASS models
* From the BPASS V2.2.1 [data release](https://bpass.auckland.ac.nz/9.html) download the data for _bpass_v2p2.1_imf_chab300_


_NOTE: the pearl script (in data/) needs to be placed on the parent directory_

```bash
├── BPASSv2.1_bin-imf135_300
│   ├── ...
│   └── ...
├── convert_bpassv2.x.pl
```

* Navigate to the BPASS folder ```cd BPASSv2.1_bin-imf135_300 ```
* Execute the pearl script from the folder
``` ../convert_bpassv2.x.pl```

_NOTE: If it complains about permissions grant the pearl file permissions_

```bash
chmod +x convert_bpassv2.x.pl
```
* Generate binary files from the resulting _.ascii_ files excuting CLOUDY ```~/c17.02/source/cloudy.exe```
* Press ```enter```
* Type ```compile star BPASSv2_imf135_100_burst_binary.ascii" ```
* Press ```enter``` again to generate the binaries.

The binaries now need to be placed in a special location for CLOUDY to use them.

* Navigate to the CLOUDY data directory ```cd ~/c17.02/data```
* Create a binaries directory ```mkdir binaries```
* Finally copy the binary BPASS file to the binaries/ directory ``` cp bpass_v2p2.1_imf_chab300_burst_binary.mod ~/c17.02/data/binaries/```
