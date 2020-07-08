from rti_python.Utilities.check_binary_file import RtiCheckFile
from rti_python.Utilities.config import RtiConfig
from rti_python_plot.matplotlib.display_ens import DisplayEnsembles
from rti_python_plot.bokeh.rti_bokeh_plot_data import RtiBokehPlotData
from rti_python_plot.bokeh.rti_bokeh_plot_manager import RtiBokehPlotManager
from rti_python_plot.bokeh.rti_bokeh_server import RtiBokehServer
from rti_python_plot.streamlit.streamlit_heatmap import StreamlitHeatmap
from rti_python_plot.streamlit.streamlit_mag_dir_line import StreamlitMagDirLine
from rti_python_plot.streamlit.Streamlit_power_line import StreamlitPowerLine
from rti_python_plot.streamlit.Streamlit_ancillary_line import StreamlitAncillaryLine
from rti_python.Writer.rti_sqlite_projects import RtiSqliteProjects
import os
import logging
from pathlib import Path, PurePath


# SEt logging level
logging.basicConfig(level=logging.DEBUG)


class FileDiag:

    def __init__(self):

        self.rti_config = RtiConfig()
        self.rti_config.init_average_waves_config()
        self.rti_config.init_terminal_config()
        self.rti_config.init_waves_config()
        self.rti_config.init_plot_server_config()

        self.is_screen_data = True
        self.already_got_data = False
        self.ens_count = 0

        # Bokeh Plot
        #self.plot_manager = RtiBokehPlotManager(self.rti_config)
        #self.plot_manager.start()
        #self.bokeh_server = RtiBokehServer(self.rti_config, self.plot_manager)

        # Matplotlib plot
        #self.display_ens = DisplayEnsembles()

        # Setup the StreamLit Plots
        self.heatmap = StreamlitHeatmap()
        self.mag_dir_line = StreamlitMagDirLine()
        #self.volt_line = StreamlitPowerLine()
        #self.ancillary_line = StreamlitAncillaryLine()

        # On reprocessing in Streamlit, it will through an error if this
        # is rerun because the browser content is not in the main thread
        rti_check = RtiCheckFile()

        # Event handler for ensembles
        rti_check.ensemble_event += self.ens_handler

        # Select a file to process
        file_paths = rti_check.select_files()
        #file_paths = [Path("//Beansack/rico/RTI/Data/cs/nav.com.cn/xiamen202007-/01400000000000000000000000000254_xiamen202007_2.ENS")]
        logging.debug(file_paths)

        # Get the folder path from the first file path
        folder_path = PurePath(file_paths[0]).parent
        prj_name = Path(file_paths[0]).stem

        # Create a project file to store the results
        prj_path = str(folder_path / "project.db")
        logging.debug(prj_path)

        if not Path(prj_path).exists():
            self.project = RtiSqliteProjects(file_path=prj_path)
            self.project.create_tables()
            prj_idx = self.project.add_prj_sql("project", prj_path)

            # Begin the batch writing to the database
            self.project.begin_batch("project")

            # Process the selected file
            rti_check.process(file_paths, show_live_error=False)

            # End any remaining batch
            self.project.end_batch()

        # Plot heatmap
        #self.heatmap.get_plot("mag")
        #self.heatmap.get_plot("dir")

        # Plot mag and direction line plot
        #self.mag_dir_line.get_bin_selector()
        #self.mag_dir_line.get_plot("mag")
        #self.mag_dir_line.get_plot("dir")
        #self.ancillary_line.get_plot()
        StreamlitAncillaryLine.get_sqlite_plot(prj_path)

        # Plot the Voltage
        #self.volt_line.get_plot()
        StreamlitPowerLine.get_sqlite_plot(prj_path)

    def ens_handler(self, sender, ens):
        if ens.IsEnsembleData:
            logging.debug(str(ens.EnsembleData.EnsembleNumber))

        #self.display_ens.process_ens(ens)
        #self.plot_manager.update_dashboard_ens(ens)


        # Add data to the SQLite project
        self.project.add_ensemble(ens)

        # Write the ensembles to the database in batches
        # This will write after 10 ensembles
        #self.ens_count = self.ens_count + 1
        #if self.ens_count % 2:
        #    self.project.end_batch()
        #    self.project.begin_batch("project")


        # Add data to plots
        #self.heatmap.add_ens(ens)
        #self.mag_dir_line.add_ens(ens)
        #self.volt_line.add_ens(ens)
        #self.ancillary_line.add_ens(ens)



if __name__ == "__main__":
    fd = FileDiag()
