from rti_python.Utilities.check_binary_file import RtiCheckFile
from rti_python.Utilities.config import RtiConfig
from rti_python_plot.matplotlib.display_ens import DisplayEnsembles
from rti_python_plot.bokeh.rti_bokeh_plot_data import RtiBokehPlotData
from rti_python_plot.bokeh.rti_bokeh_plot_manager import RtiBokehPlotManager
from rti_python_plot.bokeh.rti_bokeh_server import RtiBokehServer
from rti_python_plot.streamlit.streamlit_heatmap import StreamlitHeatmap
from rti_python_plot.streamlit.streamlit_mag_dir_line import StreamlitMagDirLine
import threading

class FileDiag():

    def __init__(self):

        self.rti_config = RtiConfig()
        self.rti_config.init_average_waves_config()
        self.rti_config.init_terminal_config()
        self.rti_config.init_waves_config()
        self.rti_config.init_plot_server_config()

        self.is_screen_data = True
        self.already_got_data = False

        # Bokeh Plot
        #self.plot_manager = RtiBokehPlotManager(self.rti_config)
        #self.plot_manager.start()
        #self.bokeh_server = RtiBokehServer(self.rti_config, self.plot_manager)

        # Matplotlib plot
        #self.display_ens = DisplayEnsembles()

        # StreamLit heatmap plot
        self.heatmap = StreamlitHeatmap()
        self.mag_dir_line = StreamlitMagDirLine()

        # On reprocessing in Streamlit, it will through an error if this
        # is rerun because the browser content is not in the main thread
        rti_check = RtiCheckFile()
        rti_check.ensemble_event += self.ens_handler
        rti_check.select_and_process()

        # Plot heatmap
        self.heatmap.get_plot("mag")
        self.heatmap.get_plot("dir")

        # Plot mag and direction line plot
        self.mag_dir_line.get_bin_selector()
        self.mag_dir_line.get_plot("mag")
        self.mag_dir_line.get_plot("dir")

        #self.display_ens.plot_amp_min_max_avg()


    def ens_handler(self, sender, ens):
        #if ens.IsEnsembleData:
        #    print(str(ens.EnsembleData.EnsembleNumber))

        #self.display_ens.process_ens(ens)
        #self.plot_manager.update_dashboard_ens(ens)

        # Add data to heatmap
        self.heatmap.add_ens(ens)
        self.mag_dir_line.add_ens(ens)



if __name__ == "__main__":
    fd = FileDiag()
