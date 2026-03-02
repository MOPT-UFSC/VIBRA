from PySide6.QtWidgets import QTextEdit

from vibra.interface.menus.tool_tips_dict import tool_tips

class ToolTip:
    def __init__(self):
        self.tool_tips: dict[str, str] = tool_tips
    
    def get_tooltip_QTextEdit(self, property_name: str) -> QTextEdit | None:
        if property_name not in self.tool_tips.keys():
            return None
        
        text = self.tool_tips[property_name]
        return QTextEdit(markdown=text)