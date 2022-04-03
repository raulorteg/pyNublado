import pathlib

class CloudyInput:
    """ Class used to create model.in file and the file structure given a sample, a 
    combination of parameters that are to be run on CLOUDY.
    
    :param int index: index identifier of the sample within the whole array of samples.
    :param int N: number of total samples.
    :param str target_dir: path of directory where samples are to be saved.
    :param str LineList_path: path to file where lines to be saved are written. 
    """

    def __init__(self, index:int, N:int, target_dir:str, LineList_path:str):

        self.target_dir = target_dir        # directory path where samples are to be saved
        self.index = index                  # index of the sample, identifier for the sample
        self.N = N                          # number of total samples
        self.LineList_path = LineList_path  # path to file containing lines to be saved
        self.buffer_to_write = []           # buffer with the final paths of all model.in files created

    def _set_title(self) -> None:
        command = 'title model'
        self.buffer_to_write.append(command)
    
    def _set_bpass_model(self) -> None:
        """ SEDs from stellar atmosphere """
        command = 'table star "binaries/bpass_v2p2.1_imf_chab300_burst_binary.mod" age={} years Z={}'.format(self.stellar_age, self.stellar_metallicity)
        self.buffer_to_write.append(command)
    
    def _set_gas_density(self) -> None:
        """ hydrogen nucleon density """
        command = 'hden {}'.format(self.log_gas_density)
        self.buffer_to_write.append(command)
    
    def _set_ionization_fraction(self) -> None:
        """ dimensionless ratio of hydrogen-ionizing photon to total-hydrogen
        densities """
        command = 'ionization parameter {}'.format(self.ionization_parameter)
        self.buffer_to_write.append(command)
    
    def _set_abundances(self) -> None:
        """ This will use solar abundances from
        Grevesse et al. (2010). """
        command = 'abundances solar_GASS10 no grains'
        self.buffer_to_write.append(command)
    
    def _set_gas_phase_metallicity_and_grains(self) -> None:
        """ multiplies the abundances of the entire mixture of metals (elements heavier than
        helium) by the scale factor entered on the line. This is useful when the effects of global
        enrichments or depletions of the elements are to be investigated.
        It seems likely that the grain to hydrogen ratio scales with the total gas-phase metallicity."""
        command = 'metals and grains {}'.format(self.gas_phase_metallicity)
        self.buffer_to_write.append(command)

    def _set_dust_depletion_grains(self) -> None:
        """ specifies graphitic and silicate grains with a size distribution and abundance
        appropriate for those along the line of sight to the Trapezium stars in Orion. The Orion size
        distribution is deficient in small particles and so produces the relatively grey extinction
        observed in Orion (Baldwin et al., 1991)"""
        command = 'grains Orion 0.2'
        self.buffer_to_write.append(command)
    
    def _set_polyaromatic_carbon_grains(self) -> None:
        """ PAHs appear to exist mainly at the interface between the H+ region and the molecular clouds.
        Apparently PAHs are destroyed in ionized gas (Sellgren et al., 1990, AGN3 section 8.5) by
        ionizing photons and by collisions with ions (mainly H+ ) and may be depleted into larger grains
        in molecular regions. """
        command = 'grains PAH 0.2'
        self.buffer_to_write.append(command)
    
    def _set_pressure_function(self) -> None:
        """ This holds the total pressure constant. This includes ram, magnetic, turbulent, particle, and
        radiation pressure. """
        command = 'constant pressure'
        self.buffer_to_write.append(command)
    
    def _set_cloud_covering_factor(self) -> None:
        """ Covering factor Ω/4π for the emission-line region. Affects both the luminosity of the emitted spectrum and the radiative
        transfer of lines and continua. If a covering factor is set and the luminosity case used then the
        luminosities will be for a shell covering Ω sr of the central object. """
        command = 'covering factor 1.0'
        self.buffer_to_write.append(command)
    
    def _set_cosmic_rays(self) -> None:
        """ Cosmic rays must be included if the calculation extends into molecular regions. The
        ion-molecule chemistry that occurs in the cold ISM requires a source of ionization (Dyson and
        Williams, 1997). """
        command = 'cosmic rays background'
        self.buffer_to_write.append(command)
    
    def _set_cmb_background(self) -> None:
        """ This specifies a radiation field shape and intensity chosen to mimic the cosmic radio to X-ray
        background (Ostriker and Ikeuchi, 1983, Ikeuchi and Ostriker, 1986, and Vedel et al., 1994)"""
        command = 'background, z={}'.format(self.redshift)
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_visual_extinction(self) -> None:
        """ This stops a calculation at a specified visual extinction AV . The value is the extinction in
        magnitudes at the isophotal wavelength of the V filter (5500Å) """
        command = 'stop AV 100.0'
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_temperature_off(self) -> None:
        """ The calculation will stop when the kinetic temperature drops below Tlow , the argument of this
        command. The default value is Tlow = 4000 K """
        command = 'stop temperature off'
        self.buffer_to_write.append(command)
    
    def _set_max_number_of_zones(self) -> None:
        command = 'set nend 2000'
        self.buffer_to_write.append(command)
    
    def _set_iteration_options(self) -> None:
        command = 'iterate to convergence max=3'
        self.buffer_to_write.append(command)
    
    def _set_print_all_lines(self) -> None:
        command = 'print line faint _off'
        self.buffer_to_write.append(command)
    
    def _set_print_only_last_iteration(self) -> None:
        command = 'print last iteration'
        self.buffer_to_write.append(command)
    
    def _set_prefix_for_savefiles(self) -> None:

        # create the folder structure if it doesnt exist
        pathlib.Path(f'{self.target_dir}sample_N{self.N}/{self.index}').mkdir(parents=True, exist_ok=True)
        command = 'set save prefix model'
        self.buffer_to_write.append(command)
    
    def _set_save_lines(self) -> None:
        command = 'save last line labels ".label"'
        self.buffer_to_write.append(command)
    
    def _set_save_continuum(self) -> None:
        command = 'save last continuum ".cont"'
        self.buffer_to_write.append(command)
    
    def _set_save_overview(self) -> None:
        command = 'save last overview ".ovr"'
        self.buffer_to_write.append(command)
    
    def _set_save_heating(self) -> None:
        command = 'save last heating ".heat"'
        self.buffer_to_write.append(command)
    
    def _set_save_cooling(self) -> None:
        command = 'save last cooling ".cool"'
        self.buffer_to_write.append(command)
    
    def _set_save_optical_depth(self) -> None:
        command = 'save last optical depth ".opd"'
        self.buffer_to_write.append(command)
    
    def _set_save_emissivity(self) -> None:
        command = 'save last lines emissivity ".emis"'
        self.buffer_to_write.append(command)
    
    def _set_lines_to_save(self) -> None:
        with open(self.LineList_path, "r") as f:
            lines = f.readlines()
        assert len(lines) <= 100, f"Line Labels list ({self.LineList_path}) can't include more than 100 lines as per CLOUDY. ({len(lines)}>100)"
        for line in lines:
            self.buffer_to_write.append(line.replace("\n", ""))
        command = 'end of lines'
        self.buffer_to_write.append(command)
    
    def _create(self) -> None:
        """ Provate method wraps the creation of the model.in file list of commands
        using all the _set_***() methods and finally writes the commands into a model.in file"""

        # create the buffer containing all commands
        self._set_title()
        self._set_bpass_model()
        self._set_gas_density()
        self._set_ionization_fraction()
        self._set_abundances()
        self._set_gas_phase_metallicity_and_grains()
        self._set_dust_depletion_grains()
        self._set_polyaromatic_carbon_grains()
        self._set_pressure_function()
        self._set_cloud_covering_factor()
        self._set_cosmic_rays()
        self._set_cmb_background()
        self._set_stop_criteria_visual_extinction()
        self._set_stop_criteria_temperature_off()
        self._set_max_number_of_zones()
        self._set_iteration_options()
        self._set_print_all_lines()
        self._set_print_only_last_iteration()
        self._set_prefix_for_savefiles()
        self._set_save_lines()
        self._set_save_continuum()
        self._set_save_overview()
        self._set_save_heating()
        self._set_save_cooling()
        self._set_save_optical_depth()
        self._set_save_emissivity()
        self._set_lines_to_save()

        # write all commands from the buffer into the model.in file
        self.in_file = f'{self.target_dir}sample_N{self.N}/{self.index}/'+"model.in"
        with open(self.in_file, "w+") as f:
            for command in self.buffer_to_write:
                print(command, file=f)

    def create(self, log_gas_density:float,
                    gas_phase_metallicity:float,
                    redshift:float,
                    ionization_parameter:float,
                    stellar_metallicity:float,
                    stellar_age:float) -> str:
        """
        Main method of the class, called to produce the model.in file using the 
        parameters in the sample. Returns the path to the model.in file created so the
        location is known and it can be found and run with ease.

        :param float log_gas_density: value logarithm of the gas density
        :param float gas_phase_metallicity: value log of the gas metallicity
        :param float redshift: value of the redshift
        :param float ionization_parameter: value log of the ionization parameter
        :param float stellar_metallicity: value log of the stellar metallicity
        :param float stellar_age: value stellar age in years
        :return: path to the model.in file created
        :rtype: str
        """
        
        # set the input variables as attributes
        self.log_gas_density = log_gas_density
        self.gas_phase_metallicity = gas_phase_metallicity
        self.redshift = redshift
        self.ionization_parameter = ionization_parameter
        self.stellar_age = stellar_age
        self.stellar_metallicity = stellar_metallicity

        # create the list of commands and write them into a .in file
        self._create()

        # return the path to the model.in file created
        return self.in_file