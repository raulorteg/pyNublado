### Using BPASS models
* From the BPASS V2.2.1 [data release](https://bpass.auckland.ac.nz/9.html) download the data for _bpass_v2p2.1_imf_chab300_


_NOTE: the Perl script (in data/) needs to be placed on the parent directory_

```bash
├── BPASSv2.1_bin-imf135_300
│   ├── ...
│   └── ...
├── convert_bpassv2.x.pl
```

* Navigate to the BPASS folder ```cd BPASSv2.1_bin-imf135_300 ```
* Execute the Perl script from the folder
``` ../convert_bpassv2.x.pl```

_NOTE: If it complains about permissions, grant the Perl file permissions_

```bash
chmod +x convert_bpassv2.x.pl
```
* Generate binary files from the resulting _.ascii_ files executing Cloudy
```bash
  ~/c17.03/source/cloudy.exe
```
* Press ```enter```
* Type
```bash 
compile star BPASSv2_imf135_100_burst_binary.ascii" 
```
* Press ```enter``` again to generate the binaries.

The binaries now need to be placed in a special location for Cloudy to use them.

* Navigate to the Cloudy data directory 
```bash
cd ~/c17.03/data
```
* Create a binaries directory 
```bash
  mkdir binaries
```
* Finally, copy the binary BPASS file to the binaries/ directory 
```bash 
cp bpass_v2p2.1_imf_chab300_burst_binary.mod ~/c17.03/data/binaries/
```
