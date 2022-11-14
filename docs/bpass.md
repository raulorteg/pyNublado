## Setting up BPASS models
We are using the stellar models of the BPASS V2.2.1 [data release](https://bpass.auckland.ac.nz/9.html)

There are two ways to install the BPASS models

1. Run the installation script ``setup_bpass.py``
```bash
  python3 setup_bpass.py
```

2. Do it manually, as shown below:

* From the BPASS V2.2.1 [data release](https://bpass.auckland.ac.nz/9.html) download the archive 
  _bpass_v2.2.1_imf_chab300.tar.gz_, either from the Google Drive or the Sharepoint page. 
  Should you prefer a different stellar model, please adjust the steps accordingly.

* Unpack the archive and place the Perl script that is located in `data/BPASS/convert_bpassv2.x.pl` 
  within the same directory as the extracted files. Alternatively, extract the BPASS archive files directly into
  `data/BPASS`.
  
* Navigate to the directory containing the script and the archive files and execute the script. 
```bash
 ./convert_bpassv2.x.pl
```
_NOTE: If the script complains about file permissions, grant the Perl file permissions to be executable_

```bash
chmod +x convert_bpassv2.x.pl
```
Then run the script. Once run successfully, the script should produce files with the _.ascii_ suffix.

* In order to generate a binary file from the resulting _.ascii_ file, the desired model file needs to 
  be moved into the `data` directory of the Cloudy installation. Here, we choose the binary model:

```bash
  mkdir ~/c17.03/data/binaries/
  cp BPASS_burst_binary.ascii  ~/c17.03/data/binaries/bpass_v2p2.1_imf_chab300_burst_binary.ascii
```  
* Generating binary mod files can be achieved by executing Cloudy from the Cloudy data directory

```bash
  cd ~/c17.03/data/
  ~/c17.03/source/cloudy.exe
  ```
Press `enter` and then type 

```bash 
  compile star "binaries/bpass_v2p2.1_imf_chab300_burst_binary.ascii"
```
* Press `enter` again (twice in total)  to generate the binaries.

* Your Cloudy data directory should now contain the following file: `binaries/bpass_v2p2.1_imf_chab300_burst_binary.mod`

Additionally, running the test suit should reveal if your BPASS file has been correctly installed.

