"""Handler for solid selection mode in 3D viewer."""
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_YELLOW

from simple_cad.service.geometry_service import extractSolidsFromShape


class VolumeSelectionHandler:
    """Encapsulates solid selection logic and state."""
    
    def __init__(self, occ_window):
        self.occ_window = occ_window
        self._is_active = False
        self._volume_ais_list = []  # List of (ais_shape, solid, selected)
        self._source_geometry = None
        self._selection_changed_callback = None
    
    def set_selection_changed_callback(self, callback):
        """Set callback to be called when selection changes.
        
        Args:
            callback: Function that takes (selected_count, total_count) as parameters
        """
        self._selection_changed_callback = callback
    
    def activate(self, geometry):
        """Start solid selection mode for a geometry.
        
        Args:
            geometry: The geometry to display and allow selection of solids
        """
        if self._is_active:
            return
        
        self._is_active = True
        self._source_geometry = geometry
        
        # Clear current display
        self.occ_window.display.EraseAll()
        self._volume_ais_list = []
        
        # Extract and display solids
        solids = extractSolidsFromShape(geometry.GetShape())
        
        for solid in solids:
            ais = AIS_Shape(solid)
            ais.SetTransparency(0.5)
            self.occ_window.display.Context.Display(ais, True)
            self._volume_ais_list.append((ais, solid, False))  # (ais, solid, selected)
        
        self.occ_window.addCoordinateAxis()
        self.occ_window.display.FitAll()
        
        # Notify of initial state
        self._notify_selection_changed()
    
    def deactivate(self):
        """Exit solid selection mode."""
        if not self._is_active:
            return
        
        self._is_active = False
        self._volume_ais_list = []
        self._source_geometry = None
        
        # Restore normal view
        self.occ_window.updateView()
    
    def handle_mouse_click(self, selected_ais):
        """Handle mouse click in solid selection mode.
        
        Args:
            selected_ais: The AIS object that was clicked
            
        Returns:
            bool: True if click was handled, False otherwise
        """
        if not self._is_active:
            return False
        
        ctx = self.occ_window.display.Context
        
        # Find which solid was clicked
        for i, (ais_shape, solid, selected) in enumerate(self._volume_ais_list):
            if ais_shape == selected_ais:
                # Toggle selection
                self._volume_ais_list[i] = (ais_shape, solid, not selected)
                
                # Update visual appearance
                if not selected:  # Now selected
                    ais_shape.SetColor(Quantity_Color(Quantity_NOC_YELLOW))
                    ais_shape.SetTransparency(0.2)
                else:  # Now deselected
                    ais_shape.UnsetColor()
                    ais_shape.SetTransparency(0.5)
                
                ctx.Redisplay(ais_shape, True)
                self._notify_selection_changed()
                return True
        
        return False
    
    def get_selected_volumes(self):
        """Return list of selected solids."""
        return [solid for _, solid, selected in self._volume_ais_list if selected]
    
    def get_total_volumes(self):
        """Return total number of solids."""
        return len(self._volume_ais_list)
    
    def is_active(self):
        """Check if solid selection mode is active."""
        return self._is_active
    
    def _notify_selection_changed(self):
        """Notify callback that selection state has changed."""
        if self._selection_changed_callback:
            selected_count = len(self.get_selected_volumes())
            total_count = self.get_total_volumes()
            self._selection_changed_callback(selected_count, total_count)
