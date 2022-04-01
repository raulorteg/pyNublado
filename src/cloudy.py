import subprocess
import pathlib

class CloudyInput:
    def __init__(self, title:str, LineList_path:str):
        self.title = title
        self.LineList_path = LineList_path
        self.buffer_to_write = []

    def _set_title(self):
        command = 'title {}'.format(self.title)
        self.buffer_to_write.append(command)
    
    def _set_bpass_model(self):
        command = 'table star "BPASSv2p1_imf135all_100_burst_binary.mod" age={} years Z={}'.format(self.age, self.metallicity)
        self.buffer_to_write.append(command)
    
    def _set_gas_density(self):
        command = 'hden {}'.format(self.log_gas_density)
        self.buffer_to_write.append(command)
    
    def _set_ionization_fraction(self):
        command = 'ionization parameter -4.0'
        self.buffer_to_write.append(command)
    
    def _set_abundances(self):
        command = 'abundances solar_GASS10 no grains'
        self.buffer_to_write.append(command)
    
    def _set_dust_depletion_grains(self):
        command = 'grains Orion 0.2'
        self.buffer_to_write.append(command)
    
    def _set_polyaromatic_carbon_grains(self):
        command = 'grains PAH 0.2'
        self.buffer_to_write.append(command)
    
    def _set_pressure_function(self):
        command = 'constant pressure'
        self.buffer_to_write.append(command)
    
    def _set_cloud_covering_factor(self):
        command = 'covering factor 1.0'
        self.buffer_to_write.append(command)
    
    def _set_cosmic_rays(self):
        command = 'cosmic rays background'
        self.buffer_to_write.append(command)
    
    def _set_cmd_background(self):
        command = 'background, z={}'.format(self.redshift)
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_visual_extinction(self):
        command = 'stop AV 100.0'
        self.buffer_to_write.append(command)
    
    def _set_stop_criteria_temperature_off(self):
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
        pathlib.Path('../out_models').mkdir(parents=True, exist_ok=True)
        pathlib.Path('../in_models').mkdir(parents=True, exist_ok=True) 
        title = '../out_models/'+self.title
        command = 'set save prefix "{}"'.format(title)
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
        self._set_dust_depletion_grains()
        self._set_polyaromatic_carbon_grains()
        self._set_pressure_function()
        self._set_cloud_covering_factor()
        self._set_cosmic_rays()
        self._set_cmd_background()
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

        with open('../in_models/'+self.title+".in", "w+") as f:
            for command in self.buffer_to_write:
                print(command, file=f)

    def create(self, log_gas_density:float,
                    gas_phase_metallicity:float,
                    redshift:float,
                    age:float,
                    metallicity:float):
        
        # set the input variables as attributes
        self.log_gas_density = log_gas_density
        self.gas_phase_metallicity = gas_phase_metallicity
        self.redshift = redshift
        self.age = age
        self.metallicity = metallicity

        # create the list of commands and write them into a .in file
        self._create()

if __name__ == "__main__":
    # example usage

    CloudyInput(title="foo", LineList_path="../data/LineList_in.dat").create(log_gas_density=1.0,
                                                                                gas_phase_metallicity=-1.8,
                                                                                redshift=6.0,
                                                                                age=2e8,
                                                                                metallicity=-1.8)