import pathlib
from sampling import sampling_create_parameters
from user_settings import STELLAR_MODEL_DIR, STELLAR_MODEL_MOD_FILE

import sys; sys.path.append('..')
from common.abundances import *


class CloudyInput:
    """ Class used to create model.in file and the file structure given a sample, a
    combination of parameters that are to be run on CLOUDY.

    :param int index: index identifier of the sample within the whole array of samples.
    :param int N_sample: number of total models.
    :param str target_dir: path of directory where samples are to be saved.
    :param str LineList_path: path to file where lines to be saved are written.
    """

    def __init__(self, index: int, N_sample: int, target_dir: str, LineList_path: str):

        self.target_dir = target_dir        # directory path where samples are to be saved
        self.index = index                  # index of the sample, identifier for the sample
        self.N = N_sample                   # number of total samples
        self.LineList_path = LineList_path  # path to file containing lines to be saved
        self.buffer_to_write = []           # buffer with the final paths of all model.in files created

    def _set_title(self) -> None:
        command = 'title model'
        self.buffer_to_write.append(command)

    def _set_bpass_model(self) -> None:
        """ SEDs from stellar atmosphere """
        command = 'table star "{}/{}" '.format(STELLAR_MODEL_DIR, STELLAR_MODEL_MOD_FILE)

        # Note that cloudy fails when the stellar age [in Myr] is multiplied by 1e6
        command += 'age={} years Z={}'.format(self.stellar_age, self.stellar_metallicity)
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
        """ This will use solar abundances from abundance.py which uses the Asplund+2009 values"""
        # command = 'abundances solar_GASS10 no grains' # (OLD)
        a_depletion = abundances((10**self.gas_phase_metallicity) * Z_sol, self.DTM)
        command = 'abundances he ='+str(a_depletion['He'])+' '
        ii = 0
        for metal in metals:
            command += ' '+metal.lower()+' ='+str(a_depletion[metal])+' '
            ii += 1
            if ii > 5:
                ii = 0
                command += '\ncontinue   '
        command += ' no grains'
        self.buffer_to_write.append(command)

    def _set_dust_grains(self) -> None:
        """ specifies graphitic and silicate grains with a size distribution and abundance
        appropriate for those along the line of sight to the Trapezium stars in Orion. The Orion size
        distribution is deficient in small particles and so produces the relatively grey extinction
        observed in Orion (Baldwin et al., 1991).
        One problem with the grains approach is metals/element abundances do not talk to the grains command
        and hence there is issues with mass conservation (see cloudy documentation). To alleviate this one
        needs to make the orion grain abundances consistent with the depletion values. Assume 1 per cent of
        C is in PAH's.
        """
        a_nodepletion   = abundances((10**self.gas_phase_metallicity) * Z_sol, 0)
        a_depletion     = abundances((10**self.gas_phase_metallicity) * Z_sol, self.DTM)
        delta_C         = 10**a_nodepletion['C'] - 10**a_depletion['C']
        delta_PAH       = 0.01 * (10**a_nodepletion['C'])
        delta_graphite  = delta_C - delta_PAH
        delta_Si        = 10**a_nodepletion['Si'] - 10**a_depletion['Si']
        if self.DTM>0:
            f_graphite  = delta_graphite/(10**(-3.6259))
            f_Si        = delta_Si/(10**(-4.5547))
            command = F'grains Orion graphite {f_graphite} \ngrains Orion silicate {f_Si}'
            self.buffer_to_write.append(command)
        else:
            f_graphite, f_Si = 0, 0

    def _set_polyaromatic_carbon_grains(self) -> None:
        """ PAHs appear to exist mainly at the interface between the H+ region and the molecular clouds.
        Apparently PAHs are destroyed in ionized gas (Sellgren et al., 1990, AGN3 section 8.5) by
        ionizing photons and by collisions with ions (mainly H+ ) and may be depleted into larger grains
        in molecular regions. Also assume the carbon fraction of PAHs from Abel+2008
        (https://iopscience.iop.org/article/10.1086/591505) assuming 1 percent of Carbon in PAHs. Another
        way is to scale the abundance as a function of the metallicity using the Z_PAH vs Z_gas relation
        from Galliano+2008 (https://iopscience.iop.org/article/10.1086/523621, y = 4.17*Z_gas_sol - 7.085),
        which will again introduce issues on mass conservation."""
        if self.DTM>0:
            a_nodepletion   = abundances((10**self.gas_phase_metallicity) * Z_sol, 0)
            delta_PAH       = 0.01 * (10**a_nodepletion['C'])
            f_pah   = delta_PAH/(10**(-4.446))
            command = F'grains PAH {f_pah}'
            self.buffer_to_write.append(command)

    def _set_pressure_function(self) -> None:
        """ This holds the total pressure constant. This includes ram, magnetic, turbulent, particle, and
        radiation pressure. """
        command = 'constant pressure'
        self.buffer_to_write.append(command)

    def _set_cloud_covering_factor(self) -> None:
        """ Covering factor Ω/4π for the emission-line region. Affects both the luminosity of the emitted spectrum
        and the radiative transfer of lines and continua. If a covering factor is set and the luminosity case used
        then the luminosities will be for a shell covering Ω sr of the central object. """
        command = 'covering factor 1.0'
        self.buffer_to_write.append(command)

    def _set_cosmic_rays(self) -> None:
        """ Cosmic rays must be included if the calculation extends into molecular regions. The documenation
        mentions that the chemistry network will probably collapse if the gas becomes molecular but cosmic rays
        are not present. The ion-molecule chemistry that occurs in the cold ISM requires a source of ionization
        (Dyson and Williams, 1997). This includes galactic background cosmic rays. We adopt the
        Indriolo et al. (2007) mean H0 cosmic ray ionization rate of 2x10-16 s-1 . The H2 secondary ionization
        rate is then 4.6 x 10-16 s-1 ,2 . (Glassgold and Langer (1974) give the relationship between H0 and H2
        ionization rates.). An optional scale factor specifies the cosmic ray ionization rate relative to this
        background value. The scale factor is assumed to be a log unless the keyword linear also appears.
        """
        command = 'cosmic rays background linear {}'.format(self.cosmic_ray_ionization_factor)
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
        pathlib.Path(f'{self.target_dir}/{self.index}').mkdir(parents=True, exist_ok=True)
        command = 'set save prefix "model"'
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
        self._set_dust_grains()
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
        self.in_file = f'{self.target_dir}/{self.index}/'+"model.in"
        with open(self.in_file, "w+") as f:
            for command in self.buffer_to_write:
                print(command, file=f)

    def create(self,
               log_gas_density: float,
               gas_phase_metallicity: float,
               redshift: float,
               cosmic_ray_ionization_factor:float,
               ionization_parameter: float,
               stellar_metallicity: float,
               stellar_age: float,
               DTM: float) -> str:
        """
        Main method of the class, called to produce the model.in file using the
        parameters in the sample. Returns the path to the model.in file created so the
        location is known and it can be found and run with ease.

        :param float log_gas_density: value logarithm of the gas density
        :param float gas_phase_metallicity: value log of the gas metallicity
        :param float redshift: value of the redshift
        :param float cosmic_ray_ionization_factor: value to use to scale the cosmic ray background
        :param float ionization_parameter: value log of the ionization parameter
        :param float stellar_metallicity: value log of the stellar metallicity
        :param float stellar_age: value stellar age in years
        :param float DTM: value dust-to-metal ratio
        :return: path to the model.in file created
        :rtype: str
        """

        # set the input variables as attributes
        self.log_gas_density = log_gas_density
        self.gas_phase_metallicity = gas_phase_metallicity
        self.redshift = redshift
        self.cosmic_ray_ionization_factor = cosmic_ray_ionization_factor
        self.ionization_parameter = ionization_parameter
        self.stellar_age = stellar_age
        self.stellar_metallicity = stellar_metallicity
        self.DTM = DTM

        # create the list of commands and write them into a .in file
        self._create()

        # return the path to the model.in file created
        return self.in_file


def create_inputs(N: int, target_dir: str, LineList_path: str, filter: bool=True, save_to_file: bool=True,
                  plot: bool=False):
    """
    Creates the model.in inputs for CLOUDY and saves them creaing the folder structure.
    Calls the sampling.sampling_create_parameters() to obtain the combinations of parameters,
    then for every combination it creates the model.in file using the template.

    :param int N: number of original (before filtering) different combinations of input parameters.
    :param str target_dir: string path to the directory where the samples are to be saved.
    :param str LineList_path: string path to the file where the list of lines to be saved are listed.
    :param bool filter: Filter out non-physical combinations.
    :param bool save_to_file: Saves the resulting parameters as numpy array.
    :param bool plot: Create a visual representation of the input space.
    :return: None
    :rtype: None
    """
    samples = sampling_create_parameters(path=target_dir,
                                         N_sample=N,
                                         filter=True,
                                         save_to_file=True,
                                         plot=False
                                         )

    for idx, sample in enumerate(samples):
        CloudyInput(index=idx, N_sample=N, target_dir=target_dir, LineList_path=LineList_path).create(*sample)


    #TODO: FK: this is also done in the hpc.py script, so might be obsolete?
