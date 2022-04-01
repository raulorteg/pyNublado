import pathlib

class CloudyInput:
    def __init__(self, index:int, N:int, target_dir:str, LineList_path:str):
        self.title = "model"
        self.target_dir = target_dir
        self.index = index
        self.N = N 
        self.LineList_path = LineList_path
        self.buffer_to_write = []

    def _set_title(self):
        command = 'title {}'.format(self.title)
        self.buffer_to_write.append(command)
    
    def _set_bpass_model(self):
        """ SEDs from stellar atmosphere """
        command = 'table star "binaries/bpass_v2p2.1_imf_chab300_burst_binary.mod" age={} years Z={}'.format(self.stellar_age, self.stellar_metallicity)
        self.buffer_to_write.append(command)
    
    def _set_gas_density(self):
        """ hydrogen nucleon density """
        command = 'hden {}'.format(self.log_gas_density)
        self.buffer_to_write.append(command)
    
    def _set_ionization_fraction(self):
        """ dimensionless ratio of hydrogen-ionizing photon to total-hydrogen
        densities """
        command = 'ionization parameter {}'.format(self.ionization_parameter)
        self.buffer_to_write.append(command)
    
    def _set_abundances(self):
        """ This will use solar abundances from
        Grevesse et al. (2010). """
        command = 'abundances solar_GASS10 no grains'
        self.buffer_to_write.append(command)
    
    def _set_gas_phase_metallicity_and_grains(self):
        """ multiplies the abundances of the entire mixture of metals (elements heavier than
        helium) by the scale factor entered on the line. This is useful when the effects of global
        enrichments or depletions of the elements are to be investigated.
        It seems likely that the grain to hydrogen ratio scales with the total gas-phase metallicity."""
        command = 'metals and grains {}'.format(self.gas_phase_metallicity)
        self.buffer_to_write.append(command)

    def _set_dust_depletion_grains(self):
        """ specifies graphitic and silicate grains with a size distribution and abundance
        appropriate for those along the line of sight to the Trapezium stars in Orion. The Orion size
        distribution is deficient in small particles and so produces the relatively grey extinction
        observed in Orion (Baldwin et al., 1991)"""
        command = 'grains Orion 0.2'
        self.buffer_to_write.append(command)
    
    def _set_polyaromatic_carbon_grains(self):
        """ PAHs appear to exist mainly at the interface between the H+ region and the molecular clouds.
        Apparently PAHs are destroyed in ionized gas (Sellgren et al., 1990, AGN3 section 8.5) by
        ionizing photons and by collisions with ions (mainly H+ ) and may be depleted into larger grains
        in molecular regions. """
        command = 'grains PAH 0.2'
        self.buffer_to_write.append(command)
    
    def _set_pressure_function(self):
        """ This holds the total pressure constant. This includes ram, magnetic, turbulent, particle, and
        radiation pressure. """
        command = 'constant pressure'
        self.buffer_to_write.append(command)
    
    def _set_cloud_covering_factor(self):
        """ Covering factor Ω/4π for the emission-line region. Affects both the luminosity of the emitted spectrum and the radiative
        transfer of lines and continua. If a covering factor is set and the luminosity case used then the
        luminosities will be for a shell covering Ω sr of the central object. """
        command = 'covering factor 1.0'
        self.buffer_to_write.append(command)
    
    def _set_cosmic_rays(self):
        """ Cosmic rays must be included if the calculation extends into molecular regions. The
        ion-molecule chemistry that occurs in the cold ISM requires a source of ionization (Dyson and
        Williams, 1997). """
        command = 'cosmic rays background'
        self.buffer_to_write.append(command)
    
    def _set_cmb_background(self):
        """ This specifies a radiation field shape and intensity chosen to mimic the cosmic radio to X-ray
        background (Ostriker and Ikeuchi, 1983, Ikeuchi and Ostriker, 1986, and Vedel et al., 1994)"""
        command = 'background, z={}'.format(self.redshift)
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_visual_extinction(self):
        """ This stops a calculation at a specified visual extinction AV . The value is the extinction in
        magnitudes at the isophotal wavelength of the V filter (5500Å) """
        command = 'stop AV 100.0'
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_temperature_off(self):
        """ The calculation will stop when the kinetic temperature drops below Tlow , the argument of this
        command. The default value is Tlow = 4000 K """
        command = 'stop temperature off'
        self.buffer_to_write.append(command)
    
    def _set_max_number_of_zones(self):
        command = 'set nend 2000'
        self.buffer_to_write.append(command)
    
    def _set_iteration_options(self):
        command = 'iterate to convergence max=3'
        self.buffer_to_write.append(command)
    
    def _set_print_all_lines(self):
        command = 'print line faint _off'
        self.buffer_to_write.append(command)
    
    def _set_print_only_last_iteration(self):
        command = 'print last iteration'
        self.buffer_to_write.append(command)
    
    def _set_prefix_for_savefiles(self):
        pathlib.Path(f'{self.target_dir}sample_N{self.N}/{self.index}').mkdir(parents=True, exist_ok=True)
        #title = f'{self.target_dir}sample_N{self.N}/{self.index}/'+self.title
        command = 'set save prefix "{}"'.format(self.title) # model
        self.buffer_to_write.append(command)
    
    def _set_save_lines(self):
        command = 'save last line labels ".label"'
        self.buffer_to_write.append(command)
    
    def _set_save_continuum(self):
        command = 'save last continuum ".cont"'
        self.buffer_to_write.append(command)
    
    def _set_save_overview(self):
        command = 'save last overview ".ovr"'
        self.buffer_to_write.append(command)
    
    def _set_save_heating(self):
        command = 'save last heating ".heat"'
        self.buffer_to_write.append(command)
    
    def _set_save_cooling(self):
        command = 'save last cooling ".cool"'
        self.buffer_to_write.append(command)
    
    def _set_save_optical_depth(self):
        command = 'save last optical depth ".opd"'
        self.buffer_to_write.append(command)
    
    def _set_save_emissivity(self):
        command = 'save last lines emissivity ".emis"'
        self.buffer_to_write.append(command)
    
    def _set_lines_to_save(self):
        with open(self.LineList_path, "r") as f:
            lines = f.readlines()
        assert len(lines) <= 100, f"Line Labels list ({self.LineList_path}) can't include more than 100 lines as per CLOUDY. ({len(lines)}>100)"
        for line in lines:
            self.buffer_to_write.append(line.replace("\n", ""))
        command = 'end of lines'
        self.buffer_to_write.append(command)
    
    def _create(self):
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

        self.in_file = f'{self.target_dir}sample_N{self.N}/{self.index}/'+self.title+".in"
        with open(self.in_file, "w+") as f:
            for command in self.buffer_to_write:
                print(command, file=f)

    def create(self, log_gas_density:float,
                    gas_phase_metallicity:float,
                    redshift:float,
                    ionization_parameter:float,
                    stellar_metallicity:float,
                    stellar_age:float):
        
        # set the input variables as attributes
        self.log_gas_density = log_gas_density
        self.gas_phase_metallicity = gas_phase_metallicity
        self.redshift = redshift
        self.ionization_parameter = ionization_parameter
        self.stellar_age = stellar_age
        self.stellar_metallicity = stellar_metallicity

        # create the list of commands and write them into a .in file
        self._create()
        return self.in_file

if __name__ == "__main__":
    # example usage

    ## approach 1 (queue of infiles)
    samples = np.array()
    
    # create all in files
    for sample in samples:
        CloudyInput().create(sample)
    
    # run the in files (multiple cpus)
    for in_file in infiles:
        run(in_file)
