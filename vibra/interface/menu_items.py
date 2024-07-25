import os
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from vibra import app, ICON_DIR
from vibra.interface.analysis.analysis_setup_input import AnalysisSetupInput
from vibra.interface.analysis.analysis_type_input import AnalysisTypeInput
from vibra.interface.model_inputs.structural.material.set_material_input import SetMaterialInput
from vibra.interface.model_inputs.acoustic.fluid.set_fluid_input import SetFluidInput
from vibra.interface.mesh.mesher_inputs import MesherInputs
#
from vibra.interface.model_inputs.acoustic.set_acoustic_pressure import AcousticPressureInput
from vibra.interface.model_inputs.acoustic.set_mass_flow_rate_inputs import MassFlowRateInput
from vibra.interface.model_inputs.acoustic.set_surface_velocity_inputs import SurfaceVelocityInput
from vibra.interface.model_inputs.acoustic.set_specific_impedance_inputs import SpecificImpedanceInput
from vibra.interface.model_inputs.acoustic.set_anechoic_termination_inputs import SetAnechoicTerminationInputs
from vibra.interface.model_inputs.acoustic.set_dissipation_model_inputs import DissipationModelInput
from vibra.interface.model_inputs.acoustic.set_lrf_eq_model_inputs import LowReducedFrequencyEquivalentModelInput
from vibra.interface.model_inputs.acoustic.set_porous_material_model import SetPorousMaterialModel
from vibra.interface.model_inputs.acoustic.set_compressor_model_input import CompressorModelInput
#
from vibra.interface.model_inputs.structural.boundary_condition_inputs import BoundaryConditionInputs
from vibra.interface.plots.acoustic.plot_acoustic_pressure_frequency_response_input import PlotAcousticPressureFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_acoustic_frequency_response_function_input import PlotAcousticFrequencyResponseFunctionInput
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import PlotSpecificAcousticImpedanceInput
from vibra.interface.plots.acoustic.plot_transmission_loss_input import PlotTransmissionLossInput
#
from vibra.interface.process_analysis import ProcessAnalysis

from vibra.interface.loading_bar import load_function
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.errors import IncompleteMeshSetup, IncompleteSetupError
from vibra.interface.exception_message import ErrorMessage


class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def sizeHint(self, option, index):
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        if pen is not None:
            # Make some room for the border
            # When width is 0, it is a cosmetic pen which
            # will be 1 pixel anyways, so set it to 1
            width = max(pen.width(), 1)
            size = size + QSize(2 * width, 2 * width)
        return size

    def size(self, item):
        separator_size = QSize()
        separator_size.setHeight(2)
        return item.setSizeHint(0, separator_size)

    def paint(self, painter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)

        if pen is not None:
            width = max(pen.width(), 1)
            # ...and remove the extra room we added in sizeHint...
            option.rect.adjust(width, width, -width, -width)

        super(BorderItemDelegate, self).paint(painter, option, index)

        if pen is not None:
            painter.save()  # Saves previous status

            # Align rect
            painter.setClipRect(rect, Qt.ReplaceClip)
            pen.setWidth(2 * width)

            # Paint the borders
            painter.setPen(pen)
            painter.drawRect(rect)

            painter.restore()  # Recovers previous status


class MenuItems(QTreeWidget):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """

    def __init__(self):
        super().__init__()

        self.main_window = app().main_window

        # self._createIcons()
        # self._configItemSizes()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._addItems()
        self._configItems()
        self.update_items()
        # self.modify_analysis_items_acces(True)
        self._initial_items_acces_config()

        self.setMinimumWidth(220)
        self.setMaximumWidth(280)

    def keyPressEvent(self, event):
        """This deals with key events that are directly linked with the menu."""
        if event.key() == Qt.Key_F5:
            if not self.item_child_runAnalysis.isDisabled():
                self.run_analysis()

    def _createIcons(self):
        """Create Icons objects that are placed on the right side of the item.
        Currently isn't used.
        """
        self.icon_child_set_material = QIcon()
        self.icon_child_set_material.addPixmap(QPixmap(str(ICON_DIR)), QIcon.Active, QIcon.On)

    def _createFonts(self):
        """Create Font objects that configure the font of the items."""
        self.font_top_Items = QFont()
        # self.font_top_Items.setFamily("Segoe UI")
        self.font_top_Items.setPointSize(10)
        self.font_top_Items.setBold(True)
        self.font_top_Items.setItalic(False)
        self.font_top_Items.setWeight(60)

        self.font_child_Items = QFont()
        # self.font_child_Items.setFamily("Segoe UI")
        self.font_child_Items.setPointSize(9)
        # self.font_child_Items.setBold(False)
        # self.font_child_Items.setItalic(True)
        self.font_child_Items.setWeight(50)

    def _createColorsBrush(self):
        """Create Color objects that define the color of the text and/or background of the items."""

        self.QLinearGradient_upper = QLinearGradient(0, 0, 400, 0)
        self.QLinearGradient_upper.setColorAt(1, QColor(60, 60, 60, 150))
        self.QLinearGradient_upper.setColorAt(0, QColor(220, 220, 220, 150))

        self.QLinearGradient_lower = QLinearGradient(0, 0, 400, 0)
        self.QLinearGradient_lower.setColorAt(1, QColor(102, 204, 255, 100))
        self.QLinearGradient_lower.setColorAt(0, QColor(240, 240, 240, 150))

        self.brush_upper_items = QBrush(self.QLinearGradient_upper)
        self.brush_upper_items.setStyle(Qt.LinearGradientPattern)

        self.brush_lower_items = QBrush(self.QLinearGradient_lower)
        self.brush_lower_items.setStyle(Qt.LinearGradientPattern)

    def _configItemSizes(self):
        """Creates a control to the items height size."""
        self.top_items_size = QSize()
        self.top_items_size.setHeight(35)
        self.child_items_size = QSize()
        self.child_items_size.setHeight(20)

    def _configTree(self):
        """Define the initial configuration of the TreeWidget."""
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setRootIsDecorated(True)
        self.setFrameShape(1)
        # self.setFrameShadow(3)
        self.setLineWidth(2)
        # self.setIndentation(20)
        # self.setColumnWidth(0, 50)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        """Creates all TreeWidgetItems."""
        self.list_top_items = []
        self.list_child_items = []
        self.item_top_generalSettings = QTreeWidgetItem(["General Settings"])
        self.item_child_import_geometry = QTreeWidgetItem(["Import geometry"])
        self.item_child_mesh_setup = QTreeWidgetItem(["Mesh Setup"])
        self.item_child_generate_mesh = QTreeWidgetItem(["Generate Mesh"])
        self.item_child_set_material = QTreeWidgetItem(["Set Material"])
        self.item_child_set_fluid = QTreeWidgetItem(["Set Fluid"])
        #
        material_tool_tip = "Attribute material to selected bodies. \ndefault material: steel (E = 210 GPa; poisson = 0.30; density = 7860 kg/m³)"
        fluid_tool_tip = "Attribute fluid to selected bodies. \ndefault fluid: air (speed of sound 343.2021 m/s; fluid density = 1.215 kg/m³)"
        self.item_child_set_material.setToolTip(0, material_tool_tip)
        self.item_child_set_fluid.setToolTip(0, fluid_tool_tip)
        #
        self.list_top_items.append(self.item_top_generalSettings)
        self.list_child_items.append(self.item_child_import_geometry)
        self.list_child_items.append(self.item_child_mesh_setup)
        self.list_child_items.append(self.item_child_set_material)
        self.list_child_items.append(self.item_child_set_fluid)
        #
        self.item_top_structuralModelSetup = QTreeWidgetItem(["Structural Model Setup"])
        self.item_child_set_boundary_condition = QTreeWidgetItem(["Set Boundary Conditions"])
        self.item_child_setNodalLoads = QTreeWidgetItem(["Set Loads"])
        #
        self.list_top_items.append(self.item_top_structuralModelSetup)
        self.list_child_items.append(self.item_child_set_boundary_condition)
        self.list_child_items.append(self.item_child_setNodalLoads)
        #
        self.item_top_acoustic_model_setup = QTreeWidgetItem(["Acoustic Model Setup"])
        self.item_child_set_dissipation_model = QTreeWidgetItem(["Set Dissipation Model"])
        self.item_child_set_acoustic_pressure = QTreeWidgetItem(["Set Acoustic Pressure"])
        self.item_child_set_mass_flow_rate = QTreeWidgetItem(["Set Mass Flow Rate"])
        self.item_child_set_surface_velocity = QTreeWidgetItem(["Set Surface Velocity"])
        self.item_child_set_anechoic_termination = QTreeWidgetItem(["Set Anechoic Termination"])
        self.item_child_set_specific_impedance = QTreeWidgetItem(["Set Specific Impedance"])
        self.item_child_set_lrf_eq_model = QTreeWidgetItem(["Set LRF Equivalent Model"])
        self.item_child_set_porous_material_model = QTreeWidgetItem(["Set Porous Material Model"])
        self.item_child_add_compressor_excitation = QTreeWidgetItem(["Add Compressor Excitation"])

        self.item_child_set_anechoic_termination.setToolTip(0, "equivalent to the long pipe boundary condition")

        #
        self.list_top_items.append(self.item_top_acoustic_model_setup)
        self.list_child_items.append(self.item_child_set_acoustic_pressure)
        self.list_child_items.append(self.item_child_set_dissipation_model)
        self.list_child_items.append(self.item_child_set_mass_flow_rate)
        self.list_child_items.append(self.item_child_set_surface_velocity)
        self.list_child_items.append(self.item_child_set_specific_impedance)
        self.list_child_items.append(self.item_child_set_anechoic_termination)
        self.list_child_items.append(self.item_child_add_compressor_excitation)
        self.list_child_items.append(self.item_child_set_porous_material_model)
        self.list_child_items.append(self.item_child_set_lrf_eq_model)
        #
        self.item_top_analysis = QTreeWidgetItem(["Analysis"])
        self.item_child_selectAnalysisType = QTreeWidgetItem(["Select Analysis Type"])
        self.item_child_analysisSetup = QTreeWidgetItem(["Analysis Setup"])
        self.item_child_runAnalysis = QTreeWidgetItem(["Run Analysis"])
        self.item_child_reset_solution = QTreeWidgetItem(["Reset Solution"])
        self.item_child_analysisSetup.setDisabled(True)
        #
        self.list_top_items.append(self.item_top_analysis)
        self.list_child_items.append(self.item_child_selectAnalysisType)
        self.list_child_items.append(self.item_child_analysisSetup)
        self.list_child_items.append(self.item_child_runAnalysis)
        self.list_child_items.append(self.item_child_reset_solution)
        #
        self.item_top_resultsViewer_structural = QTreeWidgetItem(["Results Viewer - Structural"])
        self.item_child_plotStructuralModeShapes = QTreeWidgetItem(["Plot Structural Mode Shapes"])
        self.item_child_plotDisplacementField = QTreeWidgetItem(["Plot Displacement Field"])
        self.item_child_plotStructuralFrequencyResponse = QTreeWidgetItem(["Plot Structural Frequency Response"])
        self.item_child_plotReactionsFrequencyResponse = QTreeWidgetItem(["Plot Reactions Frequency Response"])
        self.item_child_plotStressField = QTreeWidgetItem(["Plot Stress Field"])
        self.item_child_plotStressFrequencyResponse = QTreeWidgetItem(["Plot Stress Frequency Response"])
        #
        self.list_top_items.append(self.item_top_resultsViewer_structural)
        self.list_child_items.append(self.item_child_plotStructuralModeShapes)
        self.list_child_items.append(self.item_child_plotDisplacementField)
        self.list_child_items.append(self.item_child_plotStructuralFrequencyResponse)
        self.list_child_items.append(self.item_child_plotReactionsFrequencyResponse)
        self.list_child_items.append(self.item_child_plotStressField)
        self.list_child_items.append(self.item_child_plotStressFrequencyResponse)
        #
        self.item_top_resultsViewer_acoustic = QTreeWidgetItem(["Results Viewer - Acoustic"])
        self.item_child_plotAcousticModeShapes = QTreeWidgetItem(["Plot Acoustic Mode Shapes"])
        self.item_child_plot_acoustic_pressure_field = QTreeWidgetItem(["Plot Acoustic Pressure Field"])
        self.item_child_plot_acoustic_pressure_frequency_response = QTreeWidgetItem(["Plot Acoustic Pressure Frequency Response"])
        self.item_child_plot_acoustic_pressure_frequency_response_function = QTreeWidgetItem(["Plot Acoustic Pressure Frequency Response Function"])
        self.item_child_plotAcousticDeltaPressures = QTreeWidgetItem(["Plot Acoustic Delta Pressures"])
        self.item_child_plot_TL_NR = QTreeWidgetItem(["Plot Transmission Loss or Attenuation"])
        #
        self.list_top_items.append(self.item_top_resultsViewer_acoustic)
        self.list_child_items.append(self.item_child_plotAcousticModeShapes)
        self.list_child_items.append(self.item_child_plot_acoustic_pressure_field)
        self.list_child_items.append(self.item_child_plot_acoustic_pressure_frequency_response)
        self.list_child_items.append(self.item_child_plot_acoustic_pressure_frequency_response_function)
        self.list_child_items.append(self.item_child_plotAcousticDeltaPressures)
        self.list_child_items.append(self.item_child_plot_TL_NR)
        #

    def _addItems(self):
        """Adds the Top Level Items and the Child Levels Items at the TreeWidget."""
        self.addTopLevelItem(self.item_top_generalSettings)
        self.item_top_generalSettings.addChild(self.item_child_import_geometry)
        self.item_top_generalSettings.addChild(self.item_child_set_material)
        self.item_top_generalSettings.addChild(self.item_child_set_fluid)
        self.item_top_generalSettings.addChild(self.item_child_mesh_setup)

        self.addTopLevelItem(self.item_top_structuralModelSetup)
        self.item_top_structuralModelSetup.addChild(self.item_child_set_boundary_condition)
        self.item_top_structuralModelSetup.addChild(self.item_child_setNodalLoads)

        self.addTopLevelItem(self.item_top_acoustic_model_setup)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_acoustic_pressure)
        # self.item_top_acoustic_model_setup.addChild(self.item_child_set_mass_flow_rate)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_surface_velocity)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_anechoic_termination)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_specific_impedance)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_dissipation_model)
        self.item_top_acoustic_model_setup.addChild(self.item_child_set_porous_material_model)
        # self.item_top_acoustic_model_setup.addChild(self.item_child_set_lrf_eq_model)
        # self.item_top_acoustic_model_setup.addChild(self.item_child_add_compressor_excitation)

        self.addTopLevelItem(self.item_top_analysis)
        self.item_top_analysis.addChild(self.item_child_selectAnalysisType)
        self.item_top_analysis.addChild(self.item_child_analysisSetup)
        self.item_top_analysis.addChild(self.item_child_runAnalysis)
        self.item_top_analysis.addChild(self.item_child_reset_solution)

        self.addTopLevelItem(self.item_top_resultsViewer_structural)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStructuralModeShapes)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotDisplacementField)
        self.item_top_resultsViewer_structural.addChild(
            self.item_child_plotStructuralFrequencyResponse
        )
        # self.item_top_resultsViewer_structural.addChild(self.item_child_plotReactionsFrequencyResponse)
        # self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressField)
        # self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressFrequencyResponse)

        self.addTopLevelItem(self.item_top_resultsViewer_acoustic)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticModeShapes)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_acoustic_pressure_field)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_acoustic_pressure_frequency_response)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_acoustic_pressure_frequency_response_function)
        # self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticDeltaPressures)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_TL_NR)

    def _configItems(self):
        """Configure all items."""

        borderRole = Qt.UserRole + 1

        if self.main_window.user_config.theme == "light":
            # textTopBrush = QBrush(QColor(0,0,0))
            borderPen = QPen(QColor(0, 0, 0))
        elif self.main_window.user_config.theme == "dark":
            # textTopBrush = QBrush(QColor(255,255,255))
            borderPen = QPen(QColor(255, 255, 255))

        borderPen.setWidth(1)

        configTopBrush = self.brush_upper_items
        plotTopBrush = self.brush_lower_items

        configTopItems = [
            self.item_top_generalSettings,
            self.item_top_structuralModelSetup,
            self.item_top_acoustic_model_setup,
        ]

        for top_item in self.list_top_items:
            top_item.setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            top_item.setFont(0, self.font_top_Items)
            top_item.setData(0, borderRole, borderPen)
            top_item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            # top_item.setForeground(0, textTopBrush)
            # top_item.setSizeHint(0, self.top_items_size)

            if top_item in configTopItems:
                top_item.setBackground(0, configTopBrush)
                self.expandItem(top_item)
            else:
                top_item.setBackground(0, plotTopBrush)

        delegate = BorderItemDelegate(self, borderRole)
        self.setItemDelegate(delegate)

        for child_item in self.list_child_items:
            child_item.setFont(0, self.font_child_Items)
            # child_item.setForeground(0, textTopBrush)
            # child_item.setSizeHint(0, self.top_items_size)

    def update_childItems_visibility(self, item):
        toggle = lambda x: x.setExpanded(not x.isExpanded())
        if item in self.list_top_items:
            toggle(item)
            return True
        return False

    def on_click_item(self, item, column):
        """This event is raised every time an item is clicked on the menu."""

        self.before_initilize()
        if self.update_childItems_visibility(item):
            return

        self.generate_mesh_action = self.main_window.findChild(QAction, "generate_mesh_action")

        if item == self.item_child_import_geometry:
            if not self.item_child_import_geometry.isDisabled():
                self.main_window.import_geometry_dialog()
                if app().main_window.file.read_geometry_from_file():
                    self.modify_items_access_after_geometry_importing()

        elif item == self.item_child_mesh_setup:
            if not self.item_child_mesh_setup.isDisabled():
                obj = MesherInputs()
                if obj.complete:
                    self.modify_items_access_after_geometry_importing()
                    self.main_window.viewer_tabs.close_analysis_tabs()

        elif item == self.item_child_set_material:
            if not self.item_child_set_material.isDisabled():
                obj = SetMaterialInput()

        elif item == self.item_child_set_fluid:
            if not self.item_child_set_fluid.isDisabled():
                obj = SetFluidInput()

        elif item == self.item_child_set_boundary_condition:
            if not self.item_child_set_boundary_condition.isDisabled():
                obj = BoundaryConditionInputs()

        elif item == self.item_child_setNodalLoads:
            if not self.item_child_setNodalLoads.isDisabled():
                pass

        elif item == self.item_child_set_acoustic_pressure:
            if not self.item_child_set_acoustic_pressure.isDisabled():
                obj = AcousticPressureInput()

        elif item == self.item_child_set_dissipation_model:
            if not self.item_child_set_dissipation_model.isDisabled():
                obj = DissipationModelInput()

        elif item == self.item_child_set_lrf_eq_model:
            if not self.item_child_set_lrf_eq_model.isDisabled():
                obj = LowReducedFrequencyEquivalentModelInput()

        elif item == self.item_child_set_porous_material_model:
            if not self.item_child_set_porous_material_model.isDisabled():
                obj = SetPorousMaterialModel()

        elif item == self.item_child_set_mass_flow_rate:
            if not self.item_child_set_mass_flow_rate.isDisabled():
                obj = MassFlowRateInput()

        elif item == self.item_child_set_surface_velocity:
            if not self.item_child_set_surface_velocity.isDisabled():
                obj = SurfaceVelocityInput()

        elif item == self.item_child_set_specific_impedance:
            if not self.item_child_set_specific_impedance.isDisabled():
                obj = SpecificImpedanceInput()

        elif item == self.item_child_set_anechoic_termination:
            if not self.item_child_set_anechoic_termination.isDisabled():
                obj = SetAnechoicTerminationInputs()

        elif item == self.item_child_add_compressor_excitation:
            if not self.item_child_add_compressor_excitation.isDisabled():
                obj = CompressorModelInput()

        elif item == self.item_child_selectAnalysisType:
            if not self.item_child_selectAnalysisType.isDisabled():
                analysis_type = AnalysisTypeInput()
                if analysis_type.complete:

                    if analysis_type.analysis_id in [2, 4]:
                        self.run_analysis()
                        self.item_child_runAnalysis.setDisabled(False)
                        # self.item_child_reset_solution.setDisabled(False)

                    else:

                        analysis_setup = AnalysisSetupInput()
                        self.item_child_analysisSetup.setDisabled(False)

                        if analysis_setup.complete:
                            self.item_child_runAnalysis.setDisabled(False)
                            # self.item_child_reset_solution.setDisabled(False)

                        if analysis_setup.solve_analysis:
                            self.run_analysis()

        elif item == self.item_child_analysisSetup:
            if not self.item_child_analysisSetup.isDisabled():
                analysis_setup = AnalysisSetupInput()

        elif item == self.item_child_runAnalysis:
            if not self.item_child_runAnalysis.isDisabled():
                self.run_analysis()

        elif item == self.item_child_reset_solution:
            if not self.item_child_reset_solution.isDisabled():
                self.reset_solution()

        elif item == self.item_child_plotStructuralModeShapes:
            if not self.item_child_plotStructuralModeShapes.isDisabled():
                self.main_window.viewer_tabs.show_structural_modal_analysis()

        elif item == self.item_child_plotDisplacementField:
            if not self.item_child_plotDisplacementField.isDisabled():
                pass

        elif item == self.item_child_plotStructuralFrequencyResponse:
            if not self.item_child_plotStructuralFrequencyResponse.isDisabled():
                pass

        elif item == self.item_child_plotReactionsFrequencyResponse:
            if not self.item_child_plotReactionsFrequencyResponse.isDisabled():
                pass

        elif item == self.item_child_plotStressField:
            if not self.item_child_plotStressField.isDisabled():
                pass

        elif item == self.item_child_plotStressFrequencyResponse:
            if not self.item_child_plotStressFrequencyResponse.isDisabled():
                pass

        elif item == self.item_child_plotAcousticModeShapes:
            if not self.item_child_plotAcousticModeShapes.isDisabled():
                self.main_window.viewer_tabs.show_acoustic_modal_analysis()

        elif item == self.item_child_plot_acoustic_pressure_field:
            if not self.item_child_plot_acoustic_pressure_field.isDisabled():
                self.main_window.viewer_tabs.show_acoustic_harmonic_analysis()

        elif item == self.item_child_plot_acoustic_pressure_frequency_response:
            if not self.item_child_plot_acoustic_pressure_frequency_response.isDisabled():
                PlotAcousticPressureFrequencyResponseInput()  

        elif item == self.item_child_plot_acoustic_pressure_frequency_response_function:
            if not self.item_child_plot_acoustic_pressure_frequency_response_function.isDisabled():
                PlotAcousticFrequencyResponseFunctionInput()

        elif item == self.item_child_plot_TL_NR:
            if not self.item_child_plot_TL_NR.isDisabled():
                PlotTransmissionLossInput()

    def generate_mesh(self):
        """ """
        generate_mesh = load_function(self.main_window.project.generate_mesh, self.main_window)
        generate_mesh()
        self.main_window.viewer_tabs.show_mesh()
        self.generate_mesh_action.setDisabled(True)
        self.item_child_generate_mesh.setDisabled(True)

    def run_analysis(self):
        """ """
        if not self.main_window.project.model.generated_mesh:
            obj = MesherInputs()
            if obj.complete:
                self.main_window.viewer_tabs.close_analysis_tabs()
                self.main_window.viewer_tabs.update_plots()
            else:
                return
        #
        if self.main_window.project.analysis_data is None:
            return
        #
        # if not self.main_window.project.model.generated_mesh:
        #     try:
        #         self.generate_mesh()
        #     except IncompleteSetupError or IncompleteMeshSetup as error:
        #         # Please use this error message. It is easy to use,
        #         # is very clean and follows the operational system standard.
        #         ErrorMessage(error)
        #         return
        #

        self.modify_items_acoustic_results_viewer(True)
        self.modify_items_structural_results_viewer(True)

        analysis = ProcessAnalysis()

        analysis_id = self.main_window.project.analysis_data["analysis_id"]
        #
        if analysis_id == 2:
            solve_modal = load_function(analysis.process_structural_modal_analysis, 
                                        self.main_window)
            solve_modal()

        elif analysis_id == 3:
            solve_harmonic = load_function(analysis.process_acoustic_harmonic_analysis, 
                                           self.main_window)
            solve_harmonic()

        elif analysis_id == 4:
            solve_modal = load_function(analysis.process_acoustic_modal_analysis, 
                                        self.main_window)
            solve_modal()
        else:
            raise NotImplementedError("Not implemented analysis")
        self.update_items()

    def reset_solution(self):

        app().main_window.project.reset_solutions()
        app().main_window.viewer_tabs.reset_solution_tabs_visibility()
        app().main_window.file.remove_results_data_from_project_file()

        self.modify_items_acoustic_results_viewer(True)
        self.modify_items_structural_results_viewer(True)
        self.item_child_reset_solution.setDisabled(True)

    def _initial_items_acces_config(self):
        """ """
        for child_item in self.list_child_items:
            child_item.setDisabled(True)
        self.item_child_import_geometry.setDisabled(False)
        self.item_top_structuralModelSetup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(True)
        self.item_top_analysis.setHidden(True)

    def modify_geometry_item_access(self, bool_key):
        self.item_child_import_geometry.setDisabled(bool_key)
        self.item_child_mesh_setup.setDisabled(bool_key)

    def modify_general_settings_items_access(self, bool_key):
        self.item_child_import_geometry.setDisabled(bool_key)
        self.item_child_mesh_setup.setDisabled(bool_key)
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_generate_mesh.setDisabled(True)

    def modify_structural_model_setup_items_acces(self, bool_key):
        self.item_child_set_boundary_condition.setDisabled(bool_key)
        self.item_child_setNodalLoads.setDisabled(bool_key)

    def modify_acoustic_model_setup_items_acces(self, bool_key):
        self.item_child_set_acoustic_pressure.setDisabled(bool_key)
        self.item_child_set_mass_flow_rate.setDisabled(bool_key)
        self.item_child_set_surface_velocity.setDisabled(bool_key)
        self.item_child_set_specific_impedance.setDisabled(bool_key)
        self.item_child_set_anechoic_termination.setDisabled(bool_key)
        self.item_child_set_dissipation_model.setDisabled(bool_key)
        self.item_child_set_lrf_eq_model.setDisabled(bool_key)
        self.item_child_set_porous_material_model.setDisabled(bool_key)
        self.item_child_add_compressor_excitation.setDisabled(bool_key)

    def modify_analysis_items_acces(self, bool_key):
        self.item_child_selectAnalysisType.setDisabled(bool_key)
        self.item_child_runAnalysis.setDisabled(bool_key)
        self.item_child_reset_solution.setDisabled(bool_key)

    def modify_items_acoustic_results_viewer(self, bool_key):
        self.item_top_resultsViewer_acoustic.setHidden(bool_key)
        self.item_child_plotAcousticModeShapes.setDisabled(bool_key)
        self.item_child_plot_acoustic_pressure_frequency_response.setDisabled(bool_key)
        self.item_child_plot_acoustic_pressure_frequency_response_function.setDisabled(bool_key)
        self.item_child_plot_acoustic_pressure_field.setDisabled(bool_key)
        self.item_child_plotAcousticDeltaPressures.setDisabled(bool_key)
        self.item_child_plot_TL_NR.setDisabled(bool_key)

    def modify_items_structural_results_viewer(self, bool_key):
        self.item_top_resultsViewer_structural.setHidden(bool_key)
        self.item_child_plotDisplacementField.setDisabled(bool_key)
        self.item_child_plotStructuralFrequencyResponse.setDisabled(bool_key)
        self.item_child_plotReactionsFrequencyResponse.setDisabled(bool_key)
        self.item_child_plotStressField.setDisabled(bool_key)
        self.item_child_plotStructuralModeShapes.setDisabled(bool_key)

    def modify_items_access_after_geometry_importing(self):

        self.main_window.renderer_toolbar.setDisabled(False)
        self.modify_general_settings_items_access(False)
        self.modify_acoustic_model_setup_items_acces(False)
        self.modify_structural_model_setup_items_acces(False)
        self.modify_analysis_items_acces(False)

        self.item_top_resultsViewer_structural.setHidden(True)
        self.item_top_resultsViewer_acoustic.setHidden(True)
        self.item_top_analysis.setHidden(False)

        self.item_child_runAnalysis.setDisabled(True)
        self.item_child_reset_solution.setDisabled(True)
        self.filter_analysis_type()

    def filter_analysis_type(self):
        if not self.item_top_analysis.isHidden():
            self.item_top_acoustic_model_setup.setHidden(True)
            self.item_top_structuralModelSetup.setHidden(True)
            index = self.main_window.analysis_filter.comboBox_analysis_selector.currentIndex()
            if index == 0:# self.main_window.analysis_filter.radio_button_acoustic.isChecked():
                self.item_top_acoustic_model_setup.setHidden(False)
            elif index == 1:# self.main_window.analysis_filter.radio_button_structural.isChecked():
                self.item_top_structuralModelSetup.setHidden(False)
            else:
                self.item_top_acoustic_model_setup.setHidden(False)
                self.item_top_structuralModelSetup.setHidden(False)

    def update_items(self):
        """Enables and disables the Child Items on the menu after the solution is done."""

        self.item_top_resultsViewer_structural.setHidden(True)
        self.item_top_resultsViewer_acoustic.setHidden(True)

        if self.main_window.project.analysis_data is None:
            return

        analysis_id = self.main_window.project.analysis_data["analysis_id"]

        # if self.main_window.project.analysis_id in [None, 2,4]:
        #     self.item_child_analysisSetup.setDisabled(True)
        # else:
        #     self.item_child_analysisSetup.setDisabled(False)

        # if self.main_window.project.analysis_id is not None and self.main_window.project.setup_analysis_complete:
        #     self.item_child_runAnalysis.setDisabled(False)

        # if self.main_window.project.get_structural_solution() is not None or self.main_window.project.get_acoustic_solution() is not None:

        self.modify_items_acoustic_results_viewer(True)
        self.modify_items_structural_results_viewer(True)
        self.item_child_reset_solution.setDisabled(False)

        if analysis_id in [0, 1, 2]:
            self.item_top_resultsViewer_structural.setHidden(False)

        elif analysis_id in [3, 4]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            
        elif analysis_id in [5, 6]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.item_top_resultsViewer_structural.setHidden(False)

        if analysis_id == 0 or analysis_id == 1:
            self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
            self.item_child_plotDisplacementField.setDisabled(False)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
            self.item_child_plotStressField.setDisabled(False)
            self.item_child_plotStressFrequencyResponse.setDisabled(False)

        elif analysis_id == 2:
            self.item_child_plotStructuralModeShapes.setDisabled(False)
            # if get_acoustic_solution() is not None:
            #     self.item_child_plotAcousticModeShapes.setDisabled(False)

        elif analysis_id == 4:
            self.item_child_plotAcousticModeShapes.setDisabled(False)
            # if get_structural_solution() is not None:
            #     self.item_child_plotStructuralModeShapes.setDisabled(False)

        elif analysis_id == 3:
            self.item_child_plot_acoustic_pressure_frequency_response.setDisabled(False)
            self.item_child_plot_acoustic_pressure_frequency_response_function.setDisabled(False)
            self.item_child_plot_acoustic_pressure_field.setDisabled(False)
            self.item_child_plotAcousticDeltaPressures.setDisabled(False)
            self.item_child_plot_TL_NR.setDisabled(False)

        elif analysis_id in [5, 6]:
            # acoustic
            self.item_child_plot_acoustic_pressure_field.setDisabled(False)
            self.item_child_plot_acoustic_pressure_frequency_response.setDisabled(False)
            self.item_child_plot_acoustic_pressure_frequency_response_function.setDisabled(False)
            self.item_child_plotAcousticDeltaPressures.setDisabled(False)
            self.item_child_plot_TL_NR.setDisabled(False)
            # structural
            self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
            self.item_child_plotStressField.setDisabled(False)
            self.item_child_plotStressFrequencyResponse.setDisabled(False)
            self.item_child_plotDisplacementField.setDisabled(False)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(False)

        self.update_TreeVisibility_after_solution()

    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items ont the menu after the solution is done."""
        self.collapseItem(self.item_top_generalSettings)
        self.collapseItem(self.item_top_structuralModelSetup)
        self.collapseItem(self.item_top_acoustic_model_setup)
        analysis_id = self.main_window.project.analysis_data["analysis_id"]

        if analysis_id in [0, 1, 2]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            # self.expandItem(self.item_top_structuralModelSetup)
        elif analysis_id in [3, 4]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_acoustic)
            # self.expandItem(self.item_top_acoustic_model_setup)
        elif analysis_id in [5, 6]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            self.expandItem(self.item_top_resultsViewer_acoustic)

    def update_structural_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(True)

    def update_acoustic_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(False)

    def update_coupled_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(False)

    def empty_project_action_message(self):

        window_title = "Error"
        title = "Empty project"

        message = "Please, you should create a new project or load an already existing one before start to set up the model."
        message += " It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."

        PrintMessageInput([window_title, title, message])

    def before_initilize(self):
        if self.main_window.dialog is not None:
            self.main_window.dialog.close()
            self.main_window.set_input_widget(None)
