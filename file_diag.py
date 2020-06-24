from rti_python.Utilities.check_binary_file import RtiCheckFile
from rti_python.Utilities.config import RtiConfig
from rti_python_plot.matplotlib.display_ens import DisplayEnsembles

class FileDiag():

    def __init__(self):

        self.rti_config = RtiConfig()
        self.rti_config.init_average_waves_config()
        self.rti_config.init_terminal_config()
        self.rti_config.init_waves_config()
        self.rti_config.init_plot_server_config()

        #self.plot_manager = RtiBokehPlotManager(self.rti_config)
        #self.plot_manager.start()
        #self.bokeh_server = RtiBokehServer(self.rti_config, self.plot_manager)

        self.display_ens = DisplayEnsembles()

        rti_check = RtiCheckFile()
        rti_check.ensemble_event += self.ens_handler
        rti_check.select_and_process()

        #self.display_ens.plot_amp_min_max_avg()

    def ens_handler(self, sender, ens):
        #if ens.IsEnsembleData:
        #    print(str(ens.EnsembleData.EnsembleNumber))

        self.display_ens.process_ens(ens)
        #self.plot_manager.update_dashboard_ens(ens)



if __name__ == "__main__":
    fd = FileDiag()
