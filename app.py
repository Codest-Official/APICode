import re
import sys
import json
import subprocess
import platform
from pathlib import Path
from datetime import datetime
import shutil
import psutil
import gpustat
import tempfile
import os
import queue
import ast
import difflib
import importlib.util
import unittest
import editorconfig
import hashlib
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout, 
    QSplitter, 
    QMainWindow,
    QMenu, 
    QMenuBar, 
    QStatusBar, 
    QDialog, 
    QDialogButtonBox,
    QMessageBox, 
    QInputDialog, 
    QFileDialog, 
    QStyle,
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QCheckBox, 
    QSpinBox, 
    QComboBox,
    QListWidget, 
    QListWidgetItem, 
    QTreeView, 
    QTabWidget, 
    QTabBar,
    QPlainTextEdit, 
    QTextEdit,
    QCompleter,
    QFileSystemModel, 
    QFileIconProvider,
    QGraphicsScene, 
    QGraphicsView, 
    QGraphicsItem, 
    QGraphicsItemGroup,
    QGraphicsLineItem, 
    QGraphicsEllipseItem, 
    QGraphicsTextItem, 
    QGraphicsRectItem, QTreeWidget, QTreeWidgetItem,
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView, 
    QScrollArea
)
from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)
from PySide6.QtCore import (
    Qt, 
    QRegularExpression, 
    QThread, 
    QObject, 
    Signal as pyqtSignal, 
    QTimer, QPoint, 
    QSize, QRect,
    QDir, 
    QSortFilterProxyModel, 
    QFile, 
    QLineF, 
    QPointF,
    QStringListModel, 
    QUrl,
    QModelIndex
)
from PySide6.QtGui import (
    QPen, 
    QBrush, 
    QSyntaxHighlighter, 
    QTextCharFormat, 
    QColor, 
    QFont, 
    QPainter,
    QTextDocument, 
    QTextCursor, 
    QTextFormat, 
    QStandardItemModel, 
    QStandardItem,
    QIcon, 
    QPixmap, 
    QPolygon, 
    QFontMetrics, 
    QPolygonF,
    QImage,
    QAction,
    QActionGroup,
)
from PySide6 import __version__ as PYSIDE_VERSION

THEME_PALETTES = {
      "Dark": {
      "base": "#2b2b2b", "text": "#bbbbbb", "primary": "#0d6efd", "secondary": "#3c3f41",
      "highlight": "#3c3f41", "title_bar": "#252526", "menu_hover": "#3c3f41",
      "button_hover": "#0b5ed7", "button_text": "white", "border": "#555555",
      "keyword": "#569cd6", "string": "#ce9178", "comment": "#6A9955", "number": "#b5cea8",
      # editor-specific:
      "editor_font": "Fira Code",
      "editor_font_size": 13,
      "gutter_bg": "#212223",
      "gutter_text": "#6b6b6b",
      "selection_bg": "rgba(13,110,253,0.18)",   # subtle selection
      "cursor_color": "#FFD866",
      "minimap_bg": "#222425"
    },
    "Light": {
        "base": "#f0f0f0", "text": "#000000", "primary": "#0078d4", "secondary": "#ffffff",
        "highlight": "#e8e8e8", "title_bar": "#e1e1e1", "menu_hover": "#dcdcdc",
        "button_hover": "#005a9e", "button_text": "white", "border": "#cccccc",
        "keyword": "#0000ff", "string": "#a31515", "comment": "#008000", "number": "#098658"
    },
    "Amethyst": {
        "base": "#2a2133", "text": "#d9d9d9", "primary": "#9d65ff", "secondary": "#4a3d59",
        "highlight": "#3e324b", "title_bar": "#201926", "menu_hover": "#4a3d59",
        "button_hover": "#8b51ec", "button_text": "white", "border": "#5e4d75",
        "keyword": "#c792ea", "string": "#c3e88d", "comment": "#676e95", "number": "#f78c6c"
    },
    "Gold": {
        "base": "#2c2c2c", "text": "#e0e0e0", "primary": "#ffc107", "secondary": "#424242",
        "highlight": "#383838", "title_bar": "#212121", "menu_hover": "#424242",
        "button_hover": "#e0a800", "button_text": "#000000", "border": "#616161",
        "keyword": "#fbc02d", "string": "#aed581", "comment": "#757575", "number": "#ff8a65"
    },
    "Ocean": {
        "base": "#0f111a", "text": "#c8d3f5", "primary": "#82aaff", "secondary": "#1f2335",
        "highlight": "#2a2f41", "title_bar": "#090b10", "menu_hover": "#1f2335",
        "button_hover": "#6c8eec", "button_text": "#0f111a", "border": "#3b4261",
        "keyword": "#c792ea", "string": "#c3e88d", "comment": "#545c7e", "number": "#f78c6c"
    },
    "MacOS": {
        "base": "#f5f5f7", "text": "#333333", "primary": "#007aff", "secondary": "#ffffff",
        "highlight": "#e9e9eb", "title_bar": "#e8e8e8", "menu_hover": "#dcdcdc",
        "button_hover": "#005ecb", "button_text": "white", "border": "#d1d1d6",
        "keyword": "#a200a1", "string": "#d12f2f", "comment": "#007f00", "number": "#1c00cf"
    },
    "Monokai": {
        "base": "#272822", "text": "#f8f8f2", "primary": "#f92672", "secondary": "#3e3d32",
        "highlight": "#49483e", "title_bar": "#1e1f1c", "menu_hover": "#3e3d32",
        "button_hover": "#e01e60", "button_text": "white", "border": "#75715e",
        "keyword": "#f92672", "string": "#e6db74", "comment": "#75715e", "number": "#ae81ff"
    },
    "Solarized Dark": {
        "base": "#002b36", "text": "#839496", "primary": "#268bd2", "secondary": "#073642",
        "highlight": "#073642", "title_bar": "#00212b", "menu_hover": "#073642",
        "button_hover": "#1e6a9e", "button_text": "white", "border": "#586e75",
        "keyword": "#859900", "string": "#2aa198", "comment": "#586e75", "number": "#d33682"
    },
    "Solarized Light": {
        "base": "#fdf6e3", "text": "#657b83", "primary": "#268bd2", "secondary": "#eee8d5",
        "highlight": "#eee8d5", "title_bar": "#f0eada", "menu_hover": "#e8e1cd",
        "button_hover": "#1e6a9e", "button_text": "white", "border": "#93a1a1",
        "keyword": "#859900", "string": "#2aa198", "comment": "#93a1a1", "number": "#d33682"
    },
    "Dracula": {
        "base": "#282a36", "text": "#f8f8f2", "primary": "#bd93f9", "secondary": "#44475a",
        "highlight": "#44475a", "title_bar": "#1e1f29", "menu_hover": "#44475a",
        "button_hover": "#ab7ee4", "button_text": "white", "border": "#6272a4",
        "keyword": "#ff79c6", "string": "#f1fa8c", "comment": "#6272a4", "number": "#bd93f9"
    },
    "GitHub Dark": {
        "base": "#0d1117", "text": "#c9d1d9", "primary": "#238636", "secondary": "#161b22",
        "highlight": "#161b22", "title_bar": "#010409", "menu_hover": "#161b22",
        "button_hover": "#207030", "button_text": "white", "border": "#30363d",
        "keyword": "#ff7b72", "string": "#a5d6ff", "comment": "#8b949e", "number": "#79c0ff"
    },
    "GitHub Light": {
        "base": "#ffffff", "text": "#24292e", "primary": "#2ea44f", "secondary": "#f6f8fa",
        "highlight": "#f6f8fa", "title_bar": "#f6f8fa", "menu_hover": "#e1e4e8",
        "button_hover": "#299046", "button_text": "white", "border": "#d1d5da",
        "keyword": "#d73a49", "string": "#032f62", "comment": "#6a737d", "number": "#005cc5"
    },
    "One Dark": {
        "base": "#282c34", "text": "#abb2bf", "primary": "#61afef", "secondary": "#3a3f4b",
        "highlight": "#3a3f4b", "title_bar": "#21252b", "menu_hover": "#3a3f4b",
        "button_hover": "#529bda", "button_text": "white", "border": "#4b5263",
        "keyword": "#c678dd", "string": "#98c379", "comment": "#5c6370", "number": "#d19a66"
    },
    "One Light": {
        "base": "#fafafa", "text": "#383a42", "primary": "#4078f2", "secondary": "#eaeaeb",
        "highlight": "#eaeaeb", "title_bar": "#f0f0f0", "menu_hover": "#dcdfe4",
        "button_hover": "#3665ce", "button_text": "white", "border": "#d1d5da",
        "keyword": "#a626a4", "string": "#50a14f", "comment": "#a0a1a7", "number": "#d19a66"
    },
    "Nord": {
        "base": "#2e3440", "text": "#d8dee9", "primary": "#88c0d0", "secondary": "#3b4252",
        "highlight": "#3b4252", "title_bar": "#242933", "menu_hover": "#3b4252",
        "button_hover": "#79a9b8", "button_text": "#2e3440", "border": "#4c566a",
        "keyword": "#81a1c1", "string": "#a3be8c", "comment": "#4c566a", "number": "#b48ead"
    },
    "Gruvbox Dark": {
        "base": "#282828", "text": "#ebdbb2", "primary": "#fabd2f", "secondary": "#3c3836",
        "highlight": "#3c3836", "title_bar": "#1d2021", "menu_hover": "#3c3836",
        "button_hover": "#d8a329", "button_text": "#282828", "border": "#665c54",
        "keyword": "#fb4934", "string": "#b8bb26", "comment": "#928374", "number": "#d3869b"
    },
    "Gruvbox Light": {
        "base": "#fbf1c7", "text": "#3c3836", "primary": "#d65d0e", "secondary": "#ebdbb2",
        "highlight": "#ebdbb2", "title_bar": "#f2e5bc", "menu_hover": "#e0d1ac",
        "button_hover": "#b54c0b", "button_text": "white", "border": "#bdae93",
        "keyword": "#9d0006", "string": "#79740e", "comment": "#928374", "number": "#8f3f71"
    },
    "Cobalt": {
        "base": "#002240", "text": "#ffffff", "primary": "#ffc600", "secondary": "#003366",
        "highlight": "#003366", "title_bar": "#001a33", "menu_hover": "#003366",
        "button_hover": "#e6b300", "button_text": "#002240", "border": "#3b536d",
        "keyword": "#ff9d00", "string": "#3ad900", "comment": "#0088ff", "number": "#ff628c"
    },
    "Rainbow": {
        "base": "#000000", "text": "#e2a012", "primary": "#ff0000", "secondary": "#eef11a",
        "highlight": "#00ff00", "title_bar": "#000000", "menu_hover": "#3781b3",
        "button_hover": "#ff0000", "button_text": "white", "border": "#000000",
        "keyword": "#ff00ff", "string": "#821bc7", "comment": "#588849", "number": "#0000ff"
    }
}

QUICK_FIX_IMPORTS = {
    # Standard Library
    'os': {'module': 'os', 'type': 'direct'},
    'sys': {'module': 'sys', 'type': 'direct'},
    're': {'module': 're', 'type': 'direct'},
    'json': {'module': 'json', 'type': 'direct'},
    'datetime': {'module': 'datetime', 'type': 'direct'},
    'Path': {'module': 'pathlib', 'type': 'from'},
    # PyQt5
    'QApplication': {'module': 'PySide6.QtWidgets', 'type': 'from'},
    'QWidget': {'module': 'PySide6.QtWidgets', 'type': 'from'},
    'pyqtSignal': {'module': 'PySide6.QtCore', 'type': 'from'},
    'QThread': {'module': 'PySide6.QtCore', 'type': 'from'},
    'QObject': {'module': 'PySide6.QtCore', 'type': 'from'},
    # Pip-installable
    'requests': {'module': 'requests', 'type': 'direct', 'package_name': 'requests'},
    'numpy': {'module': 'numpy', 'type': 'direct', 'alias': 'np', 'package_name': 'numpy'},
    'pandas': {'module': 'pandas', 'type': 'direct', 'package_name': 'pandas'},
}

def generate_qss(theme_name):
    colors = THEME_PALETTES.get(theme_name, THEME_PALETTES["Dark"])
    return f"""
        QWidget {{ background-color: {colors['base']}; color: {colors['text']}; font-family: Segoe UI; font-size: 14px; }}
        #TerminalContainer {{ background-color: {colors['highlight']}; border: 1px solid {colors['border']}; border-radius: 4px; }}
        #TerminalOutput, #TerminalInput {{ background-color: transparent; border: none; }}
        QLineEdit, QTextEdit, QPlainTextEdit, QListWidget, QComboBox, QTreeView {{ background-color: {colors['secondary']}; border: 1px solid {colors['border']}; border-radius: 4px; padding: 5px; }}
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QTreeView:focus {{ border: 1px solid {colors['primary']}; }}
        QPushButton {{ background-color: {colors['primary']}; color: {colors['button_text']}; border: none; border-radius: 4px; padding: 8px 16px; }}
        QPushButton:hover {{ background-color: {colors['button_hover']}; }}
        #CopyButton {{ background-color: {colors['secondary']}; padding: 5px 10px; font-size: 12px; color: {colors['text']}; }}
        #CopyButton:hover {{ background-color: {colors['highlight']}; }}
        QListWidget::item:selected {{ background-color: {colors['primary']}; color: {colors['button_text']}; }}
        QComboBox QAbstractItemView {{ background-color: {colors['secondary']}; border: 1px solid {colors['border']}; selection-background-color: {colors['primary']}; }}
        QSplitter::handle {{ background-color: {colors['border']}; }} QSplitter::handle:vertical {{ height: 5px; }}
        QTreeView {{ background-color: {colors['base']}; border-right: 1px solid {colors['border']}; outline: 0; }}
        QTreeView::item:selected {{ background-color: {colors['primary']}; color: {colors['button_text']}; }}
        QHeaderView::section {{ background-color: {colors['title_bar']}; color: {colors['text']}; padding: 4px; border: 1px solid {colors['border']}; }}
        #OpenEditorsLabel {{ font-size: 11px; font-weight: bold; color: {colors['text']}; padding: 8px 4px 4px 4px; background-color: {colors['base']}; }}
        #OpenEditorsList {{ background-color: {colors['base']}; border: none; }}
        #CodeTabs::pane {{ border: 1px solid {colors['title_bar']}; border-top: none; }}
        #CodeTabs QTabBar::tab {{ background: {colors['title_bar']}; color: {colors['text']}; padding: 8px 15px; border: 1px solid {colors['title_bar']}; border-bottom: none; margin-right: 2px; }}
        #CodeTabs QTabBar::tab:selected {{ background: {colors['base']}; color: {colors['text']}; border-top: 2px solid {colors['primary']}; }}
        #CodeTabs QTabBar::tab:hover:!selected {{ background: {colors['highlight']}; }}
        #FindReplaceWidget {{ background-color: {colors['title_bar']}; border-bottom: 1px solid {colors['border']}; }}
        #FindReplaceWidget QLineEdit {{ background-color: {colors['secondary']}; }}
        QStatusBar {{ background-color: {colors['title_bar']}; color: {colors['text']}; }}
        #TitleBar {{ background-color: {colors['title_bar']}; height: 35px; }}
        #TitleBar QLabel {{ color: {colors['text']}; padding-left: 10px; font-weight: bold; }}
        #TitleBarMenuBar {{ background-color: transparent; }}
        #TitleBar QMenuBar::item {{ background-color: transparent; padding: 4px 8px; color: {colors['text']}; }}
        #TitleBar QMenuBar::item:selected {{ background-color: {colors['menu_hover']}; }}
        #BreadcrumbBar {{ padding: 4px 8px; background-color: {colors['base']}; border-bottom: 1px solid {colors['title_bar']}; }}
        #BreadcrumbBar QLabel {{ color: {colors['text']}; opacity: 0.7; background: transparent; }}
        #BreadcrumbBar QPushButton {{ background: transparent; border: none; color: {colors['text']}; opacity: 0.7; padding: 2px; }}
        #BreadcrumbBar QPushButton:hover {{ text-decoration: underline; color: {colors['primary']}; }}
        #CurrentFileCrumb {{ color: {colors['text']}; font-weight: bold; }}
        QMenu {{ background-color: {colors['secondary']}; border: 1px solid {colors['border']}; }}
        QMenu::item:selected {{ background-color: {colors['primary']}; color: {colors['button_text']}; }}
        #TabCloseButton {{ background: transparent; border: none; color: {colors['text']}; font-size: 14px; padding: 0 5px; border-radius: 4px; }}
        #TabCloseButton:hover {{ background: {colors['highlight']}; color: {colors['primary']}; }}
        #WindowControls QPushButton {{ background-color: transparent; border: none; width: 45px; height: 35px; padding: 0px; font-size: 16px; }}
        #WindowControls QPushButton:hover {{ background-color: {colors['menu_hover']}; }}
        #CloseButton:hover {{ background-color: #e81123; }}
    """
__version__ = "2.2.6"

class CustomTitleBar(QWidget):
    """A custom title bar with window controls and a menu."""
    def __init__(self, parent):
        super(CustomTitleBar, self).__init__(parent)
        self.parent = parent
        self.setObjectName("TitleBar")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 0, 0)
        self.layout.setSpacing(0)

        # App Icon
        self.icon_label = QLabel()
        self.layout.addWidget(self.icon_label)

        # Menu Bar
        self.menu_bar = QMenuBar()
        self.menu_bar.setObjectName("TitleBarMenuBar")
        self.layout.addWidget(self.menu_bar)

        # Title (will be centered in the remaining space)
        self.path_label = QLabel()
        self.path_label.setAlignment(Qt.AlignCenter)
        self.path_label.setObjectName("TitleBarPathLabel")
        self.layout.addWidget(self.path_label)
        self.layout.addStretch()

        # Window controls
        self.controls_widget = QWidget()
        self.controls_widget.setObjectName("WindowControls")
        self.controls_layout = QHBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(0)

        self.minimize_button = QPushButton("—"); self.restore_button = QPushButton("□"); self.close_button = QPushButton("✕")
        self.close_button.setObjectName("CloseButton")
        self.controls_layout.addWidget(self.minimize_button); self.controls_layout.addWidget(self.restore_button); self.controls_layout.addWidget(self.close_button)
        self.layout.addWidget(self.controls_widget)

        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.restore_button.clicked.connect(self.toggle_maximize_restore)
        self.close_button.clicked.connect(self.parent.close)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized(): self.parent.showNormal()
        else: self.parent.showMaximized()

    def update_restore_button_icon(self):
        if self.parent.isMaximized(): self.restore_button.setText("⧉")
        else: self.restore_button.setText("□")

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton: self.toggle_maximize_restore()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.drag_pos = event.globalPos()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.parent.isMaximized():
            self.parent.move(self.parent.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
class SettingsDialog(QDialog):
    """A dialog for configuring application settings."""
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(300)
        self.layout = QVBoxLayout(self)

        # Helper to create a setting row
        def create_setting_row(label_text, widget):
            layout = QHBoxLayout()
            layout.addWidget(QLabel(label_text))
            layout.addStretch()
            layout.addWidget(widget)
            self.layout.addLayout(layout)

        # Font Size
        self.font_size_spinbox = QSpinBox(); self.font_size_spinbox.setRange(8, 30)
        self.font_size_spinbox.setValue(current_settings.get('font_size', 14))
        create_setting_row("Editor Font Size:", self.font_size_spinbox)

        # Checkboxes
        self.highlight_line_check = QCheckBox(); self.highlight_line_check.setChecked(current_settings.get('highlight_current_line', True))
        create_setting_row("Highlight Current Line:", self.highlight_line_check)
        self.rounded_highlight_check = QCheckBox(); self.rounded_highlight_check.setChecked(current_settings.get('rounded_line_highlight', False))
        create_setting_row("Use Rounded Line Highlight:", self.rounded_highlight_check)
        self.show_minimap_check = QCheckBox(); self.show_minimap_check.setChecked(current_settings.get('show_minimap', True))
        create_setting_row("Show Code Minimap:", self.show_minimap_check)
        self.visible_whitespace_check = QCheckBox(); self.visible_whitespace_check.setChecked(current_settings.get('show_visible_whitespace', False))
        create_setting_row("Show Visible Whitespace:", self.visible_whitespace_check)
        self.format_on_save_check = QCheckBox(); self.format_on_save_check.setChecked(current_settings.get('format_on_save', False))
        create_setting_row("Format on Save (Python):", self.format_on_save_check)
        self.auto_save_check = QCheckBox(); self.auto_save_check.setChecked(current_settings.get('auto_save_on_focus_loss', False))
        create_setting_row("Auto-Save on Focus Loss:", self.auto_save_check)

        # Line Endings
        self.line_ending_combo = QComboBox()
        self.line_ending_combo.addItems(["LF", "CRLF"])
        self.line_ending_combo.setCurrentText(current_settings.get('default_line_ending', 'LF'))
        create_setting_row("Default Line Ending:", self.line_ending_combo)

        # Linter Debounce
        self.linter_debounce_spinbox = QSpinBox()
        self.linter_debounce_spinbox.setRange(100, 5000)
        self.linter_debounce_spinbox.setSingleStep(50)
        self.linter_debounce_spinbox.setSuffix(" ms")
        self.linter_debounce_spinbox.setValue(current_settings.get('linter_debounce_time', 750))
        create_setting_row("Linter Debounce Time:", self.linter_debounce_spinbox)
        self.layout.addStretch()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_settings(self):
        """Returns the configured settings as a dictionary."""
        return {
            'font_size': self.font_size_spinbox.value(),
            'highlight_current_line': self.highlight_line_check.isChecked(),
            'rounded_line_highlight': self.rounded_highlight_check.isChecked(),
            'show_minimap': self.show_minimap_check.isChecked(),
            'show_visible_whitespace': self.visible_whitespace_check.isChecked(),
            'format_on_save': self.format_on_save_check.isChecked(),
            'auto_save_on_focus_loss': self.auto_save_check.isChecked(),
            'default_line_ending': self.line_ending_combo.currentText(),
            'linter_debounce_time': self.linter_debounce_spinbox.value(),
        }

class ManageProfilesDialog(QDialog):
    """A dialog to rename and delete user profiles."""
    def __init__(self, profiles_dir, active_profile_name, parent=None):
        super().__init__(parent)
        self.profiles_dir = profiles_dir
        self.active_profile_name = active_profile_name
        self.parent_app = parent

        self.setWindowTitle("Manage Profiles")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        self.profile_list = QListWidget()
        self.profile_list.itemSelectionChanged.connect(self.update_button_states)
        layout.addWidget(self.profile_list)

        button_layout = QHBoxLayout()
        self.import_button = QPushButton("Import...")
        self.import_button.clicked.connect(self.import_profile)
        self.export_button = QPushButton("Export...")
        self.export_button.clicked.connect(self.export_profile)
        self.duplicate_button = QPushButton("Duplicate")
        self.duplicate_button.clicked.connect(self.duplicate_profile)
        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.rename_profile)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_profile)
        button_layout.addStretch()
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.duplicate_button)
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.close_button = QDialogButtonBox(QDialogButtonBox.Close)
        self.close_button.rejected.connect(self.reject)
        layout.addWidget(self.close_button)

        self.populate_profiles()
        self.update_button_states()

    def populate_profiles(self):
        self.profile_list.clear()
        for f in sorted(self.profiles_dir.glob("*.json")):
            profile_name = f.stem
            item = QListWidgetItem(profile_name)
            if profile_name == 'default':
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setForeground(QColor("gray"))
            if profile_name == self.active_profile_name:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.profile_list.addItem(item)

    def update_button_states(self):
        selected_items = self.profile_list.selectedItems()
        is_selection = bool(selected_items)
        self.export_button.setEnabled(is_selection)
        self.duplicate_button.setEnabled(is_selection)
        is_deletable = is_selection and selected_items[0].text() != 'default'
        self.rename_button.setEnabled(is_deletable)
        self.delete_button.setEnabled(is_deletable)

    def rename_profile(self):
        selected_item = self.profile_list.currentItem()
        if not selected_item: return

        old_name = selected_item.text()
        new_name, ok = QInputDialog.getText(self, "Rename Profile", "Enter new name:", text=old_name)

        if ok and new_name and new_name.strip() and new_name != old_name:
            if (self.profiles_dir / f"{new_name}.json").exists():
                QMessageBox.warning(self, "Error", "A profile with that name already exists.")
                return

            old_path = self.profiles_dir / f"{old_name}.json"
            new_path = self.profiles_dir / f"{new_name}.json"
            old_path.rename(new_path)

            if self.active_profile_name == old_name:
                self.active_profile_name = new_name
                self.parent_app._set_active_profile(new_name)

            self.populate_profiles()
            self.parent_app._update_profiles_menu()

    def delete_profile(self):
        selected_item = self.profile_list.currentItem()
        if not selected_item: return

        profile_to_delete = selected_item.text()
        reply = QMessageBox.question(self, "Delete Profile", f"Are you sure you want to delete the profile '{profile_to_delete}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            (self.profiles_dir / f"{profile_to_delete}.json").unlink()

            if self.active_profile_name == profile_to_delete:
                self.active_profile_name = 'default'
                self.parent_app._switch_profile('default')

            self.populate_profiles()
            self.parent_app._update_profiles_menu()

    
    def duplicate_profile(self):
        selected_item = self.profile_list.currentItem()
        if not selected_item: return

        source_name = selected_item.text()
        new_name_suggestion = f"{source_name}_copy"
        
        new_name, ok = QInputDialog.getText(self, "Duplicate Profile", "Enter name for new profile:", text=new_name_suggestion)

        if ok and new_name and new_name.strip():
            if (self.profiles_dir / f"{new_name}.json").exists():
                QMessageBox.warning(self, "Error", "A profile with that name already exists.")
                return

            source_path = self.profiles_dir / f"{source_name}.json"
            new_path = self.profiles_dir / f"{new_name}.json"
            
            try:
                shutil.copy(source_path, new_path)
                self.populate_profiles()
                self.parent_app._update_profiles_menu()
            except IOError as e:
                QMessageBox.critical(self, "Error", f"Could not duplicate profile: {e}")

    def import_profile(self):
        """Imports a profile from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Profile", "", "JSON Files (*.json)")
        if not file_path:
            return

        source_path = Path(file_path)
        profile_name = source_path.stem
        dest_path = self.profiles_dir / source_path.name

        if dest_path.exists():
            reply = QMessageBox.question(self, "Profile Exists", f"A profile named '{profile_name}' already exists. Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        try:
            shutil.copy(source_path, dest_path)
            QMessageBox.information(self, "Success", f"Profile '{profile_name}' imported successfully.")
            self.populate_profiles()
            self.parent_app._update_profiles_menu()
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Could not import profile: {e}")

    def export_profile(self):
        """Exports the selected profile to a JSON file."""
        selected_item = self.profile_list.currentItem()
        if not selected_item: return

        profile_name = selected_item.text()
        source_path = self.profiles_dir / f"{profile_name}.json"

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Profile", f"{profile_name}.json", "JSON Files (*.json)")
        if not file_path: return
        
        try:
            shutil.copy(source_path, file_path)
            QMessageBox.information(self, "Success", f"Profile '{profile_name}' exported successfully to {file_path}.")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Could not export profile: {e}")

class SourceControlWidget(QWidget):
    """A sidebar widget to display Git status and perform actions."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("SourceControlWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Commit area
        self.commit_message = QTextEdit()
        self.commit_message.setPlaceholderText("Commit message")
        self.commit_message.setFixedHeight(80)
        commit_button = QPushButton("Commit")
        layout.addWidget(self.commit_message)
        layout.addWidget(commit_button)

        # Changes lists
        self.staged_label = QLabel("Staged Changes (0)")
        self.staged_list = QListWidget()
        self.changes_label = QLabel("Changes (0)")
        self.changes_list = QListWidget()

        layout.addWidget(self.staged_label)
        layout.addWidget(self.staged_list)
        layout.addWidget(self.changes_label)
        layout.addWidget(self.changes_list)

        # Connections
        commit_button.clicked.connect(self.commit_changes)
        self.staged_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.staged_list.customContextMenuRequested.connect(lambda p: self.show_context_menu(p, self.staged_list, is_staged=True))
        self.changes_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.changes_list.customContextMenuRequested.connect(lambda p: self.show_context_menu(p, self.changes_list, is_staged=False))

    def refresh_status(self):
        self.staged_list.clear(); self.changes_list.clear()
        result = self.parent_app._run_git_command(['git', 'status', '--porcelain'])
        if not result or not result.stdout: return
        for line in result.stdout.strip().splitlines():
            status, file_path = line[:2].strip(), line[3:]
            item = QListWidgetItem(f"{status} {file_path}"); item.setData(Qt.UserRole, file_path)
            if status in ('M', 'A', 'D', 'R'): self.staged_list.addItem(item)
            else: self.changes_list.addItem(item)
        self.staged_label.setText(f"Staged Changes ({self.staged_list.count()})")
        self.changes_label.setText(f"Changes ({self.changes_list.count()})")

    def show_context_menu(self, point, list_widget, is_staged):
        item = list_widget.itemAt(point);
        if not item: return
        menu = QMenu()
        action_text = "Unstage File" if is_staged else "Stage File"
        stage_action = menu.addAction(action_text)
        diff_action = menu.addAction("View Changes")
        action = menu.exec_(list_widget.mapToGlobal(point))
        if action == stage_action:
            cmd = ['git', 'reset', 'HEAD', '--'] if is_staged else ['git', 'add']
            self.parent_app._run_git_command(cmd + [item.data(Qt.UserRole)])
            self.refresh_status()
        elif action == diff_action:
            self.parent_app._show_diff_view(item.data(Qt.UserRole))

    def commit_changes(self):
        message = self.commit_message.toPlainText().strip()
        if not message: QMessageBox.warning(self, "Commit Error", "Commit message cannot be empty."); return
        if self.staged_list.count() == 0: QMessageBox.warning(self, "Commit Error", "There are no staged changes to commit."); return
        result = self.parent_app._run_git_command(['git', 'commit', '-m', message])
        if result and result.returncode == 0: self.parent_app.statusBar().showMessage("Commit successful.", 3000); self.commit_message.clear(); self.refresh_status()
        elif result: QMessageBox.critical(self, "Commit Failed", f"Error committing changes:\n\n{result.stderr}")

class PowerShellWorker(QObject):
    """Reads output from a process in a separate thread."""

    def __init__(self, process_stream, output_queue):
        super().__init__()
        self.stream = process_stream
        self.queue = output_queue

    def run(self):
        """Read lines from the stream and put them in the queue."""
        try:
            for line in iter(self.stream.readline, ''):
                self.queue.put(line)
        finally:
            self.stream.close()

class PythonHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for Python code.""" # Fixed class definition
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        theme_name = QApplication.instance().property("theme_name") or "Dark"
        colors = THEME_PALETTES.get(theme_name, THEME_PALETTES["Dark"])

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(colors['keyword']))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
            'import', 'from', 'in', 'try', 'except', 'finally', 'with', 'as',
            'True', 'False', 'None', 'and', 'or', 'not', 'is', 'lambda'
        ]
        self.highlighting_rules = [(r'\b' + kw + r'\b', keyword_format) for kw in keywords]

        # self
        self_format = QTextCharFormat()
        self_format.setForeground(QColor("#9CDCFE")) # Light Blue
        self.highlighting_rules.append((r'\bself\b', self_format))

        # Strings (single and double quoted)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(colors['string']))
        self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
        self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(colors['comment']))
        self.highlighting_rules.append((r'#[^\n]*', comment_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(colors['number']))
        self.highlighting_rules.append((r'\b[0-9]+\b', number_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class JavaScriptHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for JavaScript and TypeScript code."""
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6")) # Blue
        keywords = [
            'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
            'default', 'delete', 'do', 'else', 'export', 'extends', 'finally',
            'for', 'function', 'if', 'import', 'in', 'instanceof', 'new',
            'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof',
            'var', 'void', 'while', 'with', 'yield', 'let', 'static',
            'async', 'await', 'public', 'private', 'protected', 'interface', 'implements'
        ]
        self.highlighting_rules = [(r'\b' + kw + r'\b', keyword_format) for kw in keywords]

        # Literals
        literal_format = QTextCharFormat()
        literal_format.setForeground(QColor("#569cd6")) # Blue
        self.highlighting_rules.extend([
            (r'\btrue\b', literal_format),
            (r'\bfalse\b', literal_format),
            (r'\bnull\b', literal_format),
            (r'\bundefined\b', literal_format),
        ])

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178")) # Orange
        self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
        self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))
        self.highlighting_rules.append((r"`[^`\\]*(\\.[^`\\]*)*`", string_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8")) # Light Green
        self.highlighting_rules.append((r'\b[0-9]+(\.[0-9]+)?\b', number_format))

        # Function names
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA")) # Yellow
        self.highlighting_rules.append((r'\b[A-Za-z0-9_]+(?=\s*\()', function_format))

        # Single-line comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955")) # Green
        self.highlighting_rules.append((r'//[^\n]*', comment_format))

        # Multi-line comments
        self.multi_line_comment_format = QTextCharFormat()
        self.multi_line_comment_format.setForeground(QColor("#6A9955"))
        self.comment_start_expression = QRegularExpression(r'/\*')
        self.comment_end_expression = QRegularExpression(r'\*/')

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.match(text).capturedStart()

        while start_index >= 0:
            end_match = self.comment_end_expression.match(text, start_index)
            end_index = end_match.capturedStart()
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + end_match.capturedLength()
            self.setFormat(start_index, comment_length, self.multi_line_comment_format)
            start_index = self.comment_start_expression.match(text, start_index + comment_length).capturedStart()

class CppHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for C-family languages (C++, C#, Java, Rust)."""
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6")) # Blue
        keywords = [
            'char', 'class', 'const', 'double', 'enum', 'explicit', 'export',
            'extern', 'float', 'friend', 'inline', 'int', 'long', 'mutable',
            'namespace', 'operator', 'private', 'protected', 'public',
            'short', 'signed', 'static', 'struct', 'template', 'typedef',
            'typename', 'union', 'unsigned', 'using', 'virtual', 'void',
            'volatile', 'wchar_t', 'bool', 'if', 'else', 'for', 'while', 'do',
            'switch', 'case', 'default', 'try', 'catch', 'throw', 'return',
            'new', 'delete', 'this', 'nullptr', 'true', 'false',
            # Rust keywords
            'fn', 'let', 'mut', 'match', 'use', 'mod', 'pub', 'crate', 'impl', 'trait'
        ]
        self.highlighting_rules = [(r'\b' + kw + r'\b', keyword_format) for kw in keywords]

        # Preprocessor
        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#c586c0")) # Magenta
        self.highlighting_rules.append((r'^\s*#\w+', preprocessor_format))

        # Other rules are identical to JavaScript, so we can reuse its implementation
        js_highlighter = JavaScriptHighlighter()
        self.highlighting_rules.extend(js_highlighter.highlighting_rules[len(js_highlighter.highlighting_rules)-6:]) # Reuse strings, numbers, functions, comments
        self.multi_line_comment_format = js_highlighter.multi_line_comment_format
        self.comment_start_expression = js_highlighter.comment_start_expression
        self.comment_end_expression = js_highlighter.comment_end_expression

    def highlightBlock(self, text):
    # Apply all highlighting rules (C++ rules + reused JS rules)
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.match(text).capturedStart()

        while start_index >= 0: # Fixed broken loop
            end_match = self.comment_end_expression.match(text, start_index)
            end_index = end_match.capturedStart()
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + end_match.capturedLength()
            self.setFormat(start_index, comment_length, self.multi_line_comment_format)
            start_index = self.comment_start_expression.match(text, start_index + comment_length).capturedStart()

class HtmlHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for HTML."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Tags
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#569cd6")) # Blue
        self.highlighting_rules.append((r'</?\w+', tag_format))

        # Attributes
        attribute_format = QTextCharFormat()
        attribute_format.setForeground(QColor("#9CDCFE")) # Light Blue
        self.highlighting_rules.append((r'\b\w+(?=\s*=)', attribute_format))

        # Values
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#ce9178")) # Orange
        self.highlighting_rules.append((r'"[^"]*"', value_format))
        self.highlighting_rules.append((r"'[^']*'", value_format))

        # Comments
        self.multi_line_comment_format = QTextCharFormat()
        self.multi_line_comment_format.setForeground(QColor("#6A9955")) # Green
        self.comment_start_expression = QRegularExpression(r'<!--')
        self.comment_end_expression = QRegularExpression(r'-->')

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        # Multi-line comments
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_start_expression.match(text).capturedStart()
        while start_index >= 0: # Fixed broken loop
            end_match = self.comment_end_expression.match(text, start_index)
            end_index = end_match.capturedStart()
            comment_length = len(text) - start_index if end_index == -1 else end_index - start_index + end_match.capturedLength()
            self.setFormat(start_index, comment_length, self.multi_line_comment_format)
            if end_index == -1:
                self.setCurrentBlockState(1)
            start_index = self.comment_start_expression.match(text, start_index + comment_length).capturedStart()

class CssHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for CSS."""
    def __init__(self, parent=None):
        super().__init__(parent)
        rules = []
        # Selectors (tags, classes, ids)
        rules.append((r'^\s*[\w\-\#\.\*:]+[\w\-\s\.\#\:\,>~\+\[\]\=\"\'\^\|\$\*]+(?=\s*\{)', QColor("#d7ba7d"))) # Yellow-ish
        # Properties
        rules.append((r'\b[\w\-]+\s*(?=:)', QColor("#9CDCFE"))) # Light Blue
        # Values (includes colors, units, strings)
        rules.append((r':\s*[^;\}]+', QColor("#ce9178"))) # Orange
        # Comments
        rules.append((r'/\*.*\*/', QColor("#6A9955"))) # Green
        self.highlighting_rules = [(p, QTextCharFormat(c)) for p, c in rules]

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class NebulaHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for the Nebula language."""
    def __init__(self, parent=None):
        super().__init__(parent)
        theme_name = QApplication.instance().property("theme_name") or "Dark"
        colors = THEME_PALETTES.get(theme_name, THEME_PALETTES["Dark"])
        rules = []
        # Keywords, UI Components, and special constructs
        rules.append((r'\b(import from|let|static|NJson|VWindow|VLayout|VLabel|VButton|Init)\b', QColor(colors['keyword'])))
        # Special constructs
        rules.append((r'&__app__\s*\(\s*start\s*\)', QColor("#c586c0"))) # Magenta
        # Comments, Strings, Numbers
        rules.append((r'#.*', QColor(colors['comment'])))
        rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', QColor(colors['string'])))
        rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", QColor(colors['string'])))
        rules.append((r'\b[0-9]+\b', QColor(colors['number'])))

        self.highlighting_rules = [(p, QTextCharFormat(f)) for p, f in rules]

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            it = QRegularExpression(pattern).globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class NebulaPreviewWidget(QWidget):
    """A widget to host the live preview of a Nebula UI."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.current_preview_widget = None
        self.placeholder_label = QLabel("Nebula UI Preview will appear here.")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.placeholder_label)

    def set_preview_widget(self, widget):
        """Clears the old preview and sets the new one."""
        if self.current_preview_widget:
            self.layout.removeWidget(self.current_preview_widget)
            self.current_preview_widget.deleteLater()
            self.current_preview_widget = None
        
        if self.placeholder_label:
            self.placeholder_label.hide()

        if widget:
            self.current_preview_widget = widget
            self.layout.addWidget(self.current_preview_widget)
        else:
            self.placeholder_label.show()

    def show_error(self, message):
        """Displays an error message instead of a preview."""
        error_label = QLabel(f"Preview Error:\n{message}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: #f44747;")
        self.set_preview_widget(error_label)

class FindInFilesWorker(QObject):
    """Worker thread for searching files."""
    match_found = pyqtSignal(str, int, str)
    finished = pyqtSignal()

    def __init__(self, search_text, directory, whole_word=False, case_sensitive=False):
        super().__init__()
        self.search_text = search_text
        self.directory = directory
        self.is_running = True
        self.case_sensitive = case_sensitive
        self.whole_word = whole_word

    def run(self):
        ignore_dirs = {'.git', '.venv', 'node_modules', '__pycache__'}
        ignore_exts = {'.pyc', '.dll', '.exe', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.db', '.zip', '.gz'}

        for root, dirs, files in os.walk(self.directory):
            if not self.is_running: break
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for filename in files:
                if not self.is_running: break
                if Path(filename).suffix in ignore_exts: continue
                
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            match = False
                            if self.whole_word:
                                flags = re.IGNORECASE if not self.case_sensitive else 0
                                if re.search(r'\b' + re.escape(self.search_text) + r'\b', line, flags):
                                    match = True
                            else:
                                if self.case_sensitive:
                                    if self.search_text in line:
                                        match = True
                                else:
                                    if self.search_text.lower() in line.lower():
                                        match = True
                            if match:
                                self.match_found.emit(file_path, line_num, line.strip())
                except Exception:
                    continue # Skip files we can't read
        self.finished.emit()

    def stop(self):
        self.is_running = False

class FindInFilesDialog(QDialog):
    """Dialog for finding text in files across the project."""
    file_open_requested = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find in Files")
        self.setMinimumSize(800, 500)
        self.layout = QVBoxLayout(self)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to find in files...")
        self.case_sensitive_check = QCheckBox("Case Sensitive")
        self.whole_word_check = QCheckBox("Whole Word")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.case_sensitive_check)
        search_layout.addWidget(self.whole_word_check)
        self.layout.addLayout(search_layout)

        self.status_label = QLabel("Ready to search.")
        self.layout.addWidget(self.status_label)

        self.results_tree = QTreeView()
        self.results_tree.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.results_tree.setModel(self.model)
        self.layout.addWidget(self.results_tree)

        # Add replace widgets
        replace_layout = QHBoxLayout()
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")
        self.replace_all_button = QPushButton("Replace All")
        replace_layout.addWidget(self.replace_input)
        replace_layout.addWidget(self.replace_all_button)
        self.layout.addLayout(replace_layout)

        self.search_worker = None
        self.search_thread = None
        self.file_items = {}

        self.search_input.returnPressed.connect(self.start_search)
        self.results_tree.doubleClicked.connect(self.on_result_activated)

        self.replace_all_button.clicked.connect(self.replace_all)

    def start_search(self, whole_word=None):
        if self.search_thread and self.search_thread.isRunning():
            self.search_worker.stop()
            self.search_thread.quit()
            self.search_thread.wait()

        search_text = self.search_input.text()
        if not search_text: return

        self.model.clear()
        self.file_items.clear()
        is_case_sensitive = self.case_sensitive_check.isChecked()
        is_whole_word = self.whole_word_check.isChecked() if whole_word is None else whole_word
        self.status_label.setText(f"Searching for '{search_text}'...")

        self.search_thread = QThread()
        self.search_worker = FindInFilesWorker(search_text, os.getcwd(), 
                                             whole_word=is_whole_word, case_sensitive=is_case_sensitive)
        self.search_worker.moveToThread(self.search_thread)

        self.search_worker.match_found.connect(self.add_match)
        self.search_worker.finished.connect(self.search_finished)
        self.search_thread.started.connect(self.search_worker.run)
        self.search_thread.start()

    def add_match(self, file_path, line_num, line_text):
        if file_path not in self.file_items:
            file_item = QStandardItem(f"{Path(file_path).name} ({Path(file_path).parent})")
            file_item.setData(file_path, Qt.UserRole)
            file_item.setEditable(False)
            self.model.appendRow(file_item)
            self.file_items[file_path] = file_item
        
        parent_item = self.file_items[file_path]
        result_item = QStandardItem(f"  {line_num}: {line_text}")
        result_item.setData(line_num, Qt.UserRole)
        result_item.setEditable(False)
        parent_item.appendRow(result_item)
        self.results_tree.expand(parent_item.index())

    def search_finished(self):
        self.status_label.setText(f"Search finished. Found {self.model.rowCount()} files with matches.")
        if self.search_thread:
            self.search_thread.quit()
            self.search_thread.wait()
            self.search_worker = None
            self.search_thread = None

    def on_result_activated(self, index):
        item = self.model.itemFromIndex(index)
        if not item or not item.parent(): return

        line_num = item.data(Qt.UserRole)
        file_path = item.parent().data(Qt.UserRole)
        self.file_open_requested.emit(file_path, line_num)
        self.accept()

    def replace_all(self):
        """Handles the 'Replace All' button click."""
        search_text = self.search_input.text()
        replace_text = self.replace_input.text()

        if not search_text or not self.file_items:
            QMessageBox.warning(self, "Replace All", "Please perform a search first to identify files for replacement.")
            return

        # Use the model to get the list of files found
        files_to_modify = list(self.file_items.keys())

        reply = QMessageBox.question(self, "Confirm Replace",
                                     f"Are you sure you want to replace all occurrences of '{search_text}' with '{replace_text}' in {len(files_to_modify)} files?\n\nThis action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            replaced_count = 0
            for file_path in files_to_modify:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Only proceed if the search text is actually in the content
                    if search_text in content:
                        new_content = content.replace(search_text, replace_text)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        replaced_count += 1
                        # Reload the file if it's open in a tab
                        if self.parent():
                            self.parent()._reload_file_if_open(file_path)

                except Exception as e:
                    # Optionally, collect and show errors at the end
                    print(f"Could not replace in {file_path}: {e}")
            
            QMessageBox.information(self, "Replace Complete", f"Replaced content in {replaced_count} files.")
            self.accept() # Close dialog after replacement

    def closeEvent(self, event):
        if self.search_worker:
            self.search_worker.stop()
            if self.search_thread and self.search_thread.isRunning():
                self.search_thread.quit()
                self.search_thread.wait()
        super().closeEvent(event)

class GoToSymbolDialog(QDialog):
    """A dialog to list and jump to symbols (functions/classes) in a file."""
    def __init__(self, symbols, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Go to Symbol")
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout(self)
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter symbols...")
        self.layout.addWidget(self.filter_input)

        self.list_widget = QListWidget()
        for symbol_name, line_number in symbols:
            item = QListWidgetItem(f"{symbol_name} (line {line_number + 1})")
            item.setData(Qt.UserRole, line_number)
            self.list_widget.addItem(item)
        self.layout.addWidget(self.list_widget)

        self.selected_line = -1

        # Connections
        self.filter_input.textChanged.connect(self.filter_symbols)
        self.list_widget.itemDoubleClicked.connect(self.accept_selection)

    def filter_symbols(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def accept_selection(self, item):
        self.selected_line = item.data(Qt.UserRole)
        self.accept()

class PeekView(QPlainTextEdit):
    """A frameless popup widget to show a peek of a definition."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set flags to make it a frameless popup that disappears when focus is lost
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.StrongFocus) # Needed to receive focusOutEvent

        # Basic styling
        is_dark = self.palette().window().color().lightness() < 128
        bg_color = "#3c3f41" if is_dark else "#ffffff"
        border_color = "#555555" if is_dark else "#cccccc"
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                border: 1px solid {border_color};
                background-color: {bg_color};
            }}
        """)

    def focusOutEvent(self, event):
        """Close the popup when it loses focus."""
        self.close()
        super().focusOutEvent(event)

class DiffViewDialog(QDialog):
    """A dialog to display a colored diff of file changes."""
    def __init__(self, diff_text, file_name, file_path, parent=None, show_git_buttons=True):
        super().__init__(parent)
        self.parent_app = parent
        self.file_path = file_path
        self.setWindowTitle(f"Changes for {file_name}")
        self.setMinimumSize(900, 600)

        self.layout = QVBoxLayout(self)

        if show_git_buttons:
            self.stage_button = QPushButton("Stage File")
            self.revert_button = QPushButton("Revert Changes")
            self.stage_button.clicked.connect(self.stage_file)
            self.revert_button.clicked.connect(self.revert_changes)
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(self.revert_button)
            button_layout.addWidget(self.stage_button)
            self.layout.addLayout(button_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Fira Code", 12))
        self.layout.addWidget(self.text_edit)

        html = self._format_diff_as_html(diff_text)
        self.text_edit.setHtml(html)

    def stage_file(self):
        """Stages the current file using Git."""
        result = self.parent_app._run_git_command(['git', 'add', self.file_path])
        if result and result.returncode == 0:
            QMessageBox.information(self, "Success", f"Staged {Path(self.file_path).name}")
            self.parent_app._update_git_status()
            self.accept() # Close dialog
        elif result: QMessageBox.critical(self, "Stage Failed", f"Error staging file:\n\n{result.stderr}")

    def revert_changes(self):
        """Reverts the changes for the current file."""
        reply = QMessageBox.question(self, "Confirm Revert",
                                     f"Are you sure you want to revert all changes for '{Path(self.file_path).name}'?\n\nThis action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = self.parent_app._run_git_command(['git', 'checkout', '--', self.file_path])
            if result and result.returncode == 0:
                QMessageBox.information(self, "Success", f"Reverted changes for {Path(self.file_path).name}")
                self.parent_app._update_git_status()
                self.parent_app._reload_file_if_open(self.file_path) # Reload the file in the editor
                self.accept() # Close dialog
        elif result: QMessageBox.critical(self, "Stage Failed", f"Error staging file:\n\n{result.stderr}")

    def _format_diff_as_html(self, diff_text):
        """Converts standard diff output to styled HTML."""
        html_lines = []
        # Use palette to check if we are in dark or light mode
        is_dark_theme = self.palette().window().color().lightness() < 128
        
        add_color = "#28a745" if is_dark_theme else "#22863a"
        del_color = "#d73a49" if is_dark_theme else "#cb2431"
        info_color = "#58a6ff" if is_dark_theme else "#005cc5"
        
        for line in diff_text.splitlines():
            line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if line.startswith('+'):
                html_lines.append(f'<div style="background-color: rgba(40, 167, 69, 0.2); color: {add_color};">{line}</div>')
            elif line.startswith('-'):
                html_lines.append(f'<div style="background-color: rgba(215, 58, 73, 0.2); color: {del_color};">{line}</div>')
            elif line.startswith('@@'):
                html_lines.append(f'<div style="color: {info_color};">{line}</div>')
            else:
                html_lines.append(f'<div>{line}</div>')
        
        return f"""<pre style="font-family: 'Fira Code', 'Consolas', 'Courier New'; white-space: pre-wrap;">
                   {''.join(html_lines)}
                   </pre>"""

class GitLogDialog(QDialog):
    """A dialog to display the Git commit history."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Git Log")
        self.setMinimumSize(900, 600)

        self.layout = QVBoxLayout(self)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter commits by message, author, or hash...")
        self.layout.addWidget(self.search_input)

        splitter = QSplitter(Qt.Vertical)

        self.commit_list = QListWidget()
        self.commit_list.setFont(QFont("Fira Code", 10))
        self.commit_list.setContextMenuPolicy(Qt.CustomContextMenu)
        splitter.addWidget(self.commit_list)

        self.commit_details = QTextEdit()
        self.commit_details.setReadOnly(True)
        self.commit_details.setFont(QFont("Fira Code", 10))
        splitter.addWidget(self.commit_details)
        
        splitter.setSizes([300, 300])
        self.layout.addWidget(splitter)

        self.populate_log()
        self.commit_list.currentItemChanged.connect(self.show_commit_details)
        self.commit_list.customContextMenuRequested.connect(self.show_context_menu)
        self.search_input.textChanged.connect(self.filter_log)

    def filter_log(self, text):
        """Hides or shows log items based on the filter text."""
        for i in range(self.commit_list.count()):
            item = self.commit_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def show_context_menu(self, point):
        """Shows a context menu for a commit item."""
        item = self.commit_list.itemAt(point)
        if not item: return

        commit_hash = item.data(Qt.UserRole)
        if not commit_hash: return

        menu = QMenu()
        cherry_pick_action = menu.addAction("Cherry-Pick this commit")
        revert_action = menu.addAction("Revert this commit")
        create_branch_action = menu.addAction("Create Branch from this commit")
        
        action = menu.exec_(self.commit_list.mapToGlobal(point))

        if action == cherry_pick_action:
            self.parent_app._git_cherry_pick(commit_hash)
            self.close()
        elif action == revert_action:
            self.parent_app._git_revert(commit_hash)
            self.close()
        elif action == create_branch_action:
            self.parent_app._git_create_branch_from_commit(commit_hash)
            self.close()

    def populate_log(self):
        self.commit_list.clear()
        # Format: FullHash|ShortHash|Author|Date|Subject
        result = self.parent_app._run_git_command(['git', 'log', '--pretty=format:%H|%h|%an|%ar|%s', '-n', '200'])
        if not result or not result.stdout:
            self.commit_list.addItem("Could not load commit history.")
            return
        
        for line in result.stdout.strip().splitlines():
            parts = line.split('|', 4)
            item = QListWidgetItem(f"{parts[1]} - {parts[4]} ({parts[2]}, {parts[3]})")
            item.setData(Qt.UserRole, parts[0]) # Store full hash
            self.commit_list.addItem(item)

    def show_commit_details(self, current, previous):
        if not current:
            self.commit_details.clear()
            return
        
        commit_hash = current.data(Qt.UserRole)
        result = self.parent_app._run_git_command(['git', 'show', '--pretty=fuller', '--stat', commit_hash])
        if result and result.stdout:
            self.commit_details.setPlainText(result.stdout)
        else:
            self.commit_details.setPlainText(f"Could not load details for commit {commit_hash[:7]}")

class CommandPalette(QDialog):
    """A searchable dialog to access all application actions."""
    def __init__(self, actions, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setMinimumWidth(600)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Type a command...")
        self.layout.addWidget(self.filter_input)
        
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        self.actions = actions
        self.populate_list()
        
        self.filter_input.textChanged.connect(self.filter_list)
        self.filter_input.returnPressed.connect(self.execute_selection)
        self.list_widget.itemActivated.connect(self.execute_selection)
        
        # Center on parent
        if parent:
            geo = parent.frameGeometry()
            center = geo.center()
            self.move(center.x() - self.width() // 2, center.y() - self.height() // 2)

    def populate_list(self):
        self.list_widget.clear()
        for action in self.actions:
            shortcut = action.shortcut().toString()
            text = action.text().replace('&', '')
            display_text = f"{text}  ({shortcut})" if shortcut else text
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, action)
            self.list_widget.addItem(item)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def filter_list(self, text):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def execute_selection(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            # If nothing is selected, try the first visible item
            for i in range(self.list_widget.count()):
                if not self.list_widget.item(i).isHidden():
                    selected_items = [self.list_widget.item(i)]
                    break
        
        if selected_items:
            action = selected_items[0].data(Qt.UserRole)
            action.trigger()
            self.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() in (Qt.Key_Up, Qt.Key_Down):
            self.list_widget.keyPressEvent(event)
        else:
            self.filter_input.setFocus()
            self.filter_input.keyPressEvent(event)

class GitBranchDialog(QDialog):
    """A dialog to manage Git branches."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Manage Git Branches")
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        button_layout = QHBoxLayout()
        self.checkout_button = QPushButton("Checkout")
        self.new_branch_button = QPushButton("New Branch...")
        self.delete_branch_button = QPushButton("Delete Branch")
        
        button_layout.addWidget(self.checkout_button)
        button_layout.addWidget(self.new_branch_button)
        button_layout.addStretch()
        button_layout.addWidget(self.delete_branch_button)
        self.layout.addLayout(button_layout)
        
        self.populate_branches()
        
        self.checkout_button.clicked.connect(self.checkout_branch)
        self.new_branch_button.clicked.connect(self.create_branch)
        self.delete_branch_button.clicked.connect(self.delete_branch)
        self.list_widget.itemDoubleClicked.connect(self.checkout_branch)

    def populate_branches(self):
        self.list_widget.clear()
        # --- Local Branches ---
        result = self.parent_app._run_git_command(['git', 'branch'])
        if not result or not result.stdout:
            self.list_widget.addItem("Not a Git repository or no branches found.")
            self.checkout_button.setEnabled(False)
            self.new_branch_button.setEnabled(False)
            self.delete_branch_button.setEnabled(False)
            return
            
        current_branch_item = None
        for line in result.stdout.strip().splitlines():
            branch_name = line.strip()
            is_current = branch_name.startswith('*')
            if is_current:
                branch_name = branch_name[1:].strip()
            
            item = QListWidgetItem(branch_name)
            if is_current:
                font = item.font(); font.setBold(True); item.setFont(font)
                item.setForeground(QColor("#569cd6"))
                current_branch_item = item
            self.list_widget.addItem(item)
        
        if current_branch_item: self.list_widget.setCurrentItem(current_branch_item)
        
        # --- Remote Branches ---
        remote_result = self.parent_app._run_git_command(['git', 'branch', '-r'])
        if remote_result and remote_result.stdout:
            separator = QListWidgetItem("Remotes")
            separator.setFlags(Qt.NoItemFlags) # Make it non-selectable
            separator.setForeground(QBrush(QColor("#8e8e8e")))
            self.list_widget.addItem(separator)
            
            for line in remote_result.stdout.strip().splitlines():
                # Skip the HEAD pointer
                if '->' in line: continue
                branch_name = line.strip()
                item = QListWidgetItem(branch_name)
                item.setForeground(QColor("#6A9955")) # Green for remotes
                item.setData(Qt.UserRole, 'remote') # Mark as remote
                self.list_widget.addItem(item)

    def checkout_branch(self):
        selected_item = self.list_widget.currentItem();
        if not selected_item: return
        branch_name = selected_item.text()
        is_remote = selected_item.data(Qt.UserRole) == 'remote'

        if is_remote:
            # For 'origin/main', the target local branch is 'main'
            local_branch_name = branch_name.split('/', 1)[-1]
            # 'git checkout <branch>' will create a local tracking branch if one doesn't exist
            checkout_command = ['git', 'checkout', local_branch_name]
        else:
            checkout_command = ['git', 'checkout', branch_name]

        result = self.parent_app._run_git_command(checkout_command)
        if result and result.returncode == 0:
            target_branch = local_branch_name if is_remote else branch_name
            self.parent_app.statusBar().showMessage(f"Switched to branch '{target_branch}'", 3000)
            self.parent_app._update_status_bar(); self.parent_app._update_git_status(); self.accept()
        elif result: QMessageBox.critical(self, "Error", f"Could not checkout branch:\n{result.stderr}")
        else: QMessageBox.critical(self, "Error", "Failed to execute Git command.")

    def create_branch(self):
        branch_name, ok = QInputDialog.getText(self, "Create New Branch", "Enter new branch name:")
        if ok and branch_name:
            result = self.parent_app._run_git_command(['git', 'checkout', '-b', branch_name])
            if result.returncode == 0:
                self.parent_app.statusBar().showMessage(f"Created and switched to new branch '{branch_name}'", 3000)
                self.parent_app._update_status_bar(); self.parent_app._update_git_status(); self.accept()
            else: QMessageBox.critical(self, "Error", f"Could not create branch:\n{result.stderr}")

    def delete_branch(self):
        selected_item = self.list_widget.currentItem();
        if not selected_item: return
        branch_name = selected_item.text()
        is_remote = selected_item.data(Qt.UserRole) == 'remote'
        if is_remote:
            QMessageBox.warning(self, "Action Not Supported", "To delete a remote branch, use the command line:\n'git push origin --delete <branch_name>'"); return

        if selected_item.font().bold():
            QMessageBox.warning(self, "Cannot Delete", "Cannot delete the currently active branch."); return
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete the branch '{branch_name}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = self.parent_app._run_git_command(['git', 'branch', '-d', branch_name])
            if result and result.returncode == 0: self.populate_branches()
            elif result: QMessageBox.critical(self, "Error", f"Could not delete branch:\n{result.stderr}")
            else: QMessageBox.critical(self, "Error", "Failed to execute Git command.")

class GitStashDialog(QDialog):
    """A dialog to view, apply, pop, and drop Git stashes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Git Stash List")
        self.setMinimumSize(600, 400)

        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Fira Code", 10))
        self.layout.addWidget(self.list_widget)
        
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.pop_button = QPushButton("Pop")
        self.drop_button = QPushButton("Drop")
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.pop_button)
        button_layout.addStretch()
        button_layout.addWidget(self.drop_button)
        self.layout.addLayout(button_layout)
        
        self.populate_stashes()
        
        self.apply_button.clicked.connect(self.apply_stash)
        self.pop_button.clicked.connect(self.pop_stash)
        self.drop_button.clicked.connect(self.drop_stash)
        self.list_widget.itemDoubleClicked.connect(self.apply_stash)

    def populate_stashes(self):
        self.list_widget.clear()
        result = self.parent_app._run_git_command(['git', 'stash', 'list'])
        if not result or not result.stdout:
            self.list_widget.addItem("No stashes found.")
            self.apply_button.setEnabled(False)
            self.pop_button.setEnabled(False)
            self.drop_button.setEnabled(False)
            return
        
        for line in result.stdout.strip().splitlines():
            stash_ref = line.split(':')[0]
            item = QListWidgetItem(line)
            item.setData(Qt.UserRole, stash_ref)
            self.list_widget.addItem(item)
        
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _get_selected_stash_ref(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a stash from the list.")
            return None
        return selected_items[0].data(Qt.UserRole)

    def apply_stash(self):
        ref = self._get_selected_stash_ref()
        if not ref: return
        self._run_stash_command(['git', 'stash', 'apply', ref], "Apply Stash")
        self.accept()

    def pop_stash(self):
        ref = self._get_selected_stash_ref()
        if not ref: return
        self._run_stash_command(['git', 'stash', 'pop', ref], "Pop Stash")

    def drop_stash(self):
        ref = self._get_selected_stash_ref()
        if not ref: return
        reply = QMessageBox.question(self, "Confirm Drop", f"Are you sure you want to drop '{ref}'? This action cannot be undone.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._run_stash_command(['git', 'stash', 'drop', ref], "Drop Stash")

    def _run_stash_command(self, command, title):
        result = self.parent_app._run_git_command(command)
        if result and result.returncode == 0:
            QMessageBox.information(self, title, f"'{command[-1]}' action was successful.")
            self.populate_stashes()
        elif result:
            QMessageBox.critical(self, f"{title} Failed", f"Error performing action:\n\n{result.stderr}")

class ImageViewer(QScrollArea):
    """A widget to display an image, with scrollbars for large images."""
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.image_label = QLabel()
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.image_label)
        self.setWidgetResizable(True)
        # Set a background color that matches the theme
        self.setStyleSheet("background-color: #2b2b2b;")

class VariableInspectorWidget(QWidget):
    """A widget to display variables from the debugger."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Name", "Type", "Value"])
        self.tree.header().setSectionResizeMode(2, QHeaderView.Stretch)
        self.layout.addWidget(self.tree)

    def clear_variables(self):
        self.tree.clear()

    def update_variables(self, variables):
        self.tree.clear()
        for name, value in sorted(variables.items()):
            if name.startswith('__'): continue # Skip dunder names
            self._populate_tree(self.tree, name, value)

    def _populate_tree(self, parent_item, key, value):
        try:
            value_repr = repr(value)
        except Exception:
            value_repr = "<unrepresentable>"

        item = QTreeWidgetItem(parent_item, [str(key), type(value).__name__, value_repr[:200]])

        if isinstance(value, (list, tuple, set)):
            item.setText(2, f"({len(value)} items)")
            for i, v in enumerate(value):
                self._populate_tree(item, str(i), v)
        elif isinstance(value, dict):
            item.setText(2, f"({len(value)} items)")
            for k, v in value.items():
                self._populate_tree(item, repr(k), v)
        elif hasattr(value, '__dict__'):
            item.setText(2, "") # Clear the generic repr
            for attr, attr_val in vars(value).items():
                if not attr.startswith('__'):
                    self._populate_tree(item, attr, attr_val)

class TaskRunnerWidget(QWidget):
    """A sidebar widget for discovering and running predefined tasks."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("TaskRunnerWidget")
        self.tasks = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        run_button = QPushButton("Run Task")
        layout.addWidget(run_button)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        run_button.clicked.connect(self.run_selected_task)
        self.task_list.itemDoubleClicked.connect(self.run_task_from_item)

    def load_tasks(self, tasks_data):
        self.tasks = tasks_data.get("tasks", [])
        self.task_list.clear()
        for task in self.tasks:
            item = QListWidgetItem(task.get("name", "Unnamed Task"))
            item.setToolTip(task.get("description", ""))
            self.task_list.addItem(item)

    def run_selected_task(self):
        current_row = self.task_list.currentRow()
        if 0 <= current_row < len(self.tasks):
            command = self.tasks[current_row].get("command")
            if command:
                self.parent_app.bottom_tabs.setCurrentWidget(self.parent_app.terminal_container)
                self.parent_app.run_terminal_command(command=command, from_user=False)

    def run_task_from_item(self, item):
        self.run_selected_task()

class ComplexityVisitor(ast.NodeVisitor):
    """Calculates Cyclomatic Complexity for an AST node."""
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_ExceptHandler(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_With(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_Assert(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_BoolOp(self, node): self.complexity += len(node.values) - 1; self.generic_visit(node)
    def visit_comprehension(self, node): self.complexity += 1; self.generic_visit(node)

class OutlineVisitor(ast.NodeVisitor):
    """Traverses an AST to build a structured outline with complexity."""
    def __init__(self):
        self.outline = []
        self.stack = []

    def _process_node(self, node, node_type):
        # Calculate complexity only for functions
        complexity = None
        if node_type == 'function':
            complexity_visitor = ComplexityVisitor()
            complexity_visitor.visit(node)
            complexity = complexity_visitor.complexity

        item_data = {'name': node.name, 'lineno': node.lineno, 'children': [], 'complexity': complexity}
        
        self.stack.append(item_data)
        self.generic_visit(node)
        item = self.stack.pop()

        if self.stack:
            self.stack[-1]['children'].append(item)
        else:
            self.outline.append(item)

    def visit_FunctionDef(self, node):
        self._process_node(node, 'function')

    def visit_ClassDef(self, node):
        self._process_node(node, 'class')

class SymbolVisitor(ast.NodeVisitor):
    """Traverses an AST to build a symbol table."""
    def __init__(self):
        self.symbols = {}

    def visit_ClassDef(self, node):
        methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
        self.symbols[node.name] = {'type': 'class', 'methods': methods}
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.symbols[node.name] = {'type': 'function'}
        self.generic_visit(node)

class LocalHistoryDialog(QDialog):
    """A dialog to view and restore previous versions of a file."""
    def __init__(self, file_path, current_content, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.file_path = file_path
        self.current_content = current_content

        self.setWindowTitle(f"Local History for {Path(file_path).name}")
        self.setMinimumSize(900, 700)

        self.layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal)

        # History List
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.addWidget(QLabel("Snapshots:"))
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.ExtendedSelection)
        history_layout.addWidget(self.history_list)
        self.splitter.addWidget(history_widget)

        # Diff View
        diff_widget = QWidget()
        diff_layout = QVBoxLayout(diff_widget)
        diff_layout.addWidget(QLabel("Changes:"))
        self.diff_view = QTextEdit()
        self.diff_view.setReadOnly(True)
        self.diff_view.setFont(QFont("Fira Code", 10))
        diff_layout.addWidget(self.diff_view)
        self.splitter.addWidget(diff_widget)

        self.splitter.setSizes([250, 650])
        self.layout.addWidget(self.splitter)

        self.restore_button = QPushButton("Restore this version")
        self.layout.addWidget(self.restore_button, 0, Qt.AlignRight)

        self.populate_history()

        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.currentItemChanged.connect(self.show_diff)
        self.restore_button.clicked.connect(self.restore_version)
        self.history_list.customContextMenuRequested.connect(self.show_history_context_menu)

    def populate_history(self):
        history_dir = self.parent_app._get_local_history_path(self.file_path)
        if not history_dir.exists():
            self.history_list.addItem("No history found.")
            self.restore_button.setEnabled(False)
            return
        
        snapshots = sorted(history_dir.glob('*.snapshot'), reverse=True)
        for snapshot in snapshots:
            dt_obj = datetime.strptime(snapshot.stem, "%Y-%m-%dT%H-%M-%S")
            item = QListWidgetItem(dt_obj.strftime("%Y-%m-%d %H:%M:%S"))
            item.setData(Qt.UserRole, str(snapshot))
            self.history_list.addItem(item)

    def show_diff(self, current, previous):
        if not current: return
        snapshot_path = Path(current.data(Qt.UserRole))
        old_content = snapshot_path.read_text(encoding='utf-8').splitlines()
        new_content = self.current_content.splitlines()
        diff = difflib.unified_diff(old_content, new_content, fromfile="snapshot", tofile="current", lineterm='')
        diff_text = "\n".join(list(diff))
        self.diff_view.setPlainText(diff_text if diff_text else "No changes from this version.")

    def restore_version(self):
        current_item = self.history_list.currentItem()
        if not current_item: return
        if QMessageBox.question(self, "Confirm Restore", "This will overwrite the current content in the editor. Are you sure?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            snapshot_path = Path(current_item.data(Qt.UserRole))
            content = snapshot_path.read_text(encoding='utf-8')
            self.parent_app._restore_file_content(self.file_path, content)
            self.accept()

    def show_history_context_menu(self, point):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return

        menu = QMenu()

        # Action for single selection
        delete_action = menu.addAction("Delete Snapshot")
        if len(selected_items) != 1:
            delete_action.setEnabled(False)

        # Action for two selections
        compare_action = menu.addAction("Compare Snapshots")
        if len(selected_items) != 2:
            compare_action.setEnabled(False)

        action = menu.exec_(self.history_list.mapToGlobal(point))

        if action == delete_action:
            self.delete_snapshot(selected_items[0])
        elif action == compare_action:
            self.compare_snapshots(selected_items)

    def delete_snapshot(self, item):
        snapshot_path = Path(item.data(Qt.UserRole))
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to permanently delete this snapshot?\n\n{snapshot_path.name}",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                snapshot_path.unlink()
                self.populate_history() # Repopulate to refresh the list
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete snapshot: {e}")

    def compare_snapshots(self, items):
        path1 = Path(items[0].data(Qt.UserRole))
        path2 = Path(items[1].data(Qt.UserRole))

        # Ensure path1 is the older one for a consistent diff direction
        if path1.stem > path2.stem:
            path1, path2 = path2, path1

        content1 = path1.read_text(encoding='utf-8').splitlines()
        content2 = path2.read_text(encoding='utf-8').splitlines()

        diff = difflib.unified_diff(content1, content2, fromfile=path1.name, tofile=path2.name, lineterm='')
        diff_text = "\n".join(list(diff))

        dialog_title = f"Comparing Snapshots"
        dialog = DiffViewDialog(diff_text, dialog_title, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

class InheritanceEdge(QGraphicsLineItem):
    """A line with an arrowhead for showing inheritance."""
    def __init__(self, source_node, dest_node, parent=None):
        super().__init__(parent)
        self.source = source_node
        self.dest = dest_node
        self.arrow_head = QPolygonF()
        self.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        self.setZValue(-1)

    def update_position(self):
        line = QLineF(self.source.pos(), self.dest.pos())
        self.setLine(line)
        import math
        angle = math.atan2(-line.dy(), line.dx())
        arrow_size = 15
        p1 = line.p2()
        p2 = p1 - QPointF(math.cos(angle + math.pi / 6) * arrow_size, math.sin(angle + math.pi / 6) * arrow_size)
        p3 = p1 - QPointF(math.cos(angle - math.pi / 6) * arrow_size, math.sin(angle - math.pi / 6) * arrow_size)
        self.arrow_head = QPolygonF([p1, p2, p3])

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(Qt.white))
        painter.drawPolygon(self.arrow_head)

class Edge(QGraphicsLineItem):
    """A line connecting two graph nodes."""
    def __init__(self, source_node, dest_node, parent=None):
        super().__init__(parent)
        self.source = source_node
        self.dest = dest_node
        self.setPen(QPen(Qt.white, 1, Qt.DashLine))
        self.setZValue(-1) # Draw edges behind nodes

    def update_position(self):
        line = QLineF(self.source.pos(), self.dest.pos())
        self.setLine(line)

class GraphNode(QGraphicsItemGroup):
    """A draggable node for the call graph."""
    def __init__(self, name, lineno, parent=None):
        super().__init__(parent)
        self.name = name
        self.edge_list = []
        self.lineno = lineno

        self.ellipse = QGraphicsEllipseItem(-40, -15, 80, 30, self)
        self.ellipse.setBrush(QBrush(QColor("#3c3f41")))
        self.ellipse.setPen(QPen(Qt.white))
        
        self.text = QGraphicsTextItem(name, self)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setPos(-self.text.boundingRect().width() / 2, -self.text.boundingRect().height() / 2)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edge_list:
                edge.update_position()
        return super().itemChange(change, value)

class ClassNode(QGraphicsItemGroup):
    """A draggable node representing a class for the class diagram."""
    def __init__(self, class_name, attributes, methods, lineno, parent=None):
        super().__init__(parent)
        font = QFont("Segoe UI", 9)
        self.edge_list = []
        self.lineno = lineno
        header_font = QFont("Segoe UI", 10, QFont.Bold)
        
        name_metrics = QFontMetrics(header_font)
        line_metrics = QFontMetrics(font)
        
        max_attr_width = max([line_metrics.width(a) for a in attributes] or [0])
        max_meth_width = max([line_metrics.width(m + "()") for m in methods] or [0])
        name_width = name_metrics.width(class_name)
        width = max(name_width, max_attr_width, max_meth_width) + 20
        
        self.name_text = QGraphicsTextItem(class_name)
        self.name_text.setFont(header_font)
        self.name_text.setDefaultTextColor(Qt.white)
        self.name_text.setPos(10, 5)

        y_pos = self.name_text.boundingRect().height() + 10
        
        self.attr_text = QGraphicsTextItem("\n".join(attributes))
        self.attr_text.setFont(font)
        self.attr_text.setDefaultTextColor(Qt.white)
        self.attr_text.setPos(10, y_pos)

        y_pos += self.attr_text.boundingRect().height() + 5

        self.meth_text = QGraphicsTextItem("\n".join([m + "()" for m in methods]))
        self.meth_text.setFont(font)
        self.meth_text.setDefaultTextColor(Qt.white)
        self.meth_text.setPos(10, y_pos)

        height = self.meth_text.boundingRect().bottom() + 10

        self.rect = QGraphicsRectItem(0, 0, width, height)
        self.rect.setBrush(QBrush(QColor("#3c3f41")))
        self.rect.setPen(QPen(Qt.white))

        line1_y = self.name_text.boundingRect().height() + 8
        self.sep1 = QGraphicsLineItem(0, line1_y, width, line1_y)
        self.sep1.setPen(QPen(Qt.white))

        line2_y = self.attr_text.boundingRect().bottom() + 8
        self.sep2 = QGraphicsLineItem(0, line2_y, width, line2_y)
        self.sep2.setPen(QPen(Qt.white))

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.sep1)
        self.addToGroup(self.attr_text)
        self.addToGroup(self.sep2)
        self.addToGroup(self.meth_text)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edge_list:
                edge.update_position()
        return super().itemChange(change, value)

class CallGraphVisitor(ast.NodeVisitor):
    """Traverses an AST to build a function call graph."""
    def __init__(self):
        self.graph = {}
        self.stack = []
        self.locations = {}

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        if node.name not in self.graph:
            self.graph[node.name] = set()
        self.generic_visit(node)
        self.stack.pop()
        self.locations[node.name] = node.lineno

    def visit_Call(self, node):
        if self.stack:
            caller = self.stack[-1]
            callee = None
            if isinstance(node.func, ast.Name):
                callee = node.func.id
            elif isinstance(node.func, ast.Attribute):
                # This handles method calls like `self.my_method()`
                # For simplicity, we'll just use the attribute name.
                callee = node.func.attr
            
            if callee:
                self.graph[caller].add(callee)
        self.generic_visit(node)

class ClassDiagramVisitor(ast.NodeVisitor):
    """Traverses an AST to find classes and their members."""
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        class_name = node.name
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        self.classes[class_name] = {'attributes': [], 'methods': [], 'lineno': node.lineno, 'bases': bases}
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                self.classes[class_name]['methods'].append(body_item.name)
            elif isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        self.classes[class_name]['attributes'].append(target.id)
            elif isinstance(body_item, ast.AnnAssign):
                if isinstance(body_item.target, ast.Name):
                    self.classes[class_name]['attributes'].append(body_item.target.id)

class CodeVisualizerWidget(QWidget):
    """A sidebar widget to visualize code structure."""
    node_selected = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("CodeVisualizerWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.diagram_type_combo = QComboBox()
        self.diagram_type_combo.addItems(["Call Graph", "Class Diagram"])
        generate_btn = QPushButton("Generate")
        export_btn = QPushButton("Export to PNG")
        toolbar_layout.addWidget(self.diagram_type_combo)
        toolbar_layout.addWidget(generate_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)

        # Graphics View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.view)

        # Connections
        generate_btn.clicked.connect(self.generate_visualization)
        export_btn.clicked.connect(self.export_to_png)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)

    def generate_visualization(self):
        editor = self.parent_app.get_current_editor()
        if not editor or self.parent_app.language_selector.currentText() != "Python":
            QMessageBox.warning(self, "Unsupported", "Code visualization is currently only supported for Python.")
            return

        code = editor.toPlainText()
        diagram_type = self.diagram_type_combo.currentText()
        
        try:
            if diagram_type == "Call Graph":
                tree = ast.parse(code)
                visitor = CallGraphVisitor()
                visitor.visit(tree)
                self.render_call_graph(visitor.graph, visitor.locations)
            elif diagram_type == "Class Diagram":
                tree = ast.parse(code)
                visitor = ClassDiagramVisitor()
                visitor.visit(tree)
                self.render_class_diagram(visitor.classes)
        except SyntaxError as e:
            QMessageBox.critical(self, "Syntax Error", f"Cannot generate graph due to a syntax error:\n{e}")

    def render_call_graph(self, graph_data, locations):
        self.scene.clear()
        if not graph_data: return

        all_nodes = set(graph_data.keys())
        for callees in graph_data.values():
            all_nodes.update(callees)

        node_items = {}
        import math
        radius = 200; center_x, center_y = 250, 250; angle_step = (2 * math.pi) / len(all_nodes) if all_nodes else 0
        for i, name in enumerate(sorted(list(all_nodes))):
            angle = i * angle_step
            x, y = center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)
            lineno = locations.get(name)
            node = GraphNode(name, lineno)
            node.setPos(x, y)
            self.scene.addItem(node)
            node_items[name] = node

        for caller, callees in graph_data.items():
            for callee in callees:
                if caller in node_items and callee in node_items:
                    source_node = node_items[caller]
                    dest_node = node_items[callee]
                    edge = Edge(source_node, dest_node)
                    self.scene.addItem(edge)
                    source_node.add_edge(edge)
                    dest_node.add_edge(edge)
                    edge.update_position()

    def render_class_diagram(self, class_data):
        self.scene.clear()
        if not class_data: return
        node_items = {}
        x, y = 20, 20
        for name, data in class_data.items():
            node = ClassNode(name, data['attributes'], data['methods'], data['lineno'])
            node.setPos(x, y)
            self.scene.addItem(node)
            node_items[name] = node
            x += node.boundingRect().width() + 20
            if x > self.view.width() - 150:
                x = 20; y += 250

        # Second pass to draw inheritance edges
        for name, data in class_data.items():
            for base_name in data.get('bases', []):
                if name in node_items and base_name in node_items:
                    source_node = node_items[name] # Child
                    dest_node = node_items[base_name] # Parent
                    edge = InheritanceEdge(source_node, dest_node)
                    self.scene.addItem(edge)
                    source_node.add_edge(edge)
                    dest_node.add_edge(edge)
                    edge.update_position()

    def export_to_png(self):
        if self.scene.itemsBoundingRect().isNull():
            QMessageBox.warning(self, "Export Error", "Please generate a diagram before exporting.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "PNG Image (*.png)")
        if not file_path:
            return

        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        image.save(file_path)
        painter.end()
        self.parent_app.statusBar().showMessage(f"Diagram saved to {file_path}", 3000)

    def show_context_menu(self, point):
        item = self.view.itemAt(point)
        if not item:
            return

        node = item
        while node and not isinstance(node, (GraphNode, ClassNode)):
            node = node.parentItem()

        if node and hasattr(node, 'lineno') and node.lineno:
            menu = QMenu()
            go_to_def_action = menu.addAction("Go to Definition")
            action = menu.exec_(self.view.mapToGlobal(point))

            if action == go_to_def_action:
                self.node_selected.emit(node.lineno)

class CodeBlockEditorDialog(QDialog):
    def __init__(self, code_text, language, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.language = language
        self.setWindowTitle("Edit Code Block")
        self.setMinimumSize(800, 600)

        self.layout = QVBoxLayout(self)
        self.editor = CodeEditor()
        self.editor.setPlainText(code_text)
        self.layout.addWidget(self.editor)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        # Apply settings from main app
        if self.parent_app:
            self.parent_app._apply_editor_settings(self.editor)
            self.parent_app._update_syntax_highlighter(self.editor, self.language)

    def get_edited_text(self):
        return self.editor.toPlainText()

class TestRunnerWorker(QObject):
    """Worker thread for running tests."""
    test_finished = pyqtSignal(str, str, str) # test_id, status, output
    finished = pyqtSignal()

    def __init__(self, test_ids, project_root):
        super().__init__()
        self.test_ids = test_ids
        self.project_root = project_root

    def run(self):
        for test_id in self.test_ids:
            try:
                proc = subprocess.run(
                    [sys.executable, '-m', 'unittest', test_id],
                    cwd=self.project_root,
                    capture_output=True, text=True, timeout=30
                )
                output = proc.stdout + proc.stderr
                status = "passed" if "OK" in output.splitlines()[-1] else "failed"
                self.test_finished.emit(test_id, status, output)
            except Exception as e:
                self.test_finished.emit(test_id, "failed", f"Failed to run test: {e}")
        self.finished.emit()

class TestRunnerWidget(QWidget):
    """A sidebar widget for discovering and running tests."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("TestRunnerWidget")
        self.test_items = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        discover_btn = QPushButton("Discover Tests")
        self.run_all_btn = QPushButton("Run All")
        toolbar_layout.addWidget(discover_btn)
        toolbar_layout.addWidget(self.run_all_btn)
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)

        # Test Tree
        self.test_tree = QTreeView()
        self.test_tree.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.test_tree.setModel(self.model)
        self.test_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.test_tree)

        # Connections
        discover_btn.clicked.connect(self.discover_tests)
        self.run_all_btn.clicked.connect(self.run_all_tests)
        self.test_tree.customContextMenuRequested.connect(self._show_test_context_menu)

    def _show_test_context_menu(self, point):
        """Shows a context menu for a test item."""
        index = self.test_tree.indexAt(point)
        if not index.isValid(): return

        item = self.model.itemFromIndex(index)
        if not item: return

        menu = QMenu()
        run_action = menu.addAction("Run")
        
        action = menu.exec_(self.test_tree.viewport().mapToGlobal(point))

        if action == run_action:
            test_ids = self._get_all_test_ids_from_item(item)
            if test_ids:
                self.run_tests(test_ids)

    def _get_all_test_ids_from_item(self, start_item):
        """Recursively collects all test IDs from a starting item and its children."""
        test_ids = []
        stack = [start_item]
        while stack:
            current_item = stack.pop()
            if not current_item.hasChildren():
                test_id = current_item.data(Qt.UserRole)
                if test_id: test_ids.append(test_id)
            else:
                for row in range(current_item.rowCount()):
                    stack.append(current_item.child(row))
        return test_ids

    def discover_tests(self):
        self.model.clear()
        self.test_items.clear()
        loader = unittest.TestLoader()
        suite = loader.discover(os.getcwd(), pattern='test_*.py')
        self._populate_tree(suite, self.model.invisibleRootItem())

    def _populate_tree(self, suite, parent_item):
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                suite_item = QStandardItem(test.id().split('.')[-1])
                suite_item.setEditable(False)
                suite_item.setData(test.id(), Qt.UserRole)
                parent_item.appendRow(suite_item)
                self.test_items[test.id()] = suite_item
                self._populate_tree(test, suite_item)
            else:
                test_name = test.id().split('.')[-1]
                test_item = QStandardItem(test_name)
                test_item.setEditable(False)
                test_item.setData(test.id(), Qt.UserRole)
                parent_item.appendRow(test_item)
                self.test_items[test.id()] = test_item

    def run_all_tests(self):
        test_ids = [key for key, val in self.test_items.items() if val.hasChildren() == False]
        self.run_tests(test_ids)

    def run_tests(self, test_ids):
        self.worker = TestRunnerWorker(test_ids, os.getcwd())
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.test_finished.connect(self.on_test_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_test_finished(self, test_id, status, output):
        item = self.test_items.get(test_id)
        if not item: return
        icon = QIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton if status == 'passed' else QStyle.SP_DialogCancelButton))
        item.setIcon(icon)
        item.setToolTip(output)

class GitCherryPickDialog(QDialog):
    """A dialog to select a commit to cherry-pick."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Cherry-Pick a Commit")
        self.setMinimumSize(700, 400)
        self.selected_commit_hash = None

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Select a commit to apply to the current branch:"))
        
        self.commit_list = QListWidget()
        self.commit_list.setFont(QFont("Fira Code", 10))
        self.layout.addWidget(self.commit_list)
        
        self.cherry_pick_button = QPushButton("Cherry-Pick")
        self.layout.addWidget(self.cherry_pick_button)
        
        self.populate_commits()
        
        self.cherry_pick_button.clicked.connect(self.accept_selection)
        self.commit_list.itemDoubleClicked.connect(self.accept_selection)

    def populate_commits(self):
        self.commit_list.clear()
        # Format: hash|author|date|subject
        result = self.parent_app._run_git_command(['git', 'log', '--pretty=format:%h|%an|%ar|%s', '-n', '100'])
        if not result or not result.stdout:
            self.commit_list.addItem("Could not load commit history.")
            self.cherry_pick_button.setEnabled(False)
            return
        
        for line in result.stdout.strip().splitlines():
            parts = line.split('|', 3)
            item = QListWidgetItem(f"{parts[0]} - {parts[3]} ({parts[1]}, {parts[2]})")
            item.setData(Qt.UserRole, parts[0]) # Store hash
            self.commit_list.addItem(item)

    def accept_selection(self):
        selected_items = self.commit_list.selectedItems()
        if selected_items:
            self.selected_commit_hash = selected_items[0].data(Qt.UserRole)
            self.accept()

class TaskManagerDialog(QDialog):
    """A dialog to display system processes and resource usage."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(800, 600)
        
        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        self.timer = QTimer(self)
        self.timer.setInterval(3000) # Refresh every 3 seconds
        self.timer.timeout.connect(self.update_view)
        self.timer.start()
        
        self.update_view()

    def update_view(self):
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
            try:
                p.cpu_percent(interval=0.01); procs.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        
        procs.sort(key=lambda x: x.info['cpu_percent'], reverse=True)
        html = self._generate_html(procs)
        self.web_view.setHtml(html, baseUrl=QUrl("file://"))

    def _generate_html(self, procs):
        is_dark = self.palette().window().color().lightness() < 128
        bg_color, text_color, header_bg, border_color = ("#2b2b2b", "#bbbbbb", "#3c3f41", "#555555") if is_dark else ("#f0f0f0", "#000000", "#e1e1e1", "#cccccc")
        rows = ""
        for p in procs[:100]: # Limit to top 100 processes
            try:
                mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                rows += f"<tr><td>{p.info['pid']}</td><td>{p.info['name']}</td><td>{p.info['username'] or 'N/A'}</td><td>{p.info['cpu_percent']:.1f}%</td><td>{mem_mb:.1f} MB</td></tr>"
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError): continue
        return f"""<html><head><style>
                body {{ font-family: Segoe UI, sans-serif; background-color: {bg_color}; color: {text_color}; }}
                table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid {border_color}; }}
                thead {{ background-color: {header_bg}; }}
            </style></head><body><h2>Processes</h2><table><thead><tr><th>PID</th><th>Name</th><th>User</th><th>CPU</th><th>Memory</th></tr></thead>
                <tbody>{rows}</tbody></table></body></html>"""

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

class AstViewer(QWidget):
    """A widget to display a Python Abstract Syntax Tree."""
    node_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)
        self.layout.addWidget(self.tree_view)

        self.tree_view.doubleClicked.connect(self.on_node_activated)

    def clear(self):
        self.model.clear()

    def update_ast(self, source_code):
        self.clear()
        try:
            tree = ast.parse(source_code)
            self._populate_tree(self.model.invisibleRootItem(), tree)
        except SyntaxError as e:
            self.model.appendRow(QStandardItem(f"SyntaxError: {e.msg}"))

    def _populate_tree(self, parent_item, node):
        node_text = node.__class__.__name__
        item = QStandardItem(node_text); item.setEditable(False)
        if hasattr(node, 'lineno'): item.setData(node.lineno, Qt.UserRole)
        parent_item.appendRow(item)
        for child_node in ast.iter_child_nodes(node): self._populate_tree(item, child_node)

    def on_node_activated(self, index: QModelIndex):
        line_num = self.model.data(index, Qt.UserRole)
        if line_num: self.node_selected.emit(line_num)

class GitCommitDialog(QDialog):
    """A dialog for staging and committing Git changes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Commit Changes")
        self.setMinimumSize(700, 500)

        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        h_splitter = QSplitter(Qt.Horizontal)

        # --- Unstaged Files ---
        unstaged_widget = QWidget()
        unstaged_layout = QVBoxLayout(unstaged_widget)
        unstaged_layout.addWidget(QLabel("Unstaged Changes:"))
        self.unstaged_list = QListWidget()
        self.unstaged_list.setSelectionMode(QListWidget.ExtendedSelection)
        unstaged_layout.addWidget(self.unstaged_list)
        h_splitter.addWidget(unstaged_widget)

        # --- Staging Buttons ---
        staging_buttons_layout = QVBoxLayout()
        staging_buttons_layout.addStretch()
        self.stage_button = QPushButton(" > ")
        self.stage_button.setToolTip("Stage Selected")
        self.unstage_button = QPushButton(" < ")
        self.unstage_button.setToolTip("Unstage Selected")
        staging_buttons_layout.addWidget(self.stage_button)
        staging_buttons_layout.addWidget(self.unstage_button)
        staging_buttons_layout.addStretch()
        staging_widget = QWidget()
        staging_widget.setLayout(staging_buttons_layout)
        h_splitter.addWidget(staging_widget)

        # --- Staged Files ---
        staged_widget = QWidget()
        staged_layout = QVBoxLayout(staged_widget)
        staged_layout.addWidget(QLabel("Staged Changes:"))
        self.staged_list = QListWidget()
        self.staged_list.setSelectionMode(QListWidget.ExtendedSelection)
        staged_layout.addWidget(self.staged_list)
        h_splitter.addWidget(staged_widget)
        
        h_splitter.setSizes([300, 50, 300])
        main_layout.addWidget(h_splitter)

        # --- Commit Message ---
        main_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message_input = QTextEdit()
        self.commit_message_input.setFixedHeight(100)
        main_layout.addWidget(self.commit_message_input)

        # --- Commit Button ---
        self.commit_button = QPushButton("Commit")
        main_layout.addWidget(self.commit_button, 0, Qt.AlignRight)

        # --- Connections ---
        self.stage_button.clicked.connect(self.stage_selected)
        self.unstage_button.clicked.connect(self.unstage_selected)
        self.commit_button.clicked.connect(self.commit_changes)
        self.unstaged_list.itemDoubleClicked.connect(self.stage_selected)
        self.staged_list.itemDoubleClicked.connect(self.unstage_selected)

        self.populate_files()

    def populate_files(self):
        self.unstaged_list.clear(); self.staged_list.clear()
        result = self.parent_app._run_git_command(['git', 'status', '--porcelain'])
        if not result or not result.stdout: return
        for line in result.stdout.strip().splitlines():
            status, file_path = line[:2], line[3:]
            item = QListWidgetItem(file_path); item.setData(Qt.UserRole, file_path)
            if status[1] in ('M', 'D', 'A', '?'): self.unstaged_list.addItem(item)
            if status[0] in ('M', 'A', 'D'): self.staged_list.addItem(QListWidgetItem(item))

    def stage_selected(self): self._move_items(self.unstaged_list, ['git', 'add'])
    def unstage_selected(self): self._move_items(self.staged_list, ['git', 'reset', 'HEAD', '--'])
    def _move_items(self, source_list, command):
        for item in source_list.selectedItems() or [source_list.item(i) for i in range(source_list.count())]:
            self.parent_app._run_git_command(command + [item.data(Qt.UserRole)])
        self.populate_files()

    def commit_changes(self):
        message = self.commit_message_input.toPlainText().strip()
        if not message: QMessageBox.warning(self, "Commit Error", "Commit message cannot be empty."); return
        if self.staged_list.count() == 0: QMessageBox.warning(self, "Commit Error", "There are no staged changes to commit."); return
        result = self.parent_app._run_git_command(['git', 'commit', '-m', message])
        if result and result.returncode == 0: self.parent_app.statusBar().showMessage("Commit successful.", 3000); self.accept()
        elif result: QMessageBox.critical(self, "Commit Failed", f"Error committing changes:\n\n{result.stderr}")
        else: QMessageBox.critical(self, "Commit Failed", "Failed to execute 'git commit' command.")

class IconFileSystemModel(QFileSystemModel):
    """A custom file system model that provides file icons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_provider = QFileIconProvider()
        self.changed_files = set()

    def set_git_changed_files(self, files_set):
        self.changed_files = files_set
        # A bit heavy, but ensures all visible items are re-evaluated for styling.
        self.layoutChanged.emit()

    def data(self, index, role):
        # Provide an icon for the first column
        if role == Qt.DecorationRole and index.column() == 0:
            file_info = self.fileInfo(index)
            return self.icon_provider.icon(file_info)
        
        if role == Qt.ForegroundRole and index.column() == 0:
            file_path = self.filePath(index)
            if Path(file_path).resolve() in self.changed_files:
                return QColor("#E2C08D") # Git-modified color (yellowish)

        return super().data(index, role)

class FileFilterProxyModel(QSortFilterProxyModel):
    """A proxy model to filter files and directories in the QTreeView."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def filterAcceptsRow(self, source_row, source_parent):
        # Get the index for the item in the source model
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        if not source_index.isValid():
            return False

        # 1. Always accept if the filter is empty
        filter_string = self.filterRegularExpression().pattern()
        if not filter_string:
            return True

        # 2. Check if the current item's name matches
        file_name = self.sourceModel().fileName(source_index)
        if self.filterRegularExpression().match(file_name).hasMatch():
            return True

        # 3. If it's a directory, check if any of its children match
        if self.sourceModel().isDir(source_index):
            for i in range(self.sourceModel().rowCount(source_index)):
                if self.filterAcceptsRow(i, source_index):
                    return True
        
        return False

class LineNumberArea(QWidget):
    """A widget to display line numbers for a CodeEditor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def mousePressEvent(self, event):
        """Handles clicks on the line number area, for folding."""
        self.codeEditor.toggle_fold_at_line(event.y())

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class MiniMap(QWidget):
    """A widget that displays a scaled-down overview of the code editor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        if not self.editor:
            return

        painter = QPainter(self)
        doc = self.editor.document()
        
        # Mini-map drawing parameters
        line_height = 2
        char_width = 1
        max_width = self.width()

        # Simple colors for syntax
        theme = self.editor.palette().window().color() # Get background color to decide on minimap colors
        if theme.lightness() < 128: # Dark theme
            comment_color = QColor("#6A9955")
            string_color = QColor("#ce9178")
            keyword_color = QColor("#569cd6")
            default_color = QColor(187, 187, 187, 150)
        else: # Light theme
            comment_color = QColor(0, 128, 0)
            string_color = QColor(163, 21, 21)
            keyword_color = QColor(0, 0, 255)
            default_color = QColor(50, 50, 50, 150)

        block = doc.firstBlock()
        block_num = 0
        while block.isValid():
            y = block_num * line_height
            text = block.text().lstrip()
            stripped_text = text.strip()
            indent = (len(block.text()) - len(text)) * char_width
            
            color = default_color
            if stripped_text.startswith(('#', '//', '/*')):
                color = comment_color
            elif stripped_text.startswith(('"', "'", "`")):
                color = string_color
            elif stripped_text.startswith(('def ', 'class ', 'function ')):
                color = keyword_color

            painter.setPen(color)
            painter.drawLine(indent, y, min(max_width, indent + len(text) * char_width), y)
            
            block = block.next()
            block_num += 1
            if y > self.height():
                break

        # Draw the visible area rectangle
        scrollbar = self.editor.verticalScrollBar()
        if scrollbar.maximum() > 0:
            scroll_fraction_start = scrollbar.value() / scrollbar.maximum()
            scroll_fraction_size = scrollbar.pageStep() / scrollbar.maximum()
            
            visible_rect_y = scroll_fraction_start * self.height()
            visible_rect_height = scroll_fraction_size * self.height()
            
            painter.fillRect(self.rect().adjusted(0, int(visible_rect_y), 0, -(self.height() - int(visible_rect_y + visible_rect_height))), QColor(128, 128, 128, 80))

    def _scroll_editor(self, event):
        """Scrolls the main editor based on the mouse position on the minimap."""
        y = event.y()
        scrollbar = self.editor.verticalScrollBar()
        target_value = (y / self.height()) * scrollbar.maximum()
        scrollbar.setValue(int(target_value))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._scroll_editor(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._scroll_editor(event)

class CodeEditor(QPlainTextEdit):
    """A QPlainTextEdit subclass with line numbers and current line highlighting."""
    modification_changed = pyqtSignal(bool)
    problems_found = pyqtSignal(str, list)
    bookmarks_changed = pyqtSignal(set)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.lineNumberArea = LineNumberArea(self)
        self.minimap = MiniMap(self)
        self._setup_completer()

        self.encoding = 'UTF-8'
        self.line_ending = 'LF'

        self.indent_style = 'space'
        self.indent_size = 4
        self.problems = []
        self.bookmarks = set()
        self.extra_cursors = []
        self.folding_regions = {}
        self.collapsed_blocks = set()

        # Snippet state
        self.in_snippet_mode = False
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

        # Settings toggles
        self.highlight_current_line = True
        self.show_visible_whitespace = False
        self.rounded_line_highlight = False

        self.folding_scan_timer = QTimer(self)
        self.folding_scan_timer.setSingleShot(True)
        self.folding_scan_timer.setInterval(500) # Debounce folding scan
        self.folding_scan_timer.timeout.connect(self.update_folding_regions)

        self.linter_timer = QTimer(self)
        self.linter_timer.setSingleShot(True)
        self.linter_timer.setInterval(750) # Debounce linter
        self.linter_timer.timeout.connect(self.run_linter)
        self.textChanged.connect(self._on_text_changed)

        self.symbol_scan_timer = QTimer(self)
        self.symbol_scan_timer.setSingleShot(True)
        self.symbol_scan_timer.setInterval(1500) # Less frequent than linter
        self.symbol_scan_timer.timeout.connect(self._run_symbol_scan)

        self.update_folding_regions() # Initial scan

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self._update_extra_selections)
        self.document().modificationChanged.connect(self.modification_changed.emit)

        # Connect signals for minimap
        self.verticalScrollBar().valueChanged.connect(self.minimap.update)
        self.textChanged.connect(self.minimap.update)

        self.updateLineNumberAreaWidth(0)
        self._update_extra_selections()

    def _on_text_changed(self):
        """Handles text changes for multiple features."""
        self.folding_scan_timer.start()
        self.linter_timer.start()
        self.symbol_scan_timer.start()

    def set_visible_whitespace(self, enabled):
        """Sets whether to show visible whitespace characters."""
        self.show_visible_whitespace = enabled
        self.viewport().update() # Trigger a repaint

    def paintEvent(self, event):
        """Override paintEvent to draw extra cursors and visible whitespace."""
        super().paintEvent(event)
        painter = QPainter(self.viewport())

        # Draw extra cursors
        color = self.palette().text().color()
        painter.setPen(color)
        for cursor in self.extra_cursors:
            rect = self.cursorRect(cursor)
            painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

        # Draw visible whitespace
        if self.show_visible_whitespace:
            self._draw_whitespace(painter, event)

    def mousePressEvent(self, event):
        if event.modifiers() & Qt.AltModifier:
            # Add a new cursor
            cursor = self.cursorForPosition(event.pos())
            self.extra_cursors.append(cursor)
            self.viewport().update() # Force a repaint
            event.accept()
        else:
            # Clear extra cursors on a normal click
            if self.extra_cursors:
                self.extra_cursors.clear()
                self.viewport().update() # Force a repaint
            # Let the base class handle the event to move the main cursor
            super().mousePressEvent(event)

    def _draw_whitespace(self, painter, event):
        """Draws dots for spaces and arrows for tabs."""
        ws_color = self.palette().text().color()
        ws_color.setAlpha(80)
        painter.setPen(ws_color)
        font_metrics = self.fontMetrics()
        space_width = font_metrics.horizontalAdvance(' ')

        block = self.firstVisibleBlock()

        while block.isValid() and block.geometry().top() <= event.rect().bottom():
            if block.isVisible() and block.geometry().bottom() >= event.rect().top():
                text = block.text()
                cursor = QTextCursor(block)
                for i, char in enumerate(text):
                    if char == ' ':
                        cursor.setPosition(block.position() + i)
                        rect = self.cursorRect(cursor)
                        if event.rect().intersects(rect):
                            center_y, center_x = rect.center().y(), rect.left() + space_width // 2
                            painter.drawPoint(center_x, center_y)
                    elif char == '\t':
                        cursor.setPosition(block.position() + i)
                        rect = self.cursorRect(cursor)
                        if event.rect().intersects(rect):
                            center_y = rect.center().y()
                            painter.drawLine(rect.left() + 2, center_y, rect.right() - 2, center_y)
                            painter.drawLine(rect.right() - 4, center_y - 2, rect.right() - 2, center_y)
                            painter.drawLine(rect.right() - 4, center_y + 2, rect.right() - 2, center_y)
            block = block.next()

    def _update_completer_model(self):
        """Updates the completer's word list from the document content."""
        text = self.toPlainText()
        words = sorted(list(set(re.findall(r'\b\w{3,}\b', text))))
        self.word_model.setStringList(words)

    def textUnderCursor(self):
        """Gets the word currently under the text cursor."""
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def insert_completion(self, completion):
        """Inserts the selected completion, replacing the current prefix."""
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def insert_indent(self):
        """Inserts an indent (spaces or tab) based on current settings."""
        cursor = self.textCursor()
        if self.indent_style == 'space':
            cursor.insertText(' ' * self.indent_size)
        else:
            cursor.insertText('\t')

    def remove_indent(self):
        """Removes an indent level from the current line."""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        pos_in_block = cursor.positionInBlock()
        cursor.movePosition(QTextCursor.StartOfLine)
        
        # Check the text at the start of the line for an indent to remove
        if self.indent_style == 'space':
            for _ in range(self.indent_size):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                if cursor.selectedText() != ' ':
                    cursor.clearSelection(); break
            if cursor.selectedText().isspace(): cursor.removeSelectedText()
        else: # tab
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            if cursor.selectedText() == '\t': cursor.removeSelectedText()
        cursor.endEditBlock()

    def duplicate_line(self):
        """Duplicates the line(s) containing the current cursor(s)."""
        all_cursors = [self.textCursor()] + self.extra_cursors
        # To handle multiple cursors on the same line, we only care about unique blocks
        blocks_to_duplicate = sorted(list(set(c.block() for c in all_cursors)), key=lambda b: b.blockNumber(), reverse=True)
        self.document().beginEditBlock()
        for block in blocks_to_duplicate:
            text_to_duplicate = block.text()
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfBlock)
            cursor.insertText('\n' + text_to_duplicate)
        self.document().endEditBlock()

    def duplicate_line_up(self):
        """Duplicates the current line or selection upwards."""
        self.document().beginEditBlock()
        cursor = self.textCursor()
        
        if cursor.hasSelection():
            text = cursor.selectedText()
            start_pos = cursor.selectionStart()
            
            cursor.setPosition(start_pos)
            cursor.insertText(text)
            
            # Reselect duplicated text
            new_cursor = self.textCursor()
            new_cursor.setPosition(start_pos, QTextCursor.MoveAnchor)
            new_cursor.setPosition(cursor.position(), QTextCursor.KeepAnchor)
            self.setTextCursor(new_cursor)
        else:
            # Duplicate line up
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText()
            
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.insertText(line_text + self.line_ending)
            
        self.document().endEditBlock()

    def duplicate_line_down(self):
        """Duplicates the current line or selection downwards."""
        self.document().beginEditBlock()
        cursor = self.textCursor()
        
        if cursor.hasSelection():
            text = cursor.selectedText()
            end_pos = cursor.selectionEnd()
            
            cursor.setPosition(end_pos)
            cursor.insertText(text)
            
            # Reselect duplicated text
            new_cursor = self.textCursor()
            new_cursor.setPosition(end_pos, QTextCursor.MoveAnchor)
            new_cursor.setPosition(cursor.position(), QTextCursor.KeepAnchor)
            self.setTextCursor(new_cursor)
        else:
            # Duplicate line down
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText()
            
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.EndOfLine)
            cursor.insertText(self.line_ending + line_text)
            
        self.document().endEditBlock()

    def keyPressEvent(self, event):
        # Snippet mode takes precedence for Tab and Escape keys
        if self.in_snippet_mode and event.key() == Qt.Key_Tab:
            self.jump_to_next_placeholder(); return
        if self.in_snippet_mode and event.key() == Qt.Key_Escape:
            self.exit_snippet_mode(); return

        # If multi-cursor is active, try to handle the key event and exit if successful.
        if self.extra_cursors:
            if self._handle_multi_cursor_key_press(event):
                event.accept()
                return

        # Handle custom tab/indentation logic
        if event.key() == Qt.Key_Tab:
            if not self.try_expand_snippet():
                self.insert_indent()
            return
        if event.key() == Qt.Key_Backtab:
            self.remove_indent()
            return

        # If not in multi-cursor mode or the key wasn't handled (e.g., Escape),
        # proceed with normal single-cursor logic.
        # Handle completer activation
        if self.completer.popup().isVisible() and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.completer.popup().hide()
            self.insert_completion(self.completer.currentCompletion())
            return

        # Default key press handling
        super().keyPressEvent(event)

        # Logic to show the completer popup
        # (Don't show if multi-cursor is active, even if the key was a fallback)
        if self.extra_cursors:
            return

        if event.text() == '.':
            self._trigger_member_completion()
            return # Don't show normal completer

        prefix = self.textUnderCursor()
        if len(prefix) < 2 or event.text().isspace() or not event.text():
            self.completer.popup().hide()
            return # Don't show completer for short prefixes or after spaces

        self.completer.setCompletionPrefix(prefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def try_expand_snippet(self):
        """Checks if the word before the cursor is a snippet and expands it."""
        cursor = self.textCursor()
        if cursor.hasSelection(): return False

        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        prefix = cursor.selectedText()

        main_window = self.window()
        if isinstance(main_window, CodeRunnerApp) and prefix in main_window.snippets:
            snippet_body = main_window.snippets[prefix]['body']
            cursor.removeSelectedText()
            self.expand_snippet(snippet_body)
            return True
        return False

    def expand_snippet(self, body):
        """Inserts a snippet and prepares for tab-stop navigation."""
        cursor = self.textCursor()
        self.in_snippet_mode = True
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

        # Find all placeholders like ${1:default}
        placeholder_pattern = re.compile(r'\$(\{\d+(:[^}]*)?\})')
        
        # Store placeholder info before modifying the body
        start_pos = cursor.position()
        placeholders = []
        for match in placeholder_pattern.finditer(body):
            full_match, content = match.group(0), match.group(1)
            parts = content.strip('{}').split(':', 1)
            index = int(parts[0])
            default_text = parts[1] if len(parts) > 1 else ""
            placeholders.append({'index': index, 'default': default_text, 'match_obj': match})

        # Sort by index number
        placeholders.sort(key=lambda p: p['index'])

        # Replace placeholders in body and calculate final positions
        final_body = body
        offset = 0
        for p in placeholders:
            match = p['match_obj']
            final_body = final_body.replace(match.group(0), p['default'], 1)
            self.snippet_placeholders.append({'pos': start_pos + match.start() - offset, 'len': len(p['default'])})
            offset += len(match.group(0)) - len(p['default'])

        cursor.insertText(final_body)
        self.jump_to_next_placeholder()

    def jump_to_next_placeholder(self):
        self.current_placeholder_index += 1
        if self.current_placeholder_index >= len(self.snippet_placeholders):
            self.exit_snippet_mode(); return

        placeholder = self.snippet_placeholders[self.current_placeholder_index]
        cursor = self.textCursor()
        cursor.setPosition(placeholder['pos'])
        cursor.setPosition(placeholder['pos'] + placeholder['len'], QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def exit_snippet_mode(self):
        self.in_snippet_mode = False
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

    def _handle_multi_cursor_key_press(self, event):
        """Processes a key press for all active cursors. Returns True if handled."""
        all_cursors = [self.textCursor()] + self.extra_cursors

        # --- Text Editing (Insertion/Deletion) ---
        if event.text() or event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            # Sort cursors in reverse order to prevent edit positions from invalidating subsequent cursors.
            sorted_cursors = sorted(all_cursors, key=lambda c: c.position(), reverse=True)
            self.document().beginEditBlock()
            for cursor in sorted_cursors:
                if event.text(): cursor.insertText(event.text())
                elif event.key() == Qt.Key_Backspace: cursor.deletePreviousChar()
                elif event.key() == Qt.Key_Delete: cursor.deleteChar()
            self.document().endEditBlock()
            self.setTextCursor(sorted_cursors[0]); self.extra_cursors = sorted_cursors[1:]
            self.viewport().update()
            return True

        # --- Navigation and Selection ---
        move_mode = QTextCursor.KeepAnchor if event.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
        op_map = {Qt.Key_Left: QTextCursor.Left, Qt.Key_Right: QTextCursor.Right, Qt.Key_Up: QTextCursor.Up,
                  Qt.Key_Down: QTextCursor.Down, Qt.Key_Home: QTextCursor.StartOfLine, Qt.Key_End: QTextCursor.EndOfLine}
        move_op = op_map.get(event.key())
        if move_op is not None:
            for cursor in all_cursors: cursor.movePosition(move_op, move_mode)
            self.setTextCursor(all_cursors[0]); self.extra_cursors = all_cursors[1:]
            self.viewport().update()
            return True

        return False # Key was not handled by multi-cursor logic.

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        space += 15 # Add space for folding markers
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        # Position the line number area
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        # Position the minimap
        minimap_width = 80
        self.minimap.setGeometry(cr.right() - minimap_width, cr.top(), minimap_width, cr.height())

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), self.palette().base().color().lighter(110))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                # Draw folding marker if this is a fold point
                if blockNumber in self.folding_regions:
                    painter.setPen(QColor("#8e8e8e"))
                    marker = "▶" if blockNumber in self.collapsed_blocks else "▼"
                    painter.drawText(5, top, 15, self.fontMetrics().height(), Qt.AlignCenter, marker)

                # Draw bookmark icon
                if blockNumber in self.bookmarks:
                    painter.setPen(QColor("#569cd6"))
                    # A simple bookmark icon
                    bookmark_poly = QPolygon([
                        QPoint(5, top + 2),
                        QPoint(self.lineNumberArea.width() - 20, top + 2),
                        QPoint(self.lineNumberArea.width() - 20, top + 12),
                        QPoint(self.lineNumberArea.width() - 25, top + 8),
                        QPoint(5, top + 12)
                    ])
                    painter.drawText(self.lineNumberArea.width() - 18, top, 15, self.fontMetrics().height(), Qt.AlignCenter, "B")

                painter.setPen(QColor("#6e7681"))
                painter.drawText(0, top, self.lineNumberArea.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def _update_extra_selections(self):
        """Manages all extra selections, like current line and bracket matching."""
        selections = []

        # 1. Current line highlighting
        if not self.isReadOnly() and not self.textCursor().hasSelection():
            use_standard_highlight = self.highlight_current_line and not self.rounded_line_highlight
            if use_standard_highlight:
                selection = QTextEdit.ExtraSelection()
                theme_bg = self.palette().base().color()
                lineColor = theme_bg.lighter(115) if theme_bg.lightness() < 128 else theme_bg.darker(105)

                selection.format.setBackground(lineColor)
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.cursor = self.textCursor()
                selection.cursor.clearSelection()
                selections.append(selection)

        # 2. Bracket matching
        match_selections = self._find_bracket_match()
        if match_selections:
            selections.extend(match_selections)

        # 3. Linter error highlighting
        error_format = QTextCharFormat()
        error_format.setUnderlineColor(Qt.red)
        error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        warning_format = QTextCharFormat()
        warning_format.setUnderlineColor(QColor("#FFC107")) # Amber/Yellow
        warning_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        for problem in self.problems:
            selection = QTextEdit.ExtraSelection()
            selection.format = error_format if problem['severity'] == 'error' else warning_format
            block = self.document().findBlockByNumber(problem['line'] - 1)
            if block.isValid():
                selection.cursor = QTextCursor(block)
                selections.append(selection)

        self.setExtraSelections(selections)

    def _setup_completer(self):
        """Initializes the code completer."""
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.word_model = QStringListModel()
        self.completer.setModel(self.word_model)
        self.textChanged.connect(self._update_completer_model)
        self.completer.activated.connect(self.insert_completion)

    def _find_bracket_match(self):
        """Finds matching brackets and returns ExtraSelection objects for them."""
        cursor = self.textCursor()
        if cursor.hasSelection(): return None

        pos = cursor.position()
        doc = self.document()
        
        matching_pairs = {'(': ')', '{': '}', '[': ']'}
        reverse_pairs = {v: k for k, v in matching_pairs.items()}
        
        # Check character BEFORE the cursor
        if pos > 0:
            char_before = doc.characterAt(pos - 1)
            if char_before in matching_pairs:
                return self._find_match_forward(pos - 1, char_before, matching_pairs[char_before])

        # Check character AT/AFTER the cursor
        char_after = doc.characterAt(pos)
        if char_after in reverse_pairs:
            return self._find_match_backward(pos, char_after, reverse_pairs[char_after])
            
        return None

    def _find_match_forward(self, start_pos, open_char, match_char):
        doc = self.document(); open_count = 1; search_pos = start_pos + 1
        while search_pos < doc.characterCount():
            char = doc.characterAt(search_pos)
            if char == open_char: open_count += 1
            elif char == match_char:
                open_count -= 1
                if open_count == 0: return self._create_bracket_selections(start_pos, search_pos)
            search_pos += 1
        return None

    def _find_match_backward(self, start_pos, close_char, match_char):
        doc = self.document(); close_count = 1; search_pos = start_pos - 1
        while search_pos >= 0:
            char = doc.characterAt(search_pos)
            if char == close_char: close_count += 1
            elif char == match_char:
                close_count -= 1
                if close_count == 0: return self._create_bracket_selections(search_pos, start_pos)
            search_pos -= 1
        return None

    def _create_bracket_selections(self, pos1, pos2):
        selections = []
        fmt = QTextCharFormat()
        theme = self.palette().window().color()
        color = QColor(80, 80, 80, 200) if theme.lightness() < 128 else QColor(200, 200, 200, 200)
        fmt.setBackground(color)
        for p in [pos1, pos2]:
            sel = QTextEdit.ExtraSelection()
            sel.format = fmt
            cursor = self.textCursor(); cursor.setPosition(p)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            sel.cursor = cursor
            selections.append(sel)
        return selections

    def run_linter(self):
        """Checks Python code for syntax errors and updates highlighting."""
        main_window = self.window()
        if not isinstance(main_window, CodeRunnerApp):
            return

        language = main_window.language_selector.currentText()
        code = self.toPlainText()

        if not code.strip():
            self.problems = []
            self.problems_found.emit(self.file_path or "Untitled", [])
            self._update_extra_selections()
            return

        if language == "Python":
            self._run_pyflakes_linter(code)
        elif language == "JavaScript":
            self._run_node_linter(code)
        else:
            # Clear problems for unsupported languages
            self.problems = []
            self.problems_found.emit(self.file_path or "Untitled", [])
            self._update_extra_selections()

    def _run_pyflakes_linter(self, code):
        """Runs the pyflakes linter on the given Python code."""
        new_problems = []
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            proc = subprocess.run([sys.executable, '-m', 'pyflakes', temp_file_path], capture_output=True, text=True)
            os.unlink(temp_file_path)
            if proc.stdout:
                for line in proc.stdout.strip().splitlines():
                    parts = line.split(':', 3)
                    if len(parts) >= 3 and parts[1].isdigit():
                        lineno, msg = int(parts[1]), parts[-1].strip()
                        # Check for ignore comment
                        line_text = self.document().findBlockByNumber(lineno - 1).text()
                        if "# $IGNORE" in line_text:
                            continue # Skip this problem
                        severity = "error" if "undefined name" in msg or "invalid syntax" in msg else "warning"
                        problem = {'line': lineno, 'col': 1, 'msg': msg, 'severity': severity}
                        if "undefined name" in msg:
                            match = re.search(r"undefined name '([^']+)'", msg)
                            if match:
                                problem['symbol'] = match.group(1)
                                problem['quick_fix_type'] = 'import'
                        new_problems.append(problem)
        except Exception as e:
            print(f"Pyflakes linter failed: {e}")
        self.problems = new_problems
        self.problems_found.emit(self.file_path or "Untitled", self.problems)
        self._update_extra_selections()

    def _run_node_linter(self, code):
        """Runs the node.js syntax checker on the given JavaScript code."""
        new_problems = []
        try:
            proc = subprocess.run(['node', '--check'], input=code, capture_output=True, text=True, encoding='utf-8')
            if proc.returncode != 0 and proc.stderr:
                match = re.search(r'<anonymous>:(\d+)', proc.stderr)
                if match:
                    lineno = int(match.group(1))
                    line_text = self.document().findBlockByNumber(lineno - 1).text()
                    if "// $IGNORE" not in line_text:
                        msg = proc.stderr.strip().split('\n')[-1]
                        new_problems.append({'line': lineno, 'col': 1, 'msg': msg, 'severity': 'error'})
        except Exception as e:
            print(f"Node.js linter failed: {e}")
        self.problems = new_problems
        self.problems_found.emit(self.file_path or "Untitled", self.problems)
        self._update_extra_selections()

    def _run_symbol_scan(self):
        """Runs the AST symbol scanner on the current code."""
        main_window = self.window()
        if not isinstance(main_window, CodeRunnerApp) or self.language_selector.currentText() != "Python":
            return

        code = self.toPlainText()
        if not code.strip():
            main_window.symbol_table = {}
            return

        try:
            tree = ast.parse(code)
            visitor = SymbolVisitor()
            visitor.visit(tree)
            main_window.symbol_table = visitor.symbols
            self._update_completer_model() # Refresh completer with new symbols
        except SyntaxError:
            pass # Ignore syntax errors, linter will catch them

    def update_folding_regions(self):
        """Scans the document for foldable regions based on indentation."""
        self.folding_regions.clear()
        indent_stack = [(0, -1)]  # (indent_level, line_number)
        block = self.document().firstBlock()
        block_num = 0
        while block.isValid():
            text = block.text()
            if text.strip():  # Only consider non-empty lines for folding
                indent = len(text) - len(text.lstrip())

                while indent <= indent_stack[-1][0] and len(indent_stack) > 1:
                    _start_indent, start_line = indent_stack.pop()
                    if block_num - 1 > start_line:
                        self.folding_regions[start_line] = block_num - 1

                if indent > indent_stack[-1][0]:
                    indent_stack.append((indent, block_num))

            block = block.next()
            block_num += 1

        # Close any remaining open blocks at the end of the file
        while len(indent_stack) > 1:
            _start_indent, start_line = indent_stack.pop()
            if block_num - 1 > start_line:
                self.folding_regions[start_line] = block_num - 1

        self.lineNumberArea.update()

    def toggle_fold_at_line(self, y_pos):
        """Finds the line number from a y-coordinate and toggles its fold state."""
        block = self.firstVisibleBlock()
        block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

        while block.isValid():
            block_bottom = block_top + self.blockBoundingRect(block).height()
            if block_top <= y_pos < block_bottom:
                line_num = block.blockNumber()
                if line_num in self.folding_regions:
                    self._toggle_fold_visibility(line_num)
                break
            block = block.next()
            block_top = block_bottom

    def _toggle_fold_visibility(self, start_line):
        """Hides or shows a block of code."""
        end_line = self.folding_regions.get(start_line, -1)
        if end_line == -1: return

        is_collapsing = start_line not in self.collapsed_blocks

        if is_collapsing: self.collapsed_blocks.add(start_line)
        else: self.collapsed_blocks.discard(start_line)

        block = self.document().findBlockByNumber(start_line).next()
        for i in range(start_line + 1, end_line + 1):
            if not block.isValid(): break
            block.setVisible(not is_collapsing)
            block = block.next()

        self.document().layout().update()
        self.lineNumberArea.update()

    def toggle_bookmark(self):
        """Toggles a bookmark on the current line."""
        line_num = self.textCursor().blockNumber()
        if line_num in self.bookmarks:
            self.bookmarks.remove(line_num)
        else:
            self.bookmarks.add(line_num)
        self.bookmarks_changed.emit(self.bookmarks)
        self.lineNumberArea.update()

    def next_bookmark(self):
        """Jumps the cursor to the next bookmark."""
        current_line = self.textCursor().blockNumber()
        sorted_bookmarks = sorted(list(self.bookmarks))
        for line in sorted_bookmarks:
            if line > current_line:
                self.go_to_line(line + 1)
                return
        # Wrap around to the first bookmark if at the end
        if sorted_bookmarks:
            self.go_to_line(sorted_bookmarks[0] + 1)

    def prev_bookmark(self):
        """Jumps the cursor to the previous bookmark."""
        current_line = self.textCursor().blockNumber()
        sorted_bookmarks = sorted(list(self.bookmarks), reverse=True)
        for line in sorted_bookmarks:
            if line < current_line:
                self.go_to_line(line + 1)
                return
        # Wrap around to the last bookmark if at the beginning
        if sorted_bookmarks:
            self.go_to_line(sorted_bookmarks[-1] + 1)

    def clear_bookmarks(self):
        """Removes all bookmarks from this editor."""
        self.bookmarks.clear()
        self.bookmarks_changed.emit(self.bookmarks)
        self.document().layout().update()
        self.lineNumberArea.update()

class FindReplaceWidget(QWidget):
    """A widget for finding and replacing text in a QTextEdit."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None
        self.setObjectName("FindReplaceWidget")
        self.setContentsMargins(5, 5, 5, 5)

        # --- Widgets ---
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace")

        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")

        self.case_sensitive_check = QCheckBox("Case Sensitive")
        self.whole_words_check = QCheckBox("Whole Words")

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("CloseFindBtn")

        # --- Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.find_input)
        input_layout.addWidget(self.replace_input)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.case_sensitive_check)
        options_layout.addWidget(self.whole_words_check)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(options_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.close_btn)

        # --- Connections ---
        self.close_btn.clicked.connect(self.hide)
        self.find_next_btn.clicked.connect(self.find_next)
        self.find_input.returnPressed.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace_one)
        self.replace_all_btn.clicked.connect(self.replace_all)

    def _get_find_flags(self):
        """Gets the search flags from the checkboxes."""
        flags = QTextDocument.FindFlags()
        if self.case_sensitive_check.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_words_check.isChecked():
            flags |= QTextDocument.FindWholeWords
        return flags

    def _unescape(self, text):
        """Interprets escape sequences like \t and \n."""
        return text.encode('utf-8').decode('unicode_escape')

    def find_next(self):
        find_text = self._unescape(self.find_input.text())
        if not find_text or not self.editor:
            return
        self.editor.find(find_text, self._get_find_flags())

    def replace_one(self):
        if not self.editor: return
        cursor = self.editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == self._unescape(self.find_input.text()):
            cursor.insertText(self._unescape(self.replace_input.text()))
        self.find_next()

    def replace_all(self):
        if not self.editor: return
        find_text = self._unescape(self.find_input.text())
        replace_text = self._unescape(self.replace_input.text())
        if not find_text: return

        # Use a cursor-based approach to preserve formatting
        document = self.editor.document()
        if not document: return
        cursor = QTextCursor(document)
        document.UndoStack().beginMacro("Replace All")
        while True:
            cursor = document.find(find_text, cursor, self._get_find_flags())
            if cursor.isNull(): break
            cursor.insertText(replace_text)
        document.UndoStack().endMacro()

class CodeRunnerApp(QMainWindow):
    """A desktop application for running code and shell commands."""

    def __init__(self):
        super().__init__()
        self.current_path = ""
        self.powershell_process = None
        self.powershell_thread = None
        self.output_queue = queue.Queue()

        self.profiles_dir = Path('.apicode') / 'profiles'
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.active_profile_path = self._get_active_profile_path()

        self.settings = {}
        self.highlighters = {}
        self.proxy_model = None
        self.recent_files = []
        self.snippets = {}
        self.tasks = {}
        self.debugger = None
        self.terminal_container = None # Will be set in init_ui
        self.all_problems = {} # {file_path: [problems]}
        self.profiles_menu = None
        self.editor_panes = []
        self.all_bookmarks = {} # {file_path: {line_num, ...}}
        self.file_to_compare = None
        self.active_editor_pane = None
        self.recent_files_actions = []
        self.untitled_counter = 1
        self.symbol_table = {} # For context-aware completion
        self.load_settings()
        self.init_ui()
        self.setAcceptDrops(True)
        self.apply_settings() # Apply loaded settings on startup
        QApplication.instance().focusChanged.connect(self._on_focus_changed)
        self._setup_timers()
        self._create_rope_project(self.current_path)
        self._load_snippets()
        self._load_tasks()

    def _load_or_create_snippets(self):
        snippet_file = Path("snippets.json")
        if not snippet_file.exists():
            default_snippets = {
                "neb-scaffold": { "prefix": "neb-scaffold", "body": "VWindow(\n\ttitle=\"My Nebula App\",\n\tVLayout.vertical(\n\t\tVLabel(\"Hello, Nebula!\"),\n\t\tVButton(\"Click Me\", on_click=lambda: print(\"Button clicked!\"))\n\t)\n) &amp;__app__(start);", "description": "Nebula UI Scaffold" }
            }
            with open(snippet_file, 'w', encoding='utf-8') as f: json.dump(default_snippets, f, indent=4)
        self._load_snippets()

    def _load_snippets(self):
        snippet_file = Path("snippets.json")
        if snippet_file.exists():
            with open(snippet_file, 'r') as f:
                self.snippets = json.load(f)

    def _load_tasks(self):
        tasks_file = Path("tasks.json")
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = {} # Load empty if file is corrupt

    def _create_rope_project(self, path):
        # This method is a placeholder for future rope integration
        # For now, it does nothing to avoid errors if rope isn't fully set up.
        pass

    def init_ui(self):
        self.setWindowTitle("APICode")
        self.setGeometry(150, 150, 900, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setWindowIcon(QIcon("assets/apicode.ico"))
        self.title_bar = CustomTitleBar(self)
        self.title_bar.icon_label.setPixmap(QIcon("assets/apicode.ico").pixmap(16, 16))
        self.file_menu = self.title_bar.menu_bar.addMenu("File")
        edit_menu = self.title_bar.menu_bar.addMenu("Edit")
        selection_menu = self.title_bar.menu_bar.addMenu("Selection")
        view_menu = self.title_bar.menu_bar.addMenu("View")
        go_menu = self.title_bar.menu_bar.addMenu("Go")
        git_menu = self.title_bar.menu_bar.addMenu("Git")
        run_menu = self.title_bar.menu_bar.addMenu("Run")
        debug_menu = self.title_bar.menu_bar.addMenu("Debug")
        help_menu = self.title_bar.menu_bar.addMenu("Help")
        self.new_file_action = QAction("New File", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.load_action = QAction("Open File...", self)
        self.new_profile_action = QAction("New Profile...", self)
        self.manage_profiles_action = QAction("Manage Profiles...", self)
        self.save_action = QAction("Save File...", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.settings_action = QAction("Settings...", self)
        self.local_history_action = QAction("Local History...", self)
        self.exit_action = QAction("Exit", self)
        self.close_all_tabs_action = QAction("Close All Tabs", self)
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.duplicate_line_action = QAction("Duplicate Line", self)
        self.duplicate_line_action.setShortcut("Ctrl+D")
        self.duplicate_line_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.duplicate_line()))

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.find_action = QAction("Find/Replace...", self)
        self.find_action.setShortcut("Ctrl+F")
        self.duplicate_line_action = QAction("Duplicate Line", self)
        self.duplicate_line_action.setShortcut("Ctrl+D")
        self.extract_block_action = QAction("Extract Code Block...", self)
        self.extract_block_action.setShortcut("Ctrl+Shift+E")
        self.move_line_up_action = QAction("Move Line Up", self)
        self.move_line_up_action.setShortcut("Alt+Up")
        self.move_line_down_action = QAction("Move Line Down", self)
        self.move_line_down_action.setShortcut("Alt+Down")
        self.format_document_action = QAction("Format Document", self)
        self.format_document_action.setShortcut("Shift+Alt+F")
        self.join_lines_action = QAction("Join Lines", self)
        self.trim_trailing_whitespace_action = QAction("Trim Trailing Whitespace", self)

        self.duplicate_line_up_action = QAction("Duplicate Line Up", self)
        self.duplicate_line_up_action.setShortcut("Alt+Shift+Up")
        self.duplicate_line_down_action = QAction("Duplicate Line Down", self)
        self.duplicate_line_down_action.setShortcut("Alt+Shift+Down")


        # Selection Menu Actions
        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut("Ctrl+A")

        self.split_editor_action = QAction("Split Editor", self)
        # View Menu Actions
        self.word_wrap_action = QAction("Toggle Word Wrap", self)
        self.word_wrap_action.setCheckable(True)

        # Selection Menu Actions (continued)
        self.column_select_action = QAction("Column Selection Mode", self)
        self.column_select_action.setCheckable(True)

        # Go Menu Actions
        self.go_to_line_action = QAction("Go to Line...", self)
        self.go_to_line_action.setShortcut("Ctrl+G")

        # Bookmark Actions
        self.toggle_bookmark_action = QAction("Toggle Bookmark", self)
        self.toggle_bookmark_action.setShortcut("Ctrl+F2")
        self.next_bookmark_action = QAction("Next Bookmark", self)
        self.next_bookmark_action.setShortcut("F2")
        self.prev_bookmark_action = QAction("Previous Bookmark", self)
        self.prev_bookmark_action.setShortcut("Shift+F2")
        self.clear_bookmarks_action = QAction("Clear All Bookmarks", self)


        # Command Palette
        self.command_palette_action = QAction("Command Palette...", self)
        self.command_palette_action.setShortcut("Ctrl+Shift+P")

        # Run/Help Menu Actions
        self.go_to_definition_action = QAction("Go to Definition", self)
        self.go_to_definition_action.setShortcut("F12")

        # Run/Help Menu Actions
        self.peek_definition_action = QAction("Peek Definition", self)
        self.peek_definition_action.setShortcut("Alt+F12")

        # Run/Help Menu Actions
        self.find_all_references_action = QAction("Find All References", self)
        self.find_all_references_action.setShortcut("Shift+F12")

        # Git Menu Actions
        self.manage_branches_action = QAction("Manage Branches...", self)
        self.commit_action = QAction("Commit...", self)
        self.commit_action.setShortcut("Ctrl+K")
        self.push_action = QAction("Push...", self)
        self.push_action.setShortcut("Ctrl+Shift+K")
        self.stash_action = QAction("Stash Changes...", self)
        self.apply_stash_action = QAction("Apply Latest Stash", self)
        self.stash_list_action = QAction("Stash List...", self)
        self.pull_action = QAction("Pull...", self)
        self.cherry_pick_action = QAction("Cherry-Pick...", self)
        self.git_log_action = QAction("Show Log...", self)


        self.pull_action.setShortcut("Ctrl+Shift+L")

        # View Menu Actions
        self.task_manager_action = QAction("Task Manager...", self)
        self.about_action = QAction("About APICode...", self)
        self.run_action = QAction("Run Code", self)
        self.go_to_symbol_action = QAction("Go to Symbol in File...", self)
        self.go_to_symbol_action.setShortcut("Ctrl+Shift+O")
        self.find_in_files_action = QAction("Find in Files...", self)
        self.find_in_files_action.setShortcut("Ctrl+Shift+F")
        self.check_for_updates_action = QAction("Check for Updates...", self)
        self.feedback_action = QAction("Submit Feedback...", self)

        # Populate Menus
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.load_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.local_history_action)
        self.recent_files_separator = self.file_menu.addSeparator()
        self.file_menu.addSeparator()
        self.profiles_menu = self.file_menu.addMenu("Profiles")
        self.new_profile_action.triggered.connect(self._create_new_profile)
        self.manage_profiles_action.triggered.connect(self._show_manage_profiles_dialog)
        self._update_profiles_menu()
        # The actions are added inside _update_profiles_menu to ensure correct order
        # self.profiles_menu.addSeparator()
        # self.profiles_menu.addAction(self.manage_profiles_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_all_tabs_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addAction(self.exit_action)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.find_in_files_action)
        self.change_case_menu = edit_menu.addMenu("Change Case")
        self.change_case_menu.addAction(self.to_upper_action)
        self.change_case_menu.addAction(self.to_lower_action)
        self.change_case_menu.addAction(self.to_title_action)
        self.change_case_menu.addSeparator()
        self.change_case_menu.addAction(self.to_camel_action)
        self.change_case_menu.addAction(self.to_snake_action)
        self.change_case_menu.addAction(self.to_kebab_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.extract_block_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.format_document_action)
        edit_menu.addAction(self.trim_trailing_whitespace_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.duplicate_line_up_action)
        edit_menu.addAction(self.duplicate_line_down_action)

        selection_menu.addSeparator()
        selection_menu.addAction(self.select_all_action)
        selection_menu.addAction(self.column_select_action)
        selection_menu.addSeparator()
        selection_menu.addAction(self.join_lines_action)
        selection_menu.addSeparator()
        selection_menu.addAction(self.duplicate_line_up_action)
        selection_menu.addAction(self.duplicate_line_down_action)

        view_menu.addAction(self.split_editor_action)
        theme_menu = view_menu.addMenu("Theme")
        self.theme_group = QActionGroup(self)
        for theme_name in sorted(THEME_PALETTES.keys()):
            action = theme_menu.addAction(theme_name)
            action.setCheckable(True)
            self.theme_group.addAction(action)
        view_menu.addSeparator()
        view_menu.addAction(self.command_palette_action)
        view_menu.addAction(self.task_manager_action)

        view_menu.addAction(self.word_wrap_action)
        go_menu.addAction(self.go_to_line_action)
        go_menu.addAction(self.go_to_definition_action)
        go_menu.addAction(self.peek_definition_action)
        go_menu.addSeparator()
        go_menu.addAction(self.toggle_bookmark_action)
        go_menu.addAction(self.next_bookmark_action)
        go_menu.addAction(self.prev_bookmark_action)
        go_menu.addAction(self.clear_bookmarks_action)
        go_menu.addSeparator()
        go_menu.addAction(self.find_all_references_action)

        git_menu.addAction(self.manage_branches_action)
        git_menu.addAction(self.commit_action)
        git_menu.addAction(self.push_action)
        git_menu.addSeparator()
        git_menu.addAction(self.stash_action)
        git_menu.addAction(self.apply_stash_action)
        git_menu.addAction(self.stash_list_action)
        git_menu.addSeparator()
        git_menu.addAction(self.cherry_pick_action)
        git_menu.addSeparator()
        git_menu.addAction(self.git_log_action)
        git_menu.addSeparator()
        git_menu.addAction(self.pull_action)
        run_menu.addAction(self.run_action)
        help_menu.addAction(self.check_for_updates_action)
        help_menu.addSeparator()
        help_menu.addAction(self.feedback_action)
        help_menu.addAction(self.about_action)

        # --- Widgets ---
        # Terminal Panel (self.terminal_container is set here)
        terminal_container = QWidget()
        terminal_container.setObjectName("TerminalContainer")

        self.terminal_output = QTextEdit()
        self.terminal_output.setObjectName("TerminalOutput")
        self.terminal_output.setContextMenuPolicy(Qt.CustomContextMenu)
        self.terminal_output.setReadOnly(True)

        self.command_input = QLineEdit()
        self.command_input.setObjectName("TerminalInput")
        self.command_input.setPlaceholderText("PS > Enter command...")

        # Code Runner Panel
        self.language_selector = QComboBox()
        self.language_selector.addItems([
            "Python",
            "JavaScript",
            "TypeScript",
            "Java",
            "C++",
            "C#",
            "Go",
            "Nebula",
            "Rust",
            "PHP",
            "Visual Basic",
            "Batch",
            "PowerShell",
            "HTML"
        ])

        self.output_view = QWebEngineView()
        self.output_view.setHtml(
            "<body style='background-color: #3c3f41; color: #bbbbbb; font-family: Segoe UI; padding: 5px;'>Code Output</body>"
        )
        self.copy_button = QPushButton("Copy")
        self.copy_button.setObjectName("CopyButton")

        self.editor_splitter = QSplitter(Qt.Horizontal)
        self.editor_splitter.setObjectName("EditorSplitter")

        # --- Layouts ---
        # Terminal Panel Layout
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        
        terminal_button_bar = QHBoxLayout()
        terminal_button_bar.addStretch()
        self.copy_output_button = QPushButton("Copy Output")
        self.copy_output_button.setObjectName("CopyButton")
        terminal_button_bar.addWidget(self.copy_output_button)
        
        terminal_layout.addLayout(terminal_button_bar)
        terminal_layout.addWidget(self.terminal_output)
        terminal_layout.addWidget(self.command_input)

        # Code Editor side top bar (language selector)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.language_selector)

        # Code Editor side main content (editor and output)
        code_splitter = QSplitter(Qt.Vertical)
        code_splitter.addWidget(self.editor_splitter)

        # Code Editor button bar
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()

        # Breadcrumbs
        self.breadcrumb_bar = QWidget()
        self.breadcrumb_bar.setObjectName("BreadcrumbBar")
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_bar)
        self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)

        # Combine Code Editor side layouts
        self.find_widget = FindReplaceWidget(self)
        self.find_widget.hide()
        code_editor_layout = QVBoxLayout()
        code_editor_layout.insertWidget(0, self.find_widget)
        code_editor_layout.addWidget(self.breadcrumb_bar)
        editor_bottom_splitter = QSplitter(Qt.Vertical)
        editor_bottom_splitter.addWidget(self.editor_splitter)
        code_editor_layout.addWidget(editor_bottom_splitter)
        code_editor_layout.addLayout(button_layout)

        # --- File Explorer Layout ---
        file_explorer_layout = QVBoxLayout()
        file_explorer_layout.setContentsMargins(0, 0, 0, 0)
        file_explorer_layout.setSpacing(0)

        self.open_editors_label = QLabel("OPEN EDITORS")
        self.open_editors_label.setObjectName("OpenEditorsLabel")
        self.open_editors_list = QListWidget()
        self.open_editors_list.setObjectName("OpenEditorsList")

        file_explorer_layout.addWidget(self.open_editors_label)
        file_explorer_layout.addWidget(self.open_editors_list)

        file_explorer_toolbar = QHBoxLayout()
        file_explorer_toolbar.setSpacing(2)
        self.file_search_input = QLineEdit()
        self.file_search_input.setPlaceholderText("Search files...")
        self.file_search_input.setStyleSheet("padding: 5px; border-radius: 0; border-bottom: 1px solid #555555;")
        self.git_refresh_button = QPushButton("⟳")
        self.git_refresh_button.setToolTip("Refresh Git Status")
        self.git_refresh_button.setFixedSize(30, 30)
        self.git_refresh_button.setStyleSheet("padding: 4px;")
        file_explorer_toolbar.addWidget(self.file_search_input)
        file_explorer_toolbar.addWidget(self.git_refresh_button)
        
        file_explorer_widget = QWidget()
        file_explorer_widget.setLayout(file_explorer_layout)

        # --- Left Panel Tab Widget ---
        self.left_panel_tabs = QTabWidget()
        self.left_panel_tabs.addTab(file_explorer_widget, "Explorer")

        self.source_control_widget = SourceControlWidget(self)
        self.left_panel_tabs.addTab(self.source_control_widget, "Source Control")

        self.task_runner_widget = TaskRunnerWidget(self)
        self.left_panel_tabs.addTab(self.task_runner_widget, "Tasks")

        self.ast_viewer = AstViewer()
        self.left_panel_tabs.addTab(self.ast_viewer, "AST Explorer")

        # --- Outline & Bookmarks ---
        self.outline_widget = self.create_outline_bookmark_widget()
        self.left_panel_tabs.addTab(self.outline_widget, "Outline")

        # --- Code Visualizer ---
        self.visualizer_widget = CodeVisualizerWidget(self)
        self.left_panel_tabs.addTab(self.visualizer_widget, "Visualizer")

        # --- Variable Inspector ---
        self.variable_inspector = VariableInspectorWidget(self)
        self.left_panel_tabs.addTab(self.variable_inspector, "Variable Inspector")

        # --- File Explorer ---
        self.file_model = IconFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.proxy_model = FileFilterProxyModel()
        self.proxy_model.setSourceModel(self.file_model)
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.proxy_model)
        source_root_index = self.file_model.index(os.getcwd())
        proxy_root_index = self.proxy_model.mapFromSource(source_root_index)
        self.file_tree.setRootIndex(proxy_root_index)
        self.file_tree.setColumnWidth(0, 250) # Make the name column wider
        self.file_tree.hideColumn(1) # Hide size
        self.file_tree.hideColumn(2) # Hide type
        self.file_tree.hideColumn(3) # Hide date modified
        self.file_tree.setObjectName("FileTree")
        self.file_tree.setDragEnabled(True)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)

        file_explorer_layout.addLayout(file_explorer_toolbar)
        file_explorer_layout.addWidget(self.file_tree)

        # --- Main Content Splitter ---
        # This splitter separates the code editor from the terminal
        editor_terminal_splitter = QSplitter(Qt.Horizontal)

        # This splitter separates the file explorer from the rest of the UI
        body_splitter = QSplitter(Qt.Horizontal)
        body_splitter.addWidget(self.left_panel_tabs)
        body_splitter.addWidget(editor_terminal_splitter)
        body_splitter.setSizes([250, 750]) # Initial sizes for file tree and the rest

        main_layout.addWidget(body_splitter)

        # --- Status Bar ---
        self.setStatusBar(QStatusBar(self))
        self.cpu_label = QLabel("CPU: -% ")
        self.mem_label = QLabel("Mem: -% ")
        self.git_label = QLabel("") # This will be populated by _update_status_bar
        self.gpu_label = QLabel("GPU: -% ")
        self.indent_label = QLabel("")
        self.encoding_label = QLabel("")
        self.line_ending_label = QLabel("")

        self.statusBar().addPermanentWidget(self.encoding_label)
        self.statusBar().addPermanentWidget(self.line_ending_label)
        self.indent_label.hide()

        self.statusBar().addPermanentWidget(self.indent_label)
        self.git_label.setCursor(Qt.PointingHandCursor)
        self.git_label.mousePressEvent = lambda event: self._show_git_branch_dialog()
        self.statusBar().insertPermanentWidget(0, self.git_label)
        self.statusBar().addPermanentWidget(self.cpu_label)
        self.statusBar().addPermanentWidget(self.mem_label)
        self.statusBar().addPermanentWidget(self.gpu_label)

        # --- Connections ---
        self.new_file_action.triggered.connect(self._create_new_tab)
        self.run_action.triggered.connect(self.run_code)
        self.load_action.triggered.connect(self.load_code_from_file)
        self.save_action.triggered.connect(self.save_code_to_file)
        self.save_as_action.triggered.connect(self.save_as)
        self.settings_action.triggered.connect(self.show_settings_dialog)
        self.local_history_action.triggered.connect(self._show_local_history_dialog)
        self.close_all_tabs_action.triggered.connect(self._close_all_tabs)
        self.split_editor_action.triggered.connect(self._create_new_editor_pane)
        self.find_action.triggered.connect(self.show_find_widget)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.go_to_line_action.triggered.connect(self.go_to_line)
        self.command_palette_action.triggered.connect(self._show_command_palette)
        self.manage_branches_action.triggered.connect(self._show_git_branch_dialog)
        self.commit_action.triggered.connect(self._show_git_commit_dialog)
        self.push_action.triggered.connect(self._git_push)
        self.stash_action.triggered.connect(self._git_stash)
        self.apply_stash_action.triggered.connect(self._git_apply_stash)
        self.stash_list_action.triggered.connect(self._show_git_stash_dialog)
        self.cherry_pick_action.triggered.connect(self._show_git_cherry_pick_dialog)
        self.git_log_action.triggered.connect(self._show_git_log_dialog)
        self.pull_action.triggered.connect(self._git_pull)
        self.task_manager_action.triggered.connect(self._show_task_manager)
        self.go_to_definition_action.triggered.connect(self._go_to_definition)
        self.peek_definition_action.triggered.connect(self._peek_definition)
        self.find_all_references_action.triggered.connect(self._find_all_references)
        self.toggle_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.toggle_bookmark()))
        self.next_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.next_bookmark()))
        self.prev_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.prev_bookmark()))
        self.clear_bookmarks_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.clear_bookmarks()))
        self.go_to_symbol_action.triggered.connect(self._show_go_to_symbol_dialog)
        self.find_in_files_action.triggered.connect(self._show_find_in_files_dialog)
        self.theme_group.triggered.connect(self._on_theme_changed)
        self.check_for_updates_action.triggered.connect(self._check_for_updates)
        self.start_debugging_action.triggered.connect(self._start_debugging)
        self.toggle_breakpoint_action.triggered.connect(self._toggle_breakpoint)
        self.feedback_action.triggered.connect(self._show_feedback_dialog)
        self.go_to_symbol_action.triggered.connect(self._show_go_to_symbol_dialog)
        self.column_select_action.toggled.connect(self._toggle_column_select_info)
        self.exit_action.triggered.connect(self.close)
        self.word_wrap_action.triggered.connect(self.toggle_word_wrap)

        self.format_document_action.triggered.connect(self._format_document)
        self.extract_block_action.triggered.connect(self._show_extract_block_dialog)
        self.join_lines_action.triggered.connect(self._join_selected_lines)
        self.trim_trailing_whitespace_action.triggered.connect(self._trim_trailing_whitespace)
        # Editor-specific actions
        self.duplicate_line_up_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.duplicate_line_up()))
        self.duplicate_line_down_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.duplicate_line_down()))
        self.undo_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.undo()))
        self.redo_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.redo()))
        self.cut_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.cut()))
        self.copy_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.copy()))
        self.paste_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.paste()))
        self.select_all_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.selectAll()))
        # Case conversion actions
        self.to_upper_action.triggered.connect(lambda: self._convert_selection_case(str.upper))
        self.to_lower_action.triggered.connect(lambda: self._convert_selection_case(str.lower))
        self.to_title_action.triggered.connect(lambda: self._convert_selection_case(str.title))
        self.to_camel_action.triggered.connect(lambda: self._convert_selection_case(self._to_camel_case))
        self.to_snake_action.triggered.connect(lambda: self._convert_selection_case(self._to_snake_case))
        self.to_kebab_action.triggered.connect(lambda: self._convert_selection_case(self._to_kebab_case))

        self.move_line_up_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.move_line_up()))
        self.move_line_down_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.move_line_down()))

        self.copy_button.clicked.connect(self.copy_code_to_clipboard)
        self.copy_output_button.clicked.connect(self.copy_terminal_output)
        self.command_input.returnPressed.connect(self.run_terminal_command)
        self.terminal_output.customContextMenuRequested.connect(self._show_terminal_context_menu)

        # --- Bottom Panel (Terminal, Output, Problems) ---
        self.bottom_tabs = QTabWidget()
        self.bottom_tabs.addTab(terminal_container, "Terminal")
        self.bottom_tabs.addTab(self.output_view, "Output")
        self.problems_table = QTableWidget()
        self.problems_table.setColumnCount(4)
        self.problems_table.setHorizontalHeaderLabels(["File", "Line", "Column", "Description"])
        self.problems_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.problems_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.problems_table.verticalHeader().setVisible(False)
        self.problems_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.problems_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bottom_tabs.addTab(self.problems_table, "Problems (0)")

        editor_bottom_splitter.addWidget(self.bottom_tabs)
        editor_bottom_splitter.setSizes([500, 200])

        self.open_editors_list.itemClicked.connect(self._on_open_editor_clicked)
        self.file_tree.doubleClicked.connect(self._open_file_from_tree)
        self.file_tree.customContextMenuRequested.connect(self._show_file_tree_context_menu)
        self.git_refresh_button.clicked.connect(self._update_git_status)
        self.ast_viewer.node_selected.connect(self.go_to_line)
        self.problems_table.cellDoubleClicked.connect(self._on_problem_activated)
        self.file_search_input.textChanged.connect(self._on_file_search_changed)

        self._create_new_editor_pane()
        self._update_recent_files_menu()
        # Set initial state
        self._create_new_tab() # Start with one empty tab
        self.terminal_container = terminal_container
        self.visualizer_widget.node_selected.connect(self.go_to_line)
        self.problems_table.customContextMenuRequested.connect(self._show_problems_context_menu)
        self.task_runner_widget.load_tasks(self.tasks)
        self.language_selector.currentIndexChanged.connect(lambda i: self._on_language_changed(self.language_selector.currentText()))


    def dragEnterEvent(self, event):
        """Accepts drag events if they contain file URLs."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handles dropped files by opening them in new tabs."""
        for url in event.mimeData().urls():
            if url.isLocalFile():
                path = url.toLocalFile()
                if not Path(path).is_dir():
                    self._open_file(path)

    def get_current_editor(self):
        """Returns the CodeEditor widget in the currently active tab."""
        if self.active_editor_pane:
            widget = self.active_editor_pane.currentWidget()
            if isinstance(widget, CodeEditor):
                return widget
        return None

    def _on_focus_changed(self, old, new):
        for pane in self.editor_panes:
            if new is pane or (new and new.parent() is pane):
                self.active_editor_pane = pane
                return

    def _safe_editor_action(self, action):
        """Executes an action on the current editor if it exists."""
        editor = self.get_current_editor()
        if editor:
            action(editor)

    def _on_tab_close_btn_clicked(self):
        btn = self.sender()
        parent = btn.parent()
        while parent:
            if isinstance(parent, QTabBar):
                tab_bar = parent
                break
            parent = parent.parent()
        else: return
        for i in range(tab_bar.count()):
            if tab_bar.tabButton(i, QTabBar.RightSide) == btn:
                tab_bar.parent().tabCloseRequested.emit(i)
                break

    def _create_new_editor_pane(self):
        pane = QTabWidget()
        pane.setMovable(True)
        pane.setContextMenuPolicy(Qt.CustomContextMenu)
        pane.setObjectName("CodeTabs")
        pane.currentChanged.connect(self._on_tab_changed)
        pane.tabCloseRequested.connect(self._close_tab)
        pane.customContextMenuRequested.connect(self._show_tab_context_menu)
        self.editor_splitter.addWidget(pane)
        self.editor_panes.append(pane)
        self.active_editor_pane = pane
        return pane

    def create_outline_bookmark_widget(self):
        """Creates the combined widget for Code Outline and Bookmarks."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        
        # Outline
        layout.addWidget(QLabel("OUTLINE"))
        self.outline_tree = QTreeView()
        self.outline_tree.setHeaderHidden(True)
        self.outline_model = QStandardItemModel()
        self.outline_tree.setModel(self.outline_model)
        self.outline_tree.doubleClicked.connect(self._on_outline_activated)

        # Bookmarks
        layout.addWidget(QLabel("BOOKMARKS"))
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(self._on_bookmark_activated)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.outline_tree)
        splitter.addWidget(self.bookmark_list)
        splitter.setSizes([400, 200])

        layout.addWidget(splitter)
        return widget


    def _create_image_tab(self, file_path):
        """Creates a new tab with an ImageViewer."""
        viewer = ImageViewer(file_path)
        tab_title = Path(file_path).name

        pane = self.active_editor_pane
        if not pane and self.editor_panes:
            pane = self.editor_panes[0]
        index = pane.addTab(viewer, tab_title)
        pane.setCurrentIndex(index)

        # Add custom close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("TabCloseButton")
        close_btn.setCursor(Qt.PointingHandCursor)
        pane.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)
        close_btn.clicked.connect(self._on_tab_close_btn_clicked)

        self._on_tab_changed(index)
        self._update_open_editors_list()

    def _create_new_tab(self, checked=False, file_path=None, content=""):
        editor = CodeEditor()
        editor.setPlaceholderText("Enter your code here...")
        editor.file_path = file_path
        editor.setPlainText(content)
        editor.document().setModified(False) # Start in a clean state

        if file_path:
            path = Path(file_path)
            tab_title = path.name
            self._add_to_recent_files(file_path)
        else:
            tab_title = f"Untitled-{self.untitled_counter}"
            self.untitled_counter += 1

        pane = self.active_editor_pane
        if not pane and self.editor_panes:
            pane = self.editor_panes[0]
        index = pane.addTab(editor, tab_title)
        pane.setCurrentIndex(index)

        # Add custom close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("TabCloseButton")
        close_btn.setCursor(Qt.PointingHandCursor)
        pane.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)
        close_btn.clicked.connect(self._on_tab_close_btn_clicked)
        editor.problems_found.connect(self._update_problems_panel)
        editor.bookmarks_changed.connect(self._update_bookmarks_view)
        editor.modification_changed.connect(self._on_modification_changed)

        # Apply settings and highlighter
        self._apply_editor_settings(editor)
        self._on_tab_changed(index) # This will set up highlighter and language
        self._update_open_editors_list()
        return editor

    def _close_tab(self, index):
        pane = self.sender()
        if not isinstance(pane, QTabWidget): return
        editor_to_close = pane.widget(index)

        if editor_to_close and editor_to_close.document().isModified():
            pane.setCurrentIndex(index)
            file_name = pane.tabText(index).replace(" •", "")
            reply = QMessageBox.question(self, "Unsaved Changes",
                                         f"'{file_name}' has unsaved changes. Do you want to save them?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                if not self.save_code_to_file():
                    return # User cancelled the save dialog, so abort closing
            elif reply == QMessageBox.Cancel:
                return # Abort closing the tab

        # Clear problems for this file
        if editor_to_close and editor_to_close.file_path:
            self._update_problems_panel(editor_to_close.file_path, [])

        # Clear bookmarks for this file
        if editor_to_close and editor_to_close.file_path:
            self.all_bookmarks.pop(editor_to_close.file_path, None)
            self._update_bookmarks_view()
        editor = pane.widget(index)
        if editor:
            doc_id = id(editor.document())
            if doc_id in self.highlighters:
                self.highlighters[doc_id].setDocument(None)
                del self.highlighters[doc_id]
        pane.removeTab(index)
        if pane.count() == 0 and len(self.editor_panes) > 1:
            self.editor_panes.remove(pane)
            pane.deleteLater()
            if self.active_editor_pane is pane:
                self.active_editor_pane = self.editor_panes[0] if self.editor_panes else None
        self._update_open_editors_list()

    def _close_other_tabs(self, index_to_keep):
        pane = self.active_editor_pane
        if not pane: return
        for i in range(pane.count() - 1, -1, -1):
            if i != index_to_keep:
                pane.tabCloseRequested.emit(i)

    def _close_tabs_to_right(self, index_to_keep):
        pane = self.active_editor_pane
        if not pane: return
        # Iterate backwards to avoid index shifting issues
        for i in range(pane.count() - 1, index_to_keep, -1):
            pane.tabCloseRequested.emit(i)

    def _close_tabs_to_left(self, index_to_keep):
        pane = self.active_editor_pane
        if not pane: return
        # Iterate backwards from the tab before the one to keep
        for i in range(index_to_keep - 1, -1, -1):
            pane.tabCloseRequested.emit(i)

    def _close_all_tabs(self):
        for pane in list(self.editor_panes):
            while pane.count() > 0:
                pane.tabCloseRequested.emit(0)

    def _show_tab_context_menu(self, point):
        """Shows a context menu for the code editor tabs."""
        tab_widget = self.sender()
        if not isinstance(tab_widget, QTabWidget): return

        tab_bar = tab_widget.tabBar()
        index = tab_bar.tabAt(point)
        if index == -1:
            return

        menu = QMenu()
        close_action = menu.addAction("Close")
        close_others_action = menu.addAction("Close Others")
        close_tabs_to_right_action = menu.addAction("Close Tabs to the Right")
        close_tabs_to_left_action = menu.addAction("Close Tabs to the Left")
        close_all_action = menu.addAction("Close All")
        menu.addSeparator()
        menu.addSeparator()
        reveal_action = menu.addAction("Reveal in File Explorer")

        editor = tab_widget.widget(index)
        if not editor or not hasattr(editor, 'file_path') or not editor.file_path:
            reveal_action.setEnabled(False)

        action = menu.exec_(tab_bar.mapToGlobal(point))

        if action == close_action:
            tab_widget.tabCloseRequested.emit(index)
        elif action == close_others_action and self.active_editor_pane is tab_widget:
            self._close_other_tabs(index)
        elif action == close_tabs_to_right_action and self.active_editor_pane is tab_widget:
            self._close_tabs_to_right(index)
        elif action == close_tabs_to_left_action and self.active_editor_pane is tab_widget:
            self._close_tabs_to_left(index)
        elif action == close_all_action:
            self._close_all_tabs()
        elif action == reveal_action and editor and editor.file_path:
            subprocess.run(['explorer', '/select,', str(Path(editor.file_path).resolve())])

    def _show_terminal_context_menu(self, point):
        """Shows a context menu for the terminal output."""
        menu = QMenu()

        copy_action = menu.addAction("Copy")
        select_all_action = menu.addAction("Select All")
        menu.addSeparator()
        clear_action = menu.addAction("Clear")

        # Disable copy if no text is selected
        if not self.terminal_output.textCursor().hasSelection():
            copy_action.setEnabled(False)

        action = menu.exec_(self.terminal_output.viewport().mapToGlobal(point))

        if action == copy_action:
            self.terminal_output.copy()
        elif action == select_all_action:
            self.terminal_output.selectAll()
        elif action == clear_action:
            self.terminal_output.clear()

    def _on_tab_changed(self, index):
        """Handles logic when the active tab changes."""
        pane = self.sender()
        if not isinstance(pane, QTabWidget): return
        self.active_editor_pane = pane
        if index == -1: # No tabs left
            self.find_widget.hide()
            self._update_editor_actions_state(False)
            return

        self._sync_open_editors_selection()

        widget = self.active_editor_pane.currentWidget()
        is_editor = isinstance(widget, CodeEditor)
        self._update_editor_actions_state(is_editor)

        if is_editor:
            self.find_widget.editor = widget
            file_path = widget.file_path
            lang = "Python" # Default
            if file_path:
                ext = Path(file_path).suffix.lower()
                if ext in ['.js', '.ts']: lang = "JavaScript"
                elif ext in ['.html', '.htm']: lang = "HTML"
                elif ext == '.css': lang = "CSS"
                elif ext in ['.cpp', '.cxx', '.h', '.hpp']: lang = "C++"
                elif ext == '.nebula': lang = "Nebula"
            
            self.bottom_tabs.setTabVisible(self.bottom_tabs.indexOf(self.nebula_preview), lang == "Nebula")
            self.language_selector.blockSignals(True)
            self.language_selector.setCurrentText(lang)
            self.language_selector.blockSignals(False)
            self._update_breadcrumbs(file_path)

            # .editorconfig handling
            try:
                config = editorconfig.get_properties(file_path) if file_path else {}
                widget.indent_style = config.get('indent_style', 'space')
                widget.indent_size = int(config.get('indent_size', 4))
                self.indent_label.setText(f"{widget.indent_style.capitalize()}: {widget.indent_size}")
                self.indent_label.show()
            except Exception:
                self.indent_label.hide()
                self.encoding_label.hide()
                self.line_ending_label.hide()
                # Fallback to defaults
                widget.indent_style = 'space'
                widget.indent_size = 4

            self._update_title_bar(file_path)
            
            if lang == "Python":
                self.ast_viewer.update_ast(widget.toPlainText())
                widget.run_linter() # Run linter on tab change
                self._update_outline_view(widget.toPlainText(), lang)
                self._update_bookmarks_view()
            else:
                self.ast_viewer.clear()
            self._update_syntax_highlighter(widget, lang)
        else:
            # This is an image viewer or other non-editor widget
            self.find_widget.hide()
            self.ast_viewer.clear()
            self._update_breadcrumbs(widget.file_path)
            self._update_title_bar(widget.file_path)
            self.encoding_label.setText(widget.encoding)
            self.line_ending_label.setText(widget.line_ending)
            self.encoding_label.show()
            self.line_ending_label.show()
            self.indent_label.hide()
            self._update_problems_panel(widget.file_path, []) # Clear problems for non-code files
            self._update_outline_view("", "") # Clear outline
            self._update_bookmarks_view()

    def _on_modification_changed(self, is_modified):
        """Updates the tab text to show a 'dirty' indicator."""
        editor = self.sender()
        if not isinstance(editor, CodeEditor): return

        # Find the tab for this editor
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if not isinstance(widget, CodeEditor): continue
                if widget != editor: continue

                if pane.widget(i) == editor:
                    current_text = pane.tabText(i)
                    # Remove indicator if it exists to prevent duplication
                    if " •" in current_text:
                        current_text = current_text.replace(" •", "")
                    
                    new_text = f"{current_text} •" if is_modified else current_text
                    pane.setTabText(i, new_text)
                    return

    def _on_focus_changed(self, old, new):
        if self.settings.get('auto_save_on_focus_loss', False) and isinstance(old, CodeEditor) and old.document().isModified():
            self.save_code_to_file(editor=old)
        for pane in self.editor_panes:
            if new is pane or (new and new.parent() is pane): self.active_editor_pane = pane; return

    def _update_open_editors_list(self):
        """Clears and rebuilds the 'Open Editors' list to match the current tabs."""
        self.open_editors_list.blockSignals(True)
        current_selection = self.open_editors_list.currentItem()
        current_data = (current_selection.data(Qt.UserRole) if current_selection else None)
        self.open_editors_list.clear()
        for pane_idx, pane in enumerate(self.editor_panes):
            for tab_idx in range(pane.count()):
                item = QListWidgetItem(pane.tabText(tab_idx))
                item.setData(Qt.UserRole, (pane_idx, tab_idx))
                self.open_editors_list.addItem(item)
        self.open_editors_list.blockSignals(False)
        self._sync_open_editors_selection()

    def _on_open_editor_clicked(self, item):
        """Switches to the tab corresponding to the clicked item in the 'Open Editors' list."""
        data = item.data(Qt.UserRole)
        if data:
            pane_idx, tab_idx = data
            if pane_idx < len(self.editor_panes):
                self.editor_panes[pane_idx].setCurrentIndex(tab_idx)

    def _sync_open_editors_selection(self):
        """Selects the correct item in the 'Open Editors' list when the tab changes."""
        if not self.active_editor_pane: return
        pane_idx = self.editor_panes.index(self.active_editor_pane)
        tab_idx = self.active_editor_pane.currentIndex()
        index = -1
        for i in range(self.open_editors_list.count()):
            if self.open_editors_list.item(i).data(Qt.UserRole) == (pane_idx, tab_idx):
                index = i
                break
        if index >= 0 and index < self.open_editors_list.count():
            self.open_editors_list.setCurrentRow(index)

    def _update_breadcrumbs(self, file_path):
        """Updates the breadcrumb navigation bar."""
        # Clear existing breadcrumbs by deleting all child widgets
        while self.breadcrumb_layout.count():
            child = self.breadcrumb_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.breadcrumb_layout.setSpacing(4)
        if file_path:
            path = Path(file_path)
            
            # Build a list of full paths for each part
            path_segments = []
            for p in reversed(path.parents):
                path_segments.append(p)
            path_segments.append(path)

            for p in path_segments[:-1]:
                button = QPushButton(p.name)
                button.setCursor(Qt.PointingHandCursor)
                button.clicked.connect(lambda checked=False, path_to_go=p: self._navigate_to_path_in_tree(str(path_to_go)))
                self.breadcrumb_layout.addWidget(button)
                self.breadcrumb_layout.addWidget(QLabel("›")) # Use a nicer separator
            self.breadcrumb_layout.addWidget(QLabel(path_segments[-1].name, objectName="CurrentFileCrumb"))
        self.breadcrumb_layout.addStretch()

    def _update_title_bar(self, file_path=None):
        """Updates the main window title and the custom title bar's path label."""
        if file_path:
            try:
                # Show relative path if possible
                rel_path = Path(file_path).relative_to(os.getcwd())
                display_text = f"{rel_path} - APICode"
            except ValueError:
                display_text = f"{Path(file_path).name} - APICode"
        else:
            display_text = "APICode"
        
        self.title_bar.path_label.setText(Path(file_path).name if file_path else "APICode")
        self.setWindowTitle(display_text)

    def _populate_outline_model(self, parent_model_item, outline_data):
        """Recursively populates the QStandardItemModel for the outline view."""
        for child_data in outline_data:
            name = child_data['name']
            complexity = child_data.get('complexity')
            display_text = f"{name} [C: {complexity}]" if complexity else name

            item = QStandardItem(display_text)
            item.setData(child_data['lineno'], Qt.UserRole)
            parent_model_item.appendRow(item)
            if child_data['children']:
                self._populate_outline_model(item, child_data['children'])

    def _update_outline_view(self, text, language):
        """Parses code and updates the outline view with complexity."""
        self.outline_model.clear()
        if not text or language != "Python":
            return

        try:
            tree = ast.parse(text)
            visitor = OutlineVisitor()
            visitor.visit(tree)
            self._populate_outline_model(self.outline_model.invisibleRootItem(), visitor.outline)
        except SyntaxError:
            pass # Ignore errors, linter will handle them

    def _on_outline_activated(self, index):
        line_num = self.outline_model.data(index, Qt.UserRole)
        if line_num is not None:
            self.go_to_line(line_num)

    def _update_bookmarks_view(self):
        """Updates the global bookmarks list from all open editors."""
        self.bookmark_list.clear()
        editor = self.get_current_editor()
        if not editor: return

        for line_num in sorted(list(editor.bookmarks)):
            line_text = editor.document().findBlockByNumber(line_num).text().strip()
            item = QListWidgetItem(f"L{line_num + 1}: {line_text}")
            item.setData(Qt.UserRole, line_num)
            self.bookmark_list.addItem(item)

    def _on_bookmark_activated(self, item):
        line_num = item.data(Qt.UserRole)
        if line_num is not None:
            self.go_to_line(line_num + 1)

    def _navigate_to_path_in_tree(self, path_str):
        """Sets the file tree root to the given path."""
        source_index = self.file_model.index(path_str)
        if source_index.isValid() and self.file_model.isDir(source_index):
            proxy_index = self.proxy_model.mapFromSource(source_index)
            self.file_tree.setRootIndex(proxy_index)
            self.file_tree.expand(proxy_index)

    def _on_language_changed(self, language: str):
        """Updates the highlighter when the user manually changes the language."""
        self._update_syntax_highlighter(self.get_current_editor(), language)

    def _update_syntax_highlighter(self, editor, language: str):
        """Updates the syntax highlighter based on the selected language."""
        if not editor: return
        doc = editor.document()
        doc_id = id(doc)

        # Clean up old highlighter for this document if it exists
        if doc_id in self.highlighters:
            self.highlighters[doc_id].setDocument(None)

        highlighter_class = {
            "Python": PythonHighlighter,
            "JavaScript": JavaScriptHighlighter,
            "TypeScript": JavaScriptHighlighter,
            "C++": CppHighlighter,
            "C#": CppHighlighter,
            "Java": CppHighlighter,
            "Rust": CppHighlighter,
            "HTML": HtmlHighlighter,
            "Nebula": NebulaHighlighter,
            "CSS": CssHighlighter,
            "Go": CppHighlighter,
        }.get(language)

        if highlighter_class:
            highlighter = highlighter_class(doc)
            self.highlighters[doc_id] = highlighter
            highlighter.rehighlight()
        else:
            self.highlighters.pop(doc_id, None)

    def _on_file_search_changed(self, text):
        """Filters the file tree based on the search input."""
        self.proxy_model.setFilterRegularExpression(text)

    def _get_active_profile_path(self):
        last_profile_file = self.profiles_dir / 'last_profile.txt'
        if last_profile_file.exists():
            profile_name = last_profile_file.read_text().strip()
            profile_path = self.profiles_dir / f"{profile_name}.json"
            if profile_path.exists():
                return profile_path
        default_profile_path = self.profiles_dir / 'default.json'
        if not default_profile_path.exists():
            with open(default_profile_path, 'w') as f:
                json.dump({'theme': 'Dark', 'font_size': 14}, f, indent=4)
        return default_profile_path

    def _set_active_profile(self, profile_name):
        last_profile_file = self.profiles_dir / 'last_profile.txt'
        last_profile_file.write_text(profile_name)
        self.active_profile_path = self.profiles_dir / f"{profile_name}.json"

    def _switch_profile(self, profile_name):
        self._set_active_profile(profile_name)
        self.load_settings()
        self.apply_settings()
        self._update_profiles_menu()
        self.statusBar().showMessage(f"Switched to profile: {profile_name}", 3000)

    def _create_new_profile(self):
        profile_name, ok = QInputDialog.getText(self, "New Profile", "Enter new profile name:")
        if ok and profile_name:
            new_profile_path = self.profiles_dir / f"{profile_name}.json"
            if new_profile_path.exists():
                QMessageBox.warning(self, "Profile Exists", "A profile with this name already exists.")
                return
            with open(new_profile_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            self._switch_profile(profile_name)

    def load_settings(self):
        """Loads settings from the active profile JSON file or sets defaults."""
        if self.active_profile_path.exists():
            with open(self.active_profile_path, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}
        
        # Ensure all settings have a default value
        defaults = {
            'font_size': 14, 'version': '2.2.6', 'theme': 'Dark',
            'highlight_current_line': True, 'rounded_line_highlight': False,
            'show_minimap': True, 'show_visible_whitespace': False,
            'format_on_save': False, 'auto_save_on_focus_loss': False,
            'default_line_ending': 'LF',
            'linter_debounce_time': 750
        }
        for key, value in defaults.items():
            self.settings.setdefault(key, value)

        self.recent_files = self.settings.get('recent_files', [])

    def save_settings(self):
        """Saves the current settings to the active profile JSON file."""
        # Ensure theme name is saved correctly
        self.settings['theme'] = self.property("theme_name") or "Dark"
        self.settings['recent_files'] = self.recent_files
        with open(self.active_profile_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def apply_settings(self):
        """Applies the current settings to the UI."""
        self._apply_theme()
        # Apply font settings to all editors in all panes
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if isinstance(editor, CodeEditor):
                    self._apply_editor_settings(editor)
                    self._update_completer_model_for_editor(editor) # Refresh completer after settings change
        # Apply to terminal
        font_size = self.settings.get('font_size', 14)
        font = QFont("Consolas", font_size)
        self.terminal_output.setFont(font)
        self.command_input.setFont(font)

    def _apply_editor_settings(self, editor):
        """Applies font settings to a single editor widget."""
        if not editor: return
        # Font
        font_size = self.settings.get('font_size', 14)
        font = QFont("Fira Code", font_size) # Fira Code is great for ligatures
        font.setStyleStrategy(QFont.PreferAntialias)
        editor.setFont(font)
        # Other settings
        editor.highlight_current_line = self.settings.get('highlight_current_line', True)
        editor.rounded_line_highlight = self.settings.get('rounded_line_highlight', False)
        editor.minimap.setVisible(self.settings.get('show_minimap', True))
        editor.set_visible_whitespace(self.settings.get('show_visible_whitespace', False))
        # Linter debounce
        linter_time = self.settings.get('linter_debounce_time', 750)
        editor.linter_timer.setInterval(linter_time)
        editor._update_extra_selections() # Refresh highlights
        self._update_completer_model_for_editor(editor)

    def _apply_theme(self):
        """Applies the currently selected theme stylesheet."""
        theme = self.settings.get('theme', 'dark')
        self.setProperty("theme_name", theme) # Store for highlighters
        self.setStyleSheet(generate_qss(theme))
        for action in self.theme_group.actions():
            if action.text() == theme:
                action.setChecked(True)
                break

    def show_settings_dialog(self):
        """Opens the settings dialog and applies changes if accepted."""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == QDialog.Accepted:
            self.settings = dialog.get_settings()
            self.apply_settings()
            self.save_settings()

    def _on_theme_changed(self, action):
        """Handles theme change from the menu."""
        theme = action.text()
        self.settings['theme'] = theme
        self._apply_theme()
        self.save_settings()
        self.recreate_all_highlighters()

    def _update_profiles_menu(self):
        if not self.profiles_menu: return
        self.profiles_menu.clear()
        
        profile_group = QActionGroup(self)

        # Add static actions first
        self.profiles_menu.addAction(self.new_profile_action)
        self.profiles_menu.addAction(self.manage_profiles_action)
        self.profiles_menu.addSeparator()
        
        profile_files = sorted(self.profiles_dir.glob("*.json"))
        active_profile_name = self.active_profile_path.stem
        
        for profile_path in profile_files:
            profile_name = profile_path.stem
            action = self.profiles_menu.addAction(profile_name)
            action.setCheckable(True)
            if profile_name == active_profile_name:
                action.setChecked(True)
            action.triggered.connect(lambda checked, name=profile_name: self._switch_profile(name))
            profile_group.addAction(action)

    def _update_completer_model_for_editor(self, editor):
        """Updates the completer model for a specific editor, including symbols."""
        if not isinstance(editor, CodeEditor): return

        text = editor.toPlainText()
        words = set(re.findall(r'\b\w{3,}\b', text))

        # Add symbols from the global symbol table
        for symbol, data in self.symbol_table.items():
            words.add(symbol)

        editor.word_model.setStringList(sorted(list(words)))

    def _trigger_member_completion(self, editor):
        """Triggers completion for members of an object (after a '.')."""
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 2)
        cursor.select(QTextCursor.WordUnderCursor)
        var_name = cursor.selectedText()

        completions = []
        # Simple hardcoded example for lists
        if "list" in var_name.lower(): # Very basic type inference
            completions.extend(['append', 'pop', 'sort', 'reverse', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'remove'])

        editor.completer.model().setStringList(completions)
        editor.completer.setCompletionPrefix("") # Start fresh
        editor.completer.complete()

    def _get_and_increment_version(self):
        """Gets the current version from settings, increments it, and saves it back."""
        version_str = self.settings.get('version', '1.0.0')
        
        try:
            major, minor, patch = map(int, version_str.split('.'))
            
            patch += 1
            if patch >= 10:
                patch = 0
                minor += 1
            if minor >= 100:
                minor = 0
                major += 1
            
            new_version_str = f"{major}.{minor}.{patch}"
            self.settings['version'] = new_version_str
            self.save_settings()
            return new_version_str
        except (ValueError, IndexError):
            self.settings['version'] = '1.0.0'
            self.save_settings()
            return '1.0.0'

    def show_about_dialog(self):
        """Displays the About dialog with version information."""
        version = self._get_and_increment_version()
        windowsver = platform.release()
        qtver = PYSIDE_VERSION
        psutilversion = psutil.__version__
        gpustatversion = getattr(gpustat, '__version__', 'N/A')
        pythonversion = platform.python_version()
        lgplversion = "3" # Assuming LGPLv3

        about_text = (
            f"APICode v{version} [tags: Windows {windowsver}, PyQt {qtver}, psutil {psutilversion}, "
            f"gpustat {gpustatversion}, Python {pythonversion}]\nFeatures Added: Git Integration, Split-Screen Editing.\n"
            f"Release Start: 8/30/2025 1:03 PM.\n"
            f"Licence: Found in LICENCE file, LGPLv{lgplversion}.\n\n"
            "Core Libraries: sys, os, json, subprocess, re, platform, pathlib, datetime, shutil, psutil, gpustat, tempfile, queue, ast, difflib, hashlib.\n"
            "Framework: PyQt5 (QtWidgets, QtWebEngineWidgets, QtCore, QtGui)."
            "Languages: Python."
        )
        QMessageBox.about(self, "About APICode", about_text)

    def show_find_widget(self):
        """Shows or hides the find/replace widget."""
        if self.find_widget.isVisible():
            self.find_widget.hide()
        else:
            # Pre-fill find input with selected text if any
            editor = self.get_current_editor()
            if not editor: return
            selected_text = editor.textCursor().selectedText()
            if selected_text:
                self.find_widget.find_input.setText(selected_text)
            self.find_widget.show()
            self.find_widget.find_input.setFocus()

    def go_to_line(self, line_num=None):
        """Shows a dialog to go to a line, or goes directly if line_num is provided."""
        editor = self.get_current_editor()
        if not editor:
            return

        if line_num is None:
            line_num, ok = QInputDialog.getInt(self, "Go to Line", "Line number:",
                                               editor.textCursor().blockNumber() + 1,
                                               min=1, max=editor.blockCount())
            if not ok:
                return
        
        if line_num > 0 and line_num <= editor.blockCount():
            cursor = QTextCursor(editor.document().findBlockByNumber(line_num - 1))
            editor.setTextCursor(cursor)
            editor.setFocus()

    def _show_go_to_symbol_dialog(self):
        """Parses the current file for symbols and shows the GoToSymbolDialog."""
        editor = self.get_current_editor()
        if not editor: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()
        symbols = []

        # Simple regex for Python and JS. Can be expanded.
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s*=\s*\(|\s*\()")
        else:
            self.statusBar().showMessage("Go to Symbol not supported for this language yet.", 3000)
            return

        for i, line in enumerate(text.splitlines()):
            match = pattern.match(line)
            if match:
                symbols.append((match.group(1), i))

        if not symbols:
            self.statusBar().showMessage("No symbols found in this file.", 3000)
            return

        dialog = GoToSymbolDialog(symbols, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_line != -1:
            self.go_to_line(dialog.selected_line + 1)

    def _toggle_column_select_info(self, checked):
        """Shows or clears a status bar message about column selection."""
        if checked:
            self.statusBar().showMessage("Column Selection Mode: Hold Alt+Shift and drag the mouse to select a block of text.", 0)
        else:
            self.statusBar().clearMessage()

    def _show_find_in_files_dialog(self):
        """Shows the 'Find in Files' dialog."""
        dialog = FindInFilesDialog(self)
        dialog.file_open_requested.connect(self._open_file_at_line)
        dialog.exec_()

    def _find_all_references(self):
        """Finds all references to the symbol under the cursor across the project."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol:
            self.statusBar().showMessage("No symbol selected to find references for.", 3000)
            return

        dialog = FindInFilesDialog(self)
        dialog.setWindowTitle(f"References to '{symbol}'")
        dialog.file_open_requested.connect(self._open_file_at_line)
        dialog.search_input.setText(symbol)
        dialog.whole_word_check.setChecked(True)
        dialog.case_sensitive_check.setChecked(True)
        dialog.start_search()
        dialog.exec_()

    def _peek_definition(self):
        """Shows the definition of the symbol under the cursor in a popup."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()

        pattern = None
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+" + re.escape(symbol) + r"\b")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+" + re.escape(symbol) + r"\b")

        if pattern:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if pattern.match(line):
                    # Found the definition, now extract context
                    start_line = i
                    # A simple way to get context: grab the next 15 lines or until indentation decreases
                    context_lines = [lines[start_line]]
                    base_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                    for j in range(start_line + 1, len(lines)):
                        next_line = lines[j]
                        if next_line.strip() == "": continue # Skip empty lines
                        next_indent = len(next_line) - len(next_line.lstrip())
                        if next_indent <= base_indent and j > start_line + 1:
                            break # End of block
                        context_lines.append(next_line)
                        if len(context_lines) >= 15:
                            break
                    
                    context_text = "\n".join(context_lines)

                    # Create and show the peek view
                    peek_view = PeekView(editor)
                    peek_view.setPlainText(context_text)
                    
                    # Apply font and highlighter
                    self._apply_editor_settings(peek_view)
                    self._update_syntax_highlighter(peek_view, language)

                    # Position and show
                    cursor_rect = editor.cursorRect()
                    global_pos = editor.mapToGlobal(cursor_rect.bottomLeft())
                    peek_view.move(global_pos)
                    peek_view.resize(editor.width() * 0.8, 250) # 80% of editor width
                    peek_view.show()
                    peek_view.setFocus()
                    return

        self.statusBar().showMessage(f"Definition of '{symbol}' not found.", 3000)

    def _run_git_command(self, command, file_path=None):
        """Helper to run a Git command in the file's directory."""
        cwd = os.path.dirname(file_path) if file_path else os.getcwd()
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(
                command, capture_output=True, text=True, check=True, cwd=cwd, startupinfo=si, creationflags=0x08000000
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _go_to_definition(self):
        """Jumps to the definition of the symbol under the cursor."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()

        pattern = None
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+" + re.escape(symbol) + r"\b")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+" + re.escape(symbol) + r"\b")

        if pattern:
            for i, line in enumerate(text.splitlines()):
                if pattern.match(line):
                    self.go_to_line(i + 1)
                    return
        self.statusBar().showMessage(f"Definition of '{symbol}' not found.", 3000)

    def _is_in_git_repo(self, file_path):
        """Checks if a file is within a Git repository."""
        return self._run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], file_path) is not None

    def _collect_actions_recursive(self, menu, collected_actions):
        for action in menu.actions():
            if action.menu(): # If it's a submenu
                self._collect_actions_recursive(action.menu(), collected_actions)
            elif not action.isSeparator() and action.text() and action.isEnabled():
                collected_actions.append(action)

    def _get_all_actions(self):
        all_actions = []
        # Iterate through the menus in our custom title bar
        for menu_action in self.title_bar.menu_bar.actions():
            menu = menu_action.menu()
            if menu: self._collect_actions_recursive(menu, all_actions)
        return all_actions

    def _show_command_palette(self):
        actions = self._get_all_actions()
        palette = CommandPalette(actions, self)
        palette.exec_()

    def _check_for_updates(self):
        """Simulates checking for a new version."""
        # In a real application, this would make an HTTP request.
        QMessageBox.information(self, "Check for Updates", f"You are running the latest version of APICode ({__version__}).")

    def _show_manage_profiles_dialog(self):
        active_profile_name = self.active_profile_path.stem
        dialog = ManageProfilesDialog(self.profiles_dir, active_profile_name, self)
        dialog.exec_()

    @staticmethod
    def _is_module_installed(module_name):
        """Checks if a top-level module can be imported."""
        top_level_module = module_name.split('.')[0]
        try:
            return importlib.util.find_spec(top_level_module) is not None
        except (ValueError, ModuleNotFoundError):
            return False

    def _get_import_suggestions(self, symbol):
        """Generates a list of potential import or install statements for a given symbol."""
        suggestions = []
        if symbol in QUICK_FIX_IMPORTS:
            info = QUICK_FIX_IMPORTS[symbol]
            module_name = info['module']
            package_name = info.get('package_name')

            if self._is_module_installed(module_name):
                # Suggest import statement
                if info['type'] == 'from':
                    text = f"from {module_name} import {symbol}"
                    suggestions.append({'text': text, 'line': text, 'type': 'import'})
                elif info['type'] == 'direct':
                    alias = info.get('alias')
                    text = f"import {module_name}" + (f" as {alias}" if alias else "")
                    suggestions.append({'text': text, 'line': text, 'type': 'import'})
            elif package_name:
                # Suggest installation
                text = f"Install package '{package_name}'"
                suggestions.append({'text': text, 'package': package_name, 'type': 'install'})
        return suggestions

    def _apply_quick_fix_install(self, package_name, file_path_to_recheck):
        """Shows a confirmation and then installs a package using pip."""
        reply = QMessageBox.question(self, "Install Package", f"Do you want to install the package '{package_name}' using pip?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.bottom_tabs.setCurrentWidget(self.terminal_container)
            command = f'"{sys.executable}" -m pip install {package_name}'
            self.run_terminal_command(command=command, from_user=False)
            def recheck_linter():
                editor = self._find_open_editor(file_path_to_recheck)
                if editor: editor.run_linter()
            QTimer.singleShot(15000, recheck_linter) # Re-check after 15s

    def _apply_quick_fix_import(self, file_path, suggestion_data):
        editor = self._find_open_editor(file_path)
        if not editor: return
        import_line = suggestion_data['line']
        if import_line in editor.toPlainText(): return
        cursor = QTextCursor(editor.document())
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(import_line + '\n')
        editor.run_linter()

    def _show_problems_context_menu(self, pos):
        item = self.problems_table.itemAt(pos)
        if not item: return
        
        row = item.row()
        file_path = self.problems_table.item(row, 0).data(Qt.UserRole)
        line_num = int(self.problems_table.item(row, 1).text())
        problem_msg = self.problems_table.item(row, 3).text()

        problem_data = None
        if file_path in self.all_problems:
            for p in self.all_problems[file_path]:
                if p['line'] == line_num and p['msg'] == problem_msg:
                    problem_data = p
                    break
        
        menu = QMenu()
        quick_fix_menu = menu.addMenu("Quick Fix")

        import_suggestions_added = False
        if problem_data and problem_data.get('quick_fix_type') == 'import':
            symbol = problem_data.get('symbol')
            suggestions = self._get_import_suggestions(symbol)
            if suggestions:
                for suggestion in suggestions:
                    action = quick_fix_menu.addAction(suggestion['text'])
                    if suggestion['type'] == 'import':
                        action.triggered.connect(lambda checked, s=suggestion: self._apply_quick_fix_import(file_path, s))
                    elif suggestion['type'] == 'install':
                        action.triggered.connect(lambda checked, s=suggestion, f=file_path: self._apply_quick_fix_install(s['package'], f))
                import_suggestions_added = True
        
        if not import_suggestions_added: quick_fix_menu.setEnabled(False)

        menu.addSeparator()
        ignore_action = menu.addAction("Disable for this line")
        ignore_action.triggered.connect(lambda: self._apply_quick_fix_ignore(file_path, line_num))
        menu.exec_(self.problems_table.viewport().mapToGlobal(pos))

    def _apply_quick_fix_ignore(self, file_path, line_num):
        editor = self._find_open_editor(file_path)
        if not editor:
            self.statusBar().showMessage("File must be open to apply quick fix.", 3000)
            return
        
        block = editor.document().findBlockByNumber(line_num - 1)
        if block.isValid():
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfBlock)
            comment = "  # $IGNORE" if self.language_selector.currentText() == "Python" else "  // $IGNORE"
            cursor.insertText(comment)

    def _format_document(self):
        """Formats the current document using an external tool (e.g., autopep8)."""
        editor = self.get_current_editor()
        language = self.language_selector.currentText()
        if not editor or language != "Python":
            self.statusBar().showMessage("Formatting is only available for Python files.", 3000)
            return

        code = editor.toPlainText()
        try:
            result = subprocess.run(
                ['autopep8', '-'], input=code, capture_output=True,
                text=True, check=True, encoding='utf-8'
            )
            formatted_code = result.stdout
            if formatted_code != code:
                editor.setPlainText(formatted_code)
                self.statusBar().showMessage("Document formatted.", 2000)
        except FileNotFoundError:
            QMessageBox.warning(self, "Formatter Not Found", "The 'autopep8' command was not found. Please install it using 'pip install autopep8' and ensure it's in your system's PATH.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Formatting Error", f"An error occurred during formatting:\n\n{e.stderr}")

    def _on_problem_activated(self, row, column):
        file_item = self.problems_table.item(row, 0)
        line_item = self.problems_table.item(row, 1)
        if file_item and line_item:
            file_path = file_item.data(Qt.UserRole)
            line_num = int(line_item.text())
            self._open_file_at_line(file_path, line_num)

    def _update_problems_panel(self, file_path, problems):
        if file_path:
            if problems:
                self.all_problems[file_path] = problems
            else:
                self.all_problems.pop(file_path, None)
        
        self.problems_table.setRowCount(0)
        total_problems = 0
        for f_path, f_problems in self.all_problems.items():
            total_problems += len(f_problems)
            for problem in f_problems:
                row = self.problems_table.rowCount()
                self.problems_table.insertRow(row)
                file_name_item = QTableWidgetItem(Path(f_path).name)
                file_name_item.setData(Qt.UserRole, f_path)
                self.problems_table.setItem(row, 0, file_name_item)
                self.problems_table.setItem(row, 1, QTableWidgetItem(str(problem['line'])))
                self.problems_table.setItem(row, 2, QTableWidgetItem(str(problem['col'])))
                self.problems_table.setItem(row, 3, QTableWidgetItem(problem['msg']))
                color = QColor("#f44747") if problem['severity'] == 'error' else QColor("#FFC107")
                for i in range(4): self.problems_table.item(row, i).setForeground(color)
        self.bottom_tabs.setTabText(2, f"Problems ({total_problems})")

    def _show_local_history_dialog(self):
        editor = self.get_current_editor()
        if not editor or not editor.file_path:
            self.statusBar().showMessage("Open and save a file to view its history.", 3000)
            return
        dialog = LocalHistoryDialog(editor.file_path, editor.toPlainText(), self)
        dialog.exec_()

    def _get_local_history_path(self, file_path):
        file_hash = hashlib.sha1(str(Path(file_path).resolve()).encode()).hexdigest()
        return Path('.apicode') / 'history' / file_hash

    def _create_local_history_snapshot(self, file_path):
        if not file_path: return
        try:
            history_dir = self._get_local_history_path(file_path)
            history_dir.mkdir(parents=True, exist_ok=True)
            content = Path(file_path).read_text(encoding='utf-8')
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            (history_dir / f"{timestamp}.snapshot").write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"Could not create local history snapshot for {file_path}: {e}")

    def _show_extract_block_dialog(self):
        editor = self.get_current_editor()
        if not editor: return

        cursor = editor.textCursor()
        if not cursor.hasSelection():
            self.statusBar().showMessage("Please select a block of code to extract.", 3000)
            return

        selected_text = cursor.selectedText()
        language = self.language_selector.currentText()

        dialog = CodeBlockEditorDialog(selected_text, language, self)
        if dialog.exec_() == QDialog.Accepted:
            new_text = dialog.get_edited_text()
            # The original cursor still holds the selection, so inserting text will replace it.
            cursor.insertText(new_text)
            self.statusBar().showMessage("Code block updated.", 3000)

    def _show_git_branch_dialog(self):
        dialog = GitBranchDialog(self)
        dialog.exec_()

    def _show_git_stash_dialog(self):
        dialog = GitStashDialog(self)
        dialog.exec_()

    def _show_git_log_dialog(self):
        dialog = GitLogDialog(self)
        dialog.exec_()

    def _show_git_commit_dialog(self):
        dialog = GitCommitDialog(self)
        dialog.exec_()
        self._update_git_status() # Refresh file tree colors after commit

    def _git_create_branch_from_commit(self, commit_hash):
        """Creates and checks out a new branch from a specific commit."""
        if not commit_hash: return
        branch_name, ok = QInputDialog.getText(self, "Create Branch", "Enter new branch name:")
        if ok and branch_name:
            result = self._run_git_command(['git', 'checkout', '-b', branch_name, commit_hash])
            if result and result.returncode == 0:
                QMessageBox.information(self, "Branch Created", f"Successfully created and switched to branch '{branch_name}'.")
                self._update_status_bar()
            elif result:
                QMessageBox.critical(self, "Branch Creation Failed", f"Error creating branch:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Branch Creation Failed", "Failed to execute 'git checkout' command.")

    def _git_cherry_pick(self, commit_hash):
        """Helper function to perform a cherry-pick and show results."""
        if not commit_hash: return
        result = self._run_git_command(['git', 'cherry-pick', commit_hash])
        if result and result.returncode == 0:
            QMessageBox.information(self, "Cherry-Pick Success", f"Successfully cherry-picked commit {commit_hash[:7]}.")
            self._update_git_status()
        elif result:
            QMessageBox.critical(self, "Cherry-Pick Failed", f"Error cherry-picking commit:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Cherry-Pick Failed", "Failed to execute 'git cherry-pick' command.")

    def _git_revert(self, commit_hash):
        """Performs a git revert for the given commit hash."""
        if not commit_hash: return
        reply = QMessageBox.question(self, "Confirm Revert", 
                                     f"This will create a new commit that undoes the changes from {commit_hash[:7]}.\n\nAre you sure you want to continue?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # --no-edit prevents git from opening an editor for the commit message
            result = self._run_git_command(['git', 'revert', '--no-edit', commit_hash])
            if result and result.returncode == 0:
                QMessageBox.information(self, "Revert Success", f"Successfully reverted commit {commit_hash[:7]}.")
                self._update_git_status()
            elif result:
                QMessageBox.critical(self, "Revert Failed", f"Error reverting commit:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Revert Failed", "Failed to execute 'git revert' command.")

    def _show_git_cherry_pick_dialog(self):
        dialog = GitCherryPickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self._git_cherry_pick(dialog.selected_commit_hash)

    def _git_push(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Git Push")
        msg_box.setText("Pushing to remote...")
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        QApplication.processEvents()

        result = self._run_git_command(['git', 'push'])
        msg_box.hide()

        if result and result.returncode == 0:
            QMessageBox.information(self, "Git Push", f"Push successful.\n\n{result.stdout}")
        elif result:
            QMessageBox.critical(self, "Git Push Failed", f"Error pushing to remote:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Git Push Failed", "Failed to execute 'git push' command.")

    def _git_stash(self):
        message, ok = QInputDialog.getText(self, "Stash Changes", "Enter an optional stash message:")
        if ok:
            command = ['git', 'stash']
            if message:
                command.extend(['push', '-m', message])
            
            result = self._run_git_command(command)
            if result and result.returncode == 0:
                QMessageBox.information(self, "Git Stash", "Changes stashed successfully.")
                self._update_git_status()
            elif result:
                QMessageBox.critical(self, "Git Stash Failed", f"Error stashing changes:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Git Stash Failed", "Failed to execute 'git stash' command.")

    def _git_apply_stash(self):
        result = self._run_git_command(['git', 'stash', 'apply'])
        if result and result.returncode == 0:
            QMessageBox.information(self, "Apply Stash", "Latest stash applied successfully.")
            self._update_git_status()
        elif result:
            QMessageBox.critical(self, "Apply Stash Failed", f"Error applying stash:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Apply Stash Failed", "Failed to execute 'git stash apply' command.")

    def _git_pull(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Git Pull")
        msg_box.setText("Pulling from remote...")
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        QApplication.processEvents()

        result = self._run_git_command(['git', 'pull'])
        msg_box.hide()

        if result and result.returncode == 0:
            QMessageBox.information(self, "Git Pull", f"Pull successful.\n\n{result.stdout}")
            self._update_git_status() # Refresh file tree in case of changes
        elif result:
            QMessageBox.critical(self, "Git Pull Failed", f"Error pulling from remote:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Git Pull Failed", "Failed to execute 'git pull' command.")

    def _show_task_manager(self):
        dialog = TaskManagerDialog(self)
        dialog.show() # Use show() for a non-modal dialog

    def _setup_timers(self):
        """Initializes all background timers."""
        # Setup a timer to batch process output from the queue
        self.output_timer = QTimer(self)
        self.output_timer.setInterval(50)  # Process queue every 50ms
        self.output_timer.timeout.connect(self._process_output_queue)

        # Setup a timer to update the status bar
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(2000) # Update every 2 seconds
        self.status_timer.timeout.connect(self._update_status_bar)

    def _is_in_git_repo(self, file_path):
        """Checks if a file is within a Git repository."""
        return self._run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], file_path) is not None

    def _has_git_changes(self, file_path):
        """Checks if a file has uncommitted changes."""
        result = self._run_git_command(['git', 'status', '--porcelain', '--', file_path], file_path)
        return result and result.stdout.strip() != ""

    def _show_diff_view(self, file_path):
        """Shows a dialog with the diff for a given file."""
        # Use --no-color to get plain text diff
        result = self._run_git_command(['git', '--no-pager', 'diff', 'HEAD', '--', file_path], file_path)
        if result:
            dialog = DiffViewDialog(result.stdout, Path(file_path).name, file_path, self)
            dialog.exec_()
        else:
            QMessageBox.information(self, "No Changes", "No changes found for this file compared to the last commit.")

    def _open_file_at_line(self, file_path, line_num):
        """Opens a file and jumps to a specific line."""
        self._open_file(file_path)
        self.go_to_line(line_num)

    def _reload_file_if_open(self, file_path):
        """Checks if a file is open in any tab and reloads its content from disk."""
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if editor.file_path and Path(editor.file_path).resolve() == resolved_path:
                    with open(resolved_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    cursor_pos = editor.textCursor().position()
                    editor.setPlainText(content)
                    cursor = editor.textCursor()
                    cursor.setPosition(min(cursor_pos, len(content)))
                    editor.setTextCursor(cursor)
                    self.statusBar().showMessage(f"Reloaded {resolved_path.name} due to external changes.", 3000)
                    return # Exit after reloading

    def _show_feedback_dialog(self):
        """Opens a dialog for the user to submit feedback."""
        text, ok = QInputDialog.getMultiLineText(self, "Submit Feedback", "Please provide your feedback for APICode and the development team to review:")
        if ok and text:
            feedback_dir = Path("feedback")
            feedback_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = feedback_dir / f"feedback_{timestamp}.txt"
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Feedback Submitted", "Thank you! Your feedback will be reviewed soon.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save feedback: {e}")

    def toggle_word_wrap(self):
        """Toggles word wrap for the current editor."""
        editor = self.get_current_editor()
        if not editor: return
        current_mode = editor.lineWrapMode()
        new_mode = QPlainTextEdit.NoWrap if current_mode == QPlainTextEdit.WidgetWidth else QPlainTextEdit.WidgetWidth
        editor.setLineWrapMode(new_mode)

    def _update_recent_files_menu(self):
        """Clears and rebuilds the 'Recent Files' part of the File menu."""
        # Remove all old recent file actions
        for action in self.recent_files_actions:
            self.file_menu.removeAction(action)
        self.recent_files_actions.clear()

        # Add the new actions
        self.recent_files_separator.setVisible(bool(self.recent_files))
        if self.recent_files:
            for path in self.recent_files:
                action = QAction(path, self)
                action.triggered.connect(lambda checked=False, p=path: self._open_recent_file(p))
                self.file_menu.insertAction(self.recent_files_separator, action)
                self.recent_files_actions.append(action)

    def _add_to_recent_files(self, file_path):
        """Adds a file path to the top of the recent files list."""
        if not file_path:
            return
        
        resolved_path = str(Path(file_path).resolve())
        if resolved_path in self.recent_files:
            self.recent_files.remove(resolved_path)
        
        self.recent_files.insert(0, resolved_path)
        self.recent_files = self.recent_files[:10] # Limit to 10 recent files
        
        self.save_settings()
        self._update_recent_files_menu()

    def _open_file_in_active_pane(self, file_path):
        if not self.active_editor_pane:
            if not self.editor_panes:
                self._create_new_editor_pane()
            self.active_editor_pane = self.editor_panes[0]
        self._open_file(file_path)

    def _open_file_from_tree(self, index):
        source_index = self.proxy_model.mapToSource(index)
        path = self.file_model.filePath(source_index)
        if not self.file_model.isDir(source_index):
            self._open_file_in_active_pane(path)

    def _show_file_tree_context_menu(self, point):
        """Creates and shows a context menu for the file tree."""
        proxy_index = self.file_tree.indexAt(point)
        # If clicking on empty space, use the root as the context
        if not proxy_index.isValid():
            proxy_index = self.file_tree.rootIndex()
        source_index = self.proxy_model.mapToSource(proxy_index)
        path = self.file_model.filePath(source_index)

        is_git_repo = self._is_in_git_repo(path)
        has_changes = is_git_repo and self._has_git_changes(path)

        is_dir = self.file_model.isDir(source_index)

        menu = QMenu()
        open_action = None
        if not is_dir:
            open_action = menu.addAction("Open")

        compare_action = None
        open_editor = self._find_open_editor(path)
        if open_editor and open_editor.document().isModified():
            compare_action = menu.addAction("Compare with Saved")

        view_changes_action = None
        if has_changes and not is_dir:
            view_changes_action = menu.addAction("View Changes")

        # --- Compare Logic ---
        menu.addSeparator()
        select_for_compare_action = None
        if not is_dir:
            select_for_compare_action = menu.addAction("Select for Compare")

        compare_with_action = None
        if self.file_to_compare and not is_dir and path != self.file_to_compare:
            compare_with_action = menu.addAction(f"Compare with '{Path(self.file_to_compare).name}'")

        cancel_compare_action = None
        if self.file_to_compare:
            cancel_compare_action = menu.addAction("Cancel Compare")
        # --- End Compare Logic ---

        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        rename_action = menu.addAction("Rename")
        menu.addSeparator()
        reveal_action = menu.addAction("Reveal in File Explorer")
        open_with_default_action = menu.addAction("Open with Default App")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")

        if not path: # Disable actions that don't make sense for empty space
            rename_action.setEnabled(False)
            delete_action.setEnabled(False)
            open_with_default_action.setEnabled(False)
            reveal_action.setEnabled(False)

        action = menu.exec_(self.file_tree.viewport().mapToGlobal(point))

        if action == open_action:
            self._open_file_in_active_pane(path)
        elif action == compare_action:
            self._show_editor_vs_disk_diff(open_editor)
        elif action == view_changes_action:
            self._show_diff_view(path)
        elif action == select_for_compare_action:
            self.file_to_compare = path
            self.statusBar().showMessage(f"Selected '{Path(path).name}' for comparison.", 3000)
        elif action == compare_with_action:
            self._show_file_diff(self.file_to_compare, path)
            self.file_to_compare = None # Reset after comparison
        elif action == cancel_compare_action:
            self.file_to_compare = None
            self.statusBar().showMessage("Comparison cancelled.", 2000)
        elif action == new_file_action:
            self._create_new_file_handler(path)
        elif action == new_folder_action:
            self._create_new_folder_handler(path)
        elif action == rename_action:
            self._rename_item_handler(path)
        elif action == open_with_default_action:
            if path: os.startfile(path)
        elif action == reveal_action:
            if path:
                if Path(path).is_dir():
                    os.startfile(path)
                else:
                    subprocess.run(['explorer', '/select,', str(Path(path).resolve())])
        elif action == delete_action:
            self._delete_item_handler(path)

    def _rename_item_handler(self, old_path_str):
        """Handles the 'Rename' action from the context menu."""
        if not old_path_str: return
        old_path = Path(old_path_str)
        
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=old_path.name)
        
        if ok and new_name and new_name != old_path.name:
            new_path = old_path.parent / new_name
            if new_path.exists():
                QMessageBox.warning(self, "Error", "A file or folder with that name already exists.")
                return
            try:
                old_path.rename(new_path)
                
                # Update any open tabs with the new path (This logic was buggy, simplified)
                self._update_tab_path(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename item: {e}")

    def _create_new_file_handler(self, path):
        """Handles the 'New File' action from the context menu."""
        base_path = Path(path)
        if not base_path.is_dir():
            base_path = base_path.parent

        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            new_file_path = base_path / file_name
            if not new_file_path.exists():
                new_file_path.touch() # Create the file
                self._open_file_in_active_pane(str(new_file_path))
            else:
                QMessageBox.warning(self, "Error", "A file with that name already exists.")

    def _update_tab_path(self, old_path, new_path):
        """Updates the path and title of an open tab after a rename."""
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if editor.file_path and Path(editor.file_path).resolve() == old_path.resolve():
                    editor.file_path = str(new_path)
                    pane.setTabText(i, new_path.name)
                    self._update_open_editors_list()
                    return

    def _create_new_folder_handler(self, path):
        """Handles the 'New Folder' action from the context menu."""
        base_path = Path(path)
        if not base_path.is_dir():
            base_path = base_path.parent

        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and folder_name:
            new_folder_path = base_path / folder_name
            if not new_folder_path.exists():
                new_folder_path.mkdir()
            else:
                QMessageBox.warning(self, "Error", "A folder with that name already exists.")

    def _delete_item_handler(self, path):
        """Handles the 'Delete' action from the context menu."""
        if not path: return
        p = Path(path)
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{p.name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete item: {e}")

    def _open_file(self, file_path):
        """Helper function to open a file and create a new tab for it."""
        resolved_path = Path(file_path).resolve()
        # Check if the file is already open in any pane
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if hasattr(widget, 'file_path') and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    pane.setCurrentIndex(i)
                    self.active_editor_pane = pane
                    return

        IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
        if resolved_path.suffix.lower() in IMAGE_EXTENSIONS:
            self._create_image_tab(str(resolved_path))
        else:
            try:
                with open(resolved_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._create_new_tab(file_path=str(resolved_path), content=content)
                self.statusBar().showMessage(f"Loaded {resolved_path}", 3000)
            except UnicodeDecodeError:
                reply = QMessageBox.question(self, "Binary File Detected",
                                             "This file does not appear to be text. Open with default application?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    os.startfile(str(resolved_path))
            except Exception as e:
                self.statusBar().showMessage(f"Error opening file: {e}", 5000)

    def _update_editor_actions_state(self, is_editor):
        """Enables or disables actions based on whether the current tab is an editor."""
        actions_to_toggle = [
            self.save_action, self.save_as_action, self.undo_action, self.redo_action,
            self.cut_action, self.copy_action, self.paste_action, self.find_action,
            self.duplicate_line_action, self.select_all_action, self.word_wrap_action,
            self.go_to_line_action, self.go_to_definition_action, self.peek_definition_action,
            self.find_all_references_action, self.go_to_symbol_action
        ]
        for action in actions_to_toggle:
            action.setEnabled(is_editor)

    def _find_open_editor(self, file_path):
        """Finds and returns the editor widget for a given file path, if open."""
        if not file_path: return None
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if isinstance(widget, CodeEditor) and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    return widget
        return None

    def _show_editor_vs_disk_diff(self, editor):
        """Shows a diff between the editor's content and the version on disk."""
        if not editor or not editor.file_path: return
            
        file_path = editor.file_path
        editor_content = editor.toPlainText().splitlines()
        
        try:
            disk_content = Path(file_path).read_text(encoding='utf-8').splitlines()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read file from disk: {e}")
            return
            
        diff = difflib.unified_diff(disk_content, editor_content, fromfile="saved on disk", tofile="current in editor", lineterm='')
        diff_text = "\n".join(list(diff))
        
        dialog = DiffViewDialog(diff_text, Path(file_path).name, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

    def _show_file_diff(self, path1, path2):
        """Shows a diff view for two arbitrary files."""
        try:
            content1 = Path(path1).read_text(encoding='utf-8', errors='ignore').splitlines()
            content2 = Path(path2).read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception as e:
            QMessageBox.critical(self, "Error Reading Files", f"Could not read one of the files for comparison:\n{e}")
            return

        diff = difflib.unified_diff(content1, content2, fromfile=Path(path1).name, tofile=Path(path2).name, lineterm='')
        diff_text = "\n".join(list(diff))

        dialog_title = f"Comparing Files"
        dialog = DiffViewDialog(diff_text, dialog_title, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

    def _open_recent_file(self, path):
        """Opens a file from the recent files list."""
        file = Path(path)
        if file.exists():
            self._open_file_in_active_pane(path)
        else:
            self.recent_files.remove(path)
            self._update_recent_files_menu()
            self.statusBar().showMessage(f"File not found: {path}", 3000)

    def _update_status_bar(self):
        """Periodically updates the resource usage in the status bar."""
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")

        # Memory
        mem_percent = psutil.virtual_memory().percent
        self.mem_label.setText(f"Mem: {mem_percent:.1f}%")

        # GPU (NVIDIA only, via gpustat)
        try:
            gpu_stats = gpustat.new_query()
            if gpu_stats:
                gpu = gpu_stats[0] # Take the first GPU
                self.gpu_label.setText(f"GPU: {gpu.utilization}%")
            else:
                self.gpu_label.setText("GPU: N/A")
        except Exception:
            self.gpu_label.setText("GPU: N/A")
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True, cwd=os.getcwd(), startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW
            )
            branch_name = result.stdout.strip()
            self.git_label.setText(f" {branch_name}")
            self.git_label.show()
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.git_label.hide()

    def _update_git_status(self):
        """Gets git status and tells the file model and source control widget to update."""
        changed_files = self._get_git_changed_files_set()
        if hasattr(self.file_model, 'set_git_changed_files'):
            self.file_model.set_git_changed_files(changed_files)
        if hasattr(self, 'source_control_widget'):
            self.source_control_widget.refresh_status()

    def _get_git_changed_files_set(self):
        """Runs 'git status' and returns a set of absolute paths for modified files."""
        result = self._run_git_command(['git', 'status', '--porcelain'])
        changed = set()
        if result and result.stdout:
            for line in result.stdout.strip().splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    abs_path = Path(os.getcwd()) / parts[1].replace('"', '')
                    changed.add(abs_path.resolve())
        return changed

    def setup_powershell_backend(self):
        """Starts a persistent PowerShell process and a thread to read its output."""
        self.powershell_process = subprocess.Popen(
            ['powershell.exe', '-NoLogo', '-NoProfile', '-NoExit', '-Command', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            shell=True,
            bufsize=1 # Line-buffered
        )

        self.powershell_thread = QThread()
        self.worker = PowerShellWorker(self.powershell_process.stdout, self.output_queue)
        self.worker.moveToThread(self.powershell_thread)

        self.powershell_thread.started.connect(self.worker.run)
        self.powershell_thread.start()

        # Send initial commands to set directory and get the first prompt path
        self.powershell_process.stdin.write("cd C:\\\n")
        self.powershell_process.stdin.write("Write-Host \"PROMPT_PATH:$((Get-Location).Path)\"\n")
        self.powershell_process.stdin.flush()

    def load_code_from_file(self):
        """Opens a file dialog to load code into the editor."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Code File", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self._open_file_in_active_pane(file_name)

    def save_code_to_file(self):
        """Opens a file dialog to save the code from the editor."""
        editor = self.get_current_editor()
        if not editor: return
        
        file_path = editor.file_path
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self._create_local_history_snapshot(file_path)
            editor.document().setModified(False)
            self.statusBar().showMessage(f"Saved {file_path}", 3000)
            return True
        else:
            return self.save_as()

    def save_as(self):
        """Saves the current tab's content to a new file."""
        editor = self.get_current_editor()
        if not editor: return
        pane = self.active_editor_pane
        index = pane.currentIndex()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self._create_local_history_snapshot(file_name)
            editor.file_path = file_name
            editor.document().setModified(False)
            pane.setTabText(index, Path(file_name).name)
            self._add_to_recent_files(file_name)
            self.statusBar().showMessage(f"Saved to {file_name}", 3000)
            return True
        return False

    def _restore_file_content(self, file_path, content):
        """Finds the tab for a file and replaces its content."""
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if isinstance(widget, CodeEditor) and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    widget.setPlainText(content)
                    self.statusBar().showMessage(f"Restored content for {Path(file_path).name}", 3000)
                    return

    def copy_code_to_clipboard(self):
        """Copies the content of the code editor to the clipboard."""
        self._safe_editor_action(lambda e: QApplication.clipboard().setText(e.toPlainText()))

    def copy_terminal_output(self):
        """Copies the content of the terminal output to the clipboard."""
        QApplication.clipboard().setText(self.terminal_output.toPlainText())

    def _display_output(self, output, is_error=False):
        """Helper to format and display text in the code output view."""
        color = "#f44747" if is_error else "#bbbbbb"
        escaped_output = output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if is_error:
            # Highlight file paths in magenta, like in VS Code
            escaped_output = re.sub(
                r'(File &quot;[^&;]+&quot;)',
                r'<span style="color: #c586c0;">\1</span>',
                escaped_output
            )

        html_output = f"<pre style='color: {color}; font-family: Consolas, Courier New;'>{escaped_output}</pre>"
        self.output_view.setHtml(html_output)

    def run_code(self):
        """Executes the code in the editor based on the selected language."""
        editor = self.get_current_editor()
        if not editor: return
        code = editor.toPlainText()
        if not code.strip():
            self._display_output("No code to run.", is_error=False)
            return

        language = self.language_selector.currentText()

        dispatch_map = {
            "Python": self.run_python,
            "JavaScript": lambda c: self.run_script(c, "node"),
            "TypeScript": self.run_typescript,
            "PHP": lambda c: self.run_script(c, "php"),
            "Go": self.run_go,
            "Java": self.run_java,
            "C++": self.run_cpp,
            "C#": self.run_csharp,
            "Rust": self.run_rust,
            "Visual Basic": self.run_vb,
            "Nebula": self.run_nebula,
            "Batch": self.run_shell,
            "PowerShell": self.run_powershell,
            "HTML": self.run_html,
        }

        runner = dispatch_map.get(language)
        if runner:
            try:
                runner(code)
            except FileNotFoundError as e:
                self._display_output(f"Error: Command '{e.filename}' not found. Is it installed and in your system's PATH?", is_error=True)
            except subprocess.TimeoutExpired:
                self._display_output("Error: Execution timed out.", is_error=True)
            except Exception as e:
                self._display_output(f"An unexpected error occurred: {e}", is_error=True)
        else:
            self._display_output(f"Language '{language}' not supported for execution.", is_error=True)

    def _transpile_nebula_for_preview(self, code: str) -> str:
        """Transpiles Nebula code into executable Python UI code."""
        # This is a simplified transpiler based on the user's runner.
        # It does not create a full GUI, just prepares the code for execution.
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'import from .*?;', '', code)
        code = re.sub(r'NJson\s+(\w+)\s*{', r'\1 = {', code)
        code = re.sub(r'let ', '', code)
        code = re.sub(r'static Init {.*?}', '', code, flags=re.DOTALL)
        code = code.replace('&__app__(start)', '')
        code = code.replace(';', '')

        # Convert UI blocks to use helper classes
        code = code.replace("VWindow(", "NebulaWindow(")
        code = code.replace("VLayout.vertical(", "NebulaVLayout('vertical',")
        code = code.replace("VLayout.horizontal(", "NebulaVLayout('horizontal',")
        code = code.replace("VLabel(", "NebulaLabel(")
        code = code.replace("VButton(", "NebulaButton(")

        code = code.replace('if __name__ = "__main__"', 'if __name__ == "__main__":')
        return code.strip()



    def _transpile_nebula(self, code: str) -> str:
        # This is a simplified transpiler based on the user's runner.
        # It does not create a full GUI, just prepares the code for execution.
        code = re.sub(r'#.*', '', code)
        code = re.sub(r'import from .*?;', '', code)
        code = re.sub(r'NJson\s+(\w+)\s*{', r'\1 = {', code)
        code = re.sub(r'let ', '', code)
        code = re.sub(r'static Init {.*?}', '', code, flags=re.DOTALL)
        code = code.replace('&__app__(start)', '')
        code = code.replace(';', '')

        # For running in the editor, replace UI components with print statements
        code = re.sub(r"VWindow\((.*?)\)", r"print('--- Creating VWindow ---\n\1\n--------------------')", code, flags=re.DOTALL)
        code = re.sub(r"VLayout\.vertical\((.*?)\)", r"print('--- Creating VLayout.vertical ---\n\1\n--------------------')", code, flags=re.DOTALL)
        code = re.sub(r"VLayout\.horizontal\((.*?)\)", r"print('--- Creating VLayout.horizontal ---\n\1\n--------------------')", code, flags=re.DOTALL)
        code = re.sub(r"VLabel\((.*?)\)", r"print(f'--- Creating VLabel with text: {\1}')", code)
        code = re.sub(r"VButton\((.*?)\)", r"print(f'--- Creating VButton with properties: {\1}')", code)

        code = code.replace('if __name__ = "__main__"', 'if __name__ == "__main__":')
        return code.strip()

    def _format_nebula_error(self, exc: Exception, code: str) -> str:
        import traceback
        tb = traceback.extract_tb(exc.__traceback__)
        code_lines = code.splitlines()
        
        for frame in reversed(tb):
            if frame.filename == "<string>":
                ln = frame.lineno
                code_line = code_lines[ln - 1] if ln <= len(code_lines) else ''
                exc_name = type(exc).__name__
                error_str = f'File "<nebula_source>", line {ln}\n'
                error_str += f'  {code_line}\n'
                error_str += f'[NRE] {exc_name}: {exc}'
                return error_str
        return f"[NRE] {type(exc).__name__}: {exc}", -1, 1

    def run_nebula(self, code: str, preview_only=False):
        """Transpiles and runs Nebula code."""
        if preview_only:
            try:
                python_code = self._transpile_nebula_for_preview(code)
                if "NebulaWindow" not in python_code:
                    self.nebula_preview.set_preview_widget(None) # No UI to preview
                    return

                env = {
                    'NebulaWindow': NebulaWindow, 'NebulaVLayout': NebulaVLayout,
                    'NebulaLabel': NebulaLabel, 'NebulaButton': NebulaButton
                }
                exec(python_code, env)
                
                preview_widget = None
                for v in env.values():
                    if isinstance(v, QWidget) and not isinstance(v, (NebulaPreviewWidget, CodeRunnerApp)):
                        preview_widget = v
                        break
                self.nebula_preview.set_preview_widget(preview_widget)
            except Exception as e:
                self.nebula_preview.show_error(str(e))
            return

        try:
            python_code = self._transpile_nebula(code)
            header = "--- Transpiled to Python ---\n"
            
            from io import StringIO
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            try:
                exec(python_code, {})
            finally:
                sys.stdout = old_stdout

            execution_output = redirected_output.getvalue()
            self._display_output(header + python_code + "\n\n--- Execution Output ---\n" + execution_output)
            self._update_problems_panel(self.get_current_editor().file_path, []) # Clear errors on success
        except Exception as e:
            error_str, line_num, _ = self._format_nebula_error(e, code)
            self._display_output(error_str, is_error=True)
            
            # Update problems panel with the runtime error
            if line_num != -1:
                problem = {'line': line_num, 'col': 1, 'msg': str(e), 'severity': 'error'}
                self._update_problems_panel(self.get_current_editor().file_path, [problem])

    def run_script(self, code: str, interpreter: str):
        """Executes a script using a given interpreter via stdin."""
        result = subprocess.run(
            [interpreter, "-"], input=code, capture_output=True, text=True, timeout=10
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_typescript(self, code: str):
        """Compiles and runs a TypeScript program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.ts"
            source_path.write_text(code, encoding='utf-8')
            js_path = Path(tempdir) / "source.js"

            # Compile TypeScript to JavaScript
            compile_proc = subprocess.run(
                ['tsc', str(source_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            # Run the resulting JavaScript file
            self.run_script(f'require("{js_path.as_posix()}");', "node")

    def run_go(self, code: str):
        """Compiles and runs a Go program using 'go run'."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(code)
            source_path = temp_file.name
        try:
            result = subprocess.run(
                ['go', 'run', source_path], capture_output=True, text=True, timeout=20
            )
            self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)
        finally:
            os.remove(source_path)

    def run_java(self, code: str):
        """Compiles and runs a Java program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "Main.java"
            source_path.write_text(code, encoding='utf-8')

            compile_proc = subprocess.run(
                ['javac', str(source_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            run_proc = subprocess.run(
                ['java', 'Main'], cwd=tempdir, capture_output=True, text=True, timeout=10
            )
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def _compile_and_run(self, code, ext, compile_cmd, exe_name="source.exe"):
        """Generic helper to compile and run languages that produce an .exe."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / f"source{ext}"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / exe_name

            compile_proc = subprocess.run(
                compile_cmd + [str(source_path), '/out:' + str(exe_path)],
                capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            run_proc = subprocess.run(
                [str(exe_path)], capture_output=True, text=True, timeout=10
            )
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_cpp(self, code: str):
        """Compiles and runs a C++ program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.cpp"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / "source.exe"
            compile_proc = subprocess.run(
                ['g++', str(source_path), '-o', str(exe_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return
            run_proc = subprocess.run([str(exe_path)], capture_output=True, text=True, timeout=10)
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_csharp(self, code: str):
        """Compiles and runs a C# program."""
        self._compile_and_run(code, '.cs', ['csc'])

    def run_rust(self, code: str):
        """Compiles and runs a Rust program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.rs"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / "source.exe"
            compile_proc = subprocess.run(
                ['rustc', str(source_path), '-o', str(exe_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return
            run_proc = subprocess.run([str(exe_path)], capture_output=True, text=True, timeout=10)
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_vb(self, code: str):
        """Compiles and runs a Visual Basic program."""
        self._compile_and_run(code, '.vb', ['vbc'])

    def run_powershell(self, code: str):
        """Executes a PowerShell script and displays the output."""
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-Command', code],
            capture_output=True, text=True, timeout=15
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_python(self, code: str):
        """Executes a Python script in a subprocess and displays the output."""
        # sys.executable ensures we use the same Python interpreter that runs the app
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, timeout=10
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_html(self, code: str):
        """Renders HTML code directly in the web view."""
        self.output_view.setHtml(code)

    def run_shell(self, command: str):
        """Executes a shell command and displays the output."""
        # Using shell=True allows execution of shell built-ins (e.g., 'dir', 'echo').
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def format_terminal_output(self, text, is_error=False):
        """Formats text with HTML for rich color display in the terminal."""
        # Escape base HTML characters
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if is_error:
            text = f"<span style='color: #f44747;'>{text}</span>"
            # Highlight file paths in magenta
            text = re.sub(
                r'(File\s+)(&quot;[^&;]+&quot;)',
                r'\1<span style="color: #c586c0;">\2</span>',
                text
            )
        else:
            # Highlight PowerShell-like variables ($...) in green
            text = re.sub(r'(\$\w+)', r'<span style="color: #98c379;">\1</span>', text)
            # Highlight single-quoted strings in blue
            text = re.sub(r"('[^']+')", r'<span style="color: #569cd6;">\1</span>', text)

        return text
    def run_terminal_command(self, command=None, from_user=True):
        """Executes the command from the input line in the integrated terminal."""
        command_to_run = command if command is not None else self.command_input.text().strip()
        if from_user:
            self.command_input.clear()

        if not command_to_run: return

        safe_path = self.current_path.replace("<", "&lt;").replace(">", "&gt;")
        prompt_html = f"<span style='color: #bbbbbb;'>PS {safe_path}&gt; </span><span style='color: #dcdcaa;'>{command_to_run}</span>"
        self.terminal_output.append(prompt_html)
        self.powershell_process.stdin.write(command_to_run + '\n')
        self.powershell_process.stdin.write("Write-Host \"PROMPT_PATH:$((Get-Location).Path)\"\n")
        self.powershell_process.stdin.flush()
    def _process_output_queue(self):
        if self.output_queue.empty():
            return
        lines = []
        while not self.output_queue.empty():
            try:
                lines.append(self.output_queue.get_nowait())
            except queue.Empty:
                break
        output_html = []
        for line in lines:
            
                if not attr.startswith('__'):
                    self._populate_tree(item, attr, attr_val)

class SymbolVisitor(ast.NodeVisitor):
    """Traverses an AST to build a symbol table."""
    def __init__(self):
        self.symbols = {}

    def visit_ClassDef(self, node):
        methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
        self.symbols[node.name] = {'type': 'class', 'methods': methods}
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.symbols[node.name] = {'type': 'function'}
        self.generic_visit(node)

class LocalHistoryDialog(QDialog):
    """A dialog to view and restore previous versions of a file."""
    def __init__(self, file_path, current_content, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.file_path = file_path
        self.current_content = current_content

        self.setWindowTitle(f"Local History for {Path(file_path).name}")
        self.setMinimumSize(900, 700)

        self.layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Horizontal)

        # History List
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.addWidget(QLabel("Snapshots:"))
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.ExtendedSelection)
        history_layout.addWidget(self.history_list)
        self.splitter.addWidget(history_widget)

        # Diff View
        diff_widget = QWidget()
        diff_layout = QVBoxLayout(diff_widget)
        diff_layout.addWidget(QLabel("Changes:"))
        self.diff_view = QTextEdit()
        self.diff_view.setReadOnly(True)
        self.diff_view.setFont(QFont("Fira Code", 10))
        diff_layout.addWidget(self.diff_view)
        self.splitter.addWidget(diff_widget)

        self.splitter.setSizes([250, 650])
        self.layout.addWidget(self.splitter)

        self.restore_button = QPushButton("Restore this version")
        self.layout.addWidget(self.restore_button, 0, Qt.AlignRight)

        self.populate_history()

        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.currentItemChanged.connect(self.show_diff)
        self.restore_button.clicked.connect(self.restore_version)
        self.history_list.customContextMenuRequested.connect(self.show_history_context_menu)

    def populate_history(self):
        history_dir = self.parent_app._get_local_history_path(self.file_path)
        if not history_dir.exists():
            self.history_list.addItem("No history found.")
            self.restore_button.setEnabled(False)
            return
        
        snapshots = sorted(history_dir.glob('*.snapshot'), reverse=True)
        for snapshot in snapshots:
            dt_obj = datetime.strptime(snapshot.stem, "%Y-%m-%dT%H-%M-%S")
            item = QListWidgetItem(dt_obj.strftime("%Y-%m-%d %H:%M:%S"))
            item.setData(Qt.UserRole, str(snapshot))
            self.history_list.addItem(item)

    def show_diff(self, current, previous):
        if not current: return
        snapshot_path = Path(current.data(Qt.UserRole))
        old_content = snapshot_path.read_text(encoding='utf-8').splitlines()
        new_content = self.current_content.splitlines()
        diff = difflib.unified_diff(old_content, new_content, fromfile="snapshot", tofile="current", lineterm='')
        diff_text = "\n".join(list(diff))
        self.diff_view.setPlainText(diff_text if diff_text else "No changes from this version.")

    def restore_version(self):
        current_item = self.history_list.currentItem()
        if not current_item: return
        if QMessageBox.question(self, "Confirm Restore", "This will overwrite the current content in the editor. Are you sure?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            snapshot_path = Path(current_item.data(Qt.UserRole))
            content = snapshot_path.read_text(encoding='utf-8')
            self.parent_app._restore_file_content(self.file_path, content)
            self.accept()

    def show_history_context_menu(self, point):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            return

        menu = QMenu()

        # Action for single selection
        delete_action = menu.addAction("Delete Snapshot")
        if len(selected_items) != 1:
            delete_action.setEnabled(False)

        # Action for two selections
        compare_action = menu.addAction("Compare Snapshots")
        if len(selected_items) != 2:
            compare_action.setEnabled(False)

        action = menu.exec_(self.history_list.mapToGlobal(point))

        if action == delete_action:
            self.delete_snapshot(selected_items[0])
        elif action == compare_action:
            self.compare_snapshots(selected_items)

    def delete_snapshot(self, item):
        snapshot_path = Path(item.data(Qt.UserRole))
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to permanently delete this snapshot?\n\n{snapshot_path.name}",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                snapshot_path.unlink()
                self.populate_history() # Repopulate to refresh the list
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete snapshot: {e}")

    def compare_snapshots(self, items):
        path1 = Path(items[0].data(Qt.UserRole))
        path2 = Path(items[1].data(Qt.UserRole))

        # Ensure path1 is the older one for a consistent diff direction
        if path1.stem > path2.stem:
            path1, path2 = path2, path1

        content1 = path1.read_text(encoding='utf-8').splitlines()
        content2 = path2.read_text(encoding='utf-8').splitlines()

        diff = difflib.unified_diff(content1, content2, fromfile=path1.name, tofile=path2.name, lineterm='')
        diff_text = "\n".join(list(diff))

        dialog_title = f"Comparing Snapshots"
        dialog = DiffViewDialog(diff_text, dialog_title, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

class InheritanceEdge(QGraphicsLineItem):
    """A line with an arrowhead for showing inheritance."""
    def __init__(self, source_node, dest_node, parent=None):
        super().__init__(parent)
        self.source = source_node
        self.dest = dest_node
        self.arrow_head = QPolygonF()
        self.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        self.setZValue(-1)

    def update_position(self):
        line = QLineF(self.source.pos(), self.dest.pos())
        self.setLine(line)
        import math
        angle = math.atan2(-line.dy(), line.dx())
        arrow_size = 15
        p1 = line.p2()
        p2 = p1 - QPointF(math.cos(angle + math.pi / 6) * arrow_size, math.sin(angle + math.pi / 6) * arrow_size)
        p3 = p1 - QPointF(math.cos(angle - math.pi / 6) * arrow_size, math.sin(angle - math.pi / 6) * arrow_size)
        self.arrow_head = QPolygonF([p1, p2, p3])

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(Qt.white))
        painter.drawPolygon(self.arrow_head)

class Edge(QGraphicsLineItem):
    """A line connecting two graph nodes."""
    def __init__(self, source_node, dest_node, parent=None):
        super().__init__(parent)
        self.source = source_node
        self.dest = dest_node
        self.setPen(QPen(Qt.white, 1, Qt.DashLine))
        self.setZValue(-1) # Draw edges behind nodes

    def update_position(self):
        line = QLineF(self.source.pos(), self.dest.pos())
        self.setLine(line)

class GraphNode(QGraphicsItemGroup):
    """A draggable node for the call graph."""
    def __init__(self, name, lineno, parent=None):
        super().__init__(parent)
        self.name = name
        self.edge_list = []
        self.lineno = lineno

        self.ellipse = QGraphicsEllipseItem(-40, -15, 80, 30, self)
        self.ellipse.setBrush(QBrush(QColor("#3c3f41")))
        self.ellipse.setPen(QPen(Qt.white))
        
        self.text = QGraphicsTextItem(name, self)
        self.text.setDefaultTextColor(Qt.white)
        self.text.setPos(-self.text.boundingRect().width() / 2, -self.text.boundingRect().height() / 2)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edge_list:
                edge.update_position()
        return super().itemChange(change, value)

class ClassNode(QGraphicsItemGroup):
    """A draggable node representing a class for the class diagram."""
    def __init__(self, class_name, attributes, methods, lineno, parent=None):
        super().__init__(parent)
        font = QFont("Segoe UI", 9)
        self.edge_list = []
        self.lineno = lineno
        header_font = QFont("Segoe UI", 10, QFont.Bold)
        
        name_metrics = QFontMetrics(header_font)
        line_metrics = QFontMetrics(font)
        
        max_attr_width = max([line_metrics.width(a) for a in attributes] or [0])
        max_meth_width = max([line_metrics.width(m + "()") for m in methods] or [0])
        name_width = name_metrics.width(class_name)
        width = max(name_width, max_attr_width, max_meth_width) + 20
        
        self.name_text = QGraphicsTextItem(class_name)
        self.name_text.setFont(header_font)
        self.name_text.setDefaultTextColor(Qt.white)
        self.name_text.setPos(10, 5)

        y_pos = self.name_text.boundingRect().height() + 10
        
        self.attr_text = QGraphicsTextItem("\n".join(attributes))
        self.attr_text.setFont(font)
        self.attr_text.setDefaultTextColor(Qt.white)
        self.attr_text.setPos(10, y_pos)

        y_pos += self.attr_text.boundingRect().height() + 5

        self.meth_text = QGraphicsTextItem("\n".join([m + "()" for m in methods]))
        self.meth_text.setFont(font)
        self.meth_text.setDefaultTextColor(Qt.white)
        self.meth_text.setPos(10, y_pos)

        height = self.meth_text.boundingRect().bottom() + 10

        self.rect = QGraphicsRectItem(0, 0, width, height)
        self.rect.setBrush(QBrush(QColor("#3c3f41")))
        self.rect.setPen(QPen(Qt.white))

        line1_y = self.name_text.boundingRect().height() + 8
        self.sep1 = QGraphicsLineItem(0, line1_y, width, line1_y)
        self.sep1.setPen(QPen(Qt.white))

        line2_y = self.attr_text.boundingRect().bottom() + 8
        self.sep2 = QGraphicsLineItem(0, line2_y, width, line2_y)
        self.sep2.setPen(QPen(Qt.white))

        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.sep1)
        self.addToGroup(self.attr_text)
        self.addToGroup(self.sep2)
        self.addToGroup(self.meth_text)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edge_list:
                edge.update_position()
        return super().itemChange(change, value)

class CallGraphVisitor(ast.NodeVisitor):
    """Traverses an AST to build a function call graph."""
    def __init__(self):
        self.graph = {}
        self.stack = []
        self.locations = {}

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        if node.name not in self.graph:
            self.graph[node.name] = set()
        self.generic_visit(node)
        self.stack.pop()
        self.locations[node.name] = node.lineno

    def visit_Call(self, node):
        if self.stack:
            caller = self.stack[-1]
            callee = None
            if isinstance(node.func, ast.Name):
                callee = node.func.id
            elif isinstance(node.func, ast.Attribute):
                # This handles method calls like `self.my_method()`
                # For simplicity, we'll just use the attribute name.
                callee = node.func.attr
            
            if callee:
                self.graph[caller].add(callee)
        self.generic_visit(node)

class ClassDiagramVisitor(ast.NodeVisitor):
    """Traverses an AST to find classes and their members."""
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        class_name = node.name
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        self.classes[class_name] = {'attributes': [], 'methods': [], 'lineno': node.lineno, 'bases': bases}
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                self.classes[class_name]['methods'].append(body_item.name)
            elif isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        self.classes[class_name]['attributes'].append(target.id)
            elif isinstance(body_item, ast.AnnAssign):
                if isinstance(body_item.target, ast.Name):
                    self.classes[class_name]['attributes'].append(body_item.target.id)

class CodeVisualizerWidget(QWidget):
    """A sidebar widget to visualize code structure."""
    node_selected = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("CodeVisualizerWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.diagram_type_combo = QComboBox()
        self.diagram_type_combo.addItems(["Call Graph", "Class Diagram"])
        generate_btn = QPushButton("Generate")
        export_btn = QPushButton("Export to PNG")
        toolbar_layout.addWidget(self.diagram_type_combo)
        toolbar_layout.addWidget(generate_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)

        # Graphics View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.view)

        # Connections
        generate_btn.clicked.connect(self.generate_visualization)
        export_btn.clicked.connect(self.export_to_png)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)

    def generate_visualization(self):
        editor = self.parent_app.get_current_editor()
        if not editor or self.parent_app.language_selector.currentText() != "Python":
            QMessageBox.warning(self, "Unsupported", "Code visualization is currently only supported for Python.")
            return

        code = editor.toPlainText()
        diagram_type = self.diagram_type_combo.currentText()
        
        try:
            if diagram_type == "Call Graph":
                tree = ast.parse(code)
                visitor = CallGraphVisitor()
                visitor.visit(tree)
                self.render_call_graph(visitor.graph, visitor.locations)
            elif diagram_type == "Class Diagram":
                tree = ast.parse(code)
                visitor = ClassDiagramVisitor()
                visitor.visit(tree)
                self.render_class_diagram(visitor.classes)
        except SyntaxError as e:
            QMessageBox.critical(self, "Syntax Error", f"Cannot generate graph due to a syntax error:\n{e}")

    def render_call_graph(self, graph_data, locations):
        self.scene.clear()
        if not graph_data: return

        all_nodes = set(graph_data.keys())
        for callees in graph_data.values():
            all_nodes.update(callees)

        node_items = {}
        import math
        radius = 200; center_x, center_y = 250, 250; angle_step = (2 * math.pi) / len(all_nodes) if all_nodes else 0
        for i, name in enumerate(sorted(list(all_nodes))):
            angle = i * angle_step
            x, y = center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)
            lineno = locations.get(name)
            node = GraphNode(name, lineno)
            node.setPos(x, y)
            self.scene.addItem(node)
            node_items[name] = node

        for caller, callees in graph_data.items():
            for callee in callees:
                if caller in node_items and callee in node_items:
                    source_node = node_items[caller]
                    dest_node = node_items[callee]
                    edge = Edge(source_node, dest_node)
                    self.scene.addItem(edge)
                    source_node.add_edge(edge)
                    dest_node.add_edge(edge)
                    edge.update_position()

    def render_class_diagram(self, class_data):
        self.scene.clear()
        if not class_data: return
        node_items = {}
        x, y = 20, 20
        for name, data in class_data.items():
            node = ClassNode(name, data['attributes'], data['methods'], data['lineno'])
            node.setPos(x, y)
            self.scene.addItem(node)
            node_items[name] = node
            x += node.boundingRect().width() + 20
            if x > self.view.width() - 150:
                x = 20; y += 250

        # Second pass to draw inheritance edges
        for name, data in class_data.items():
            for base_name in data.get('bases', []):
                if name in node_items and base_name in node_items:
                    source_node = node_items[name] # Child
                    dest_node = node_items[base_name] # Parent
                    edge = InheritanceEdge(source_node, dest_node)
                    self.scene.addItem(edge)
                    source_node.add_edge(edge)
                    dest_node.add_edge(edge)
                    edge.update_position()

    def export_to_png(self):
        if self.scene.itemsBoundingRect().isNull():
            QMessageBox.warning(self, "Export Error", "Please generate a diagram before exporting.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "PNG Image (*.png)")
        if not file_path:
            return

        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        image.save(file_path)
        painter.end()
        self.parent_app.statusBar().showMessage(f"Diagram saved to {file_path}", 3000)

    def show_context_menu(self, point):
        item = self.view.itemAt(point)
        if not item:
            return

        node = item
        while node and not isinstance(node, (GraphNode, ClassNode)):
            node = node.parentItem()

        if node and hasattr(node, 'lineno') and node.lineno:
            menu = QMenu()
            go_to_def_action = menu.addAction("Go to Definition")
            action = menu.exec_(self.view.mapToGlobal(point))

            if action == go_to_def_action:
                self.node_selected.emit(node.lineno)

class CodeBlockEditorDialog(QDialog):
    def __init__(self, code_text, language, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.language = language
        self.setWindowTitle("Edit Code Block")
        self.setMinimumSize(800, 600)

        self.layout = QVBoxLayout(self)
        self.editor = CodeEditor()
        self.editor.setPlainText(code_text)
        self.layout.addWidget(self.editor)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        # Apply settings from main app
        if self.parent_app:
            self.parent_app._apply_editor_settings(self.editor)
            self.parent_app._update_syntax_highlighter(self.editor, self.language)

    def get_edited_text(self):
        return self.editor.toPlainText()

class TestRunnerWorker(QObject):
    """Worker thread for running tests."""
    test_finished = pyqtSignal(str, str, str) # test_id, status, output
    finished = pyqtSignal()

    def __init__(self, test_ids, project_root):
        super().__init__()
        self.test_ids = test_ids
        self.project_root = project_root

    def run(self):
        for test_id in self.test_ids:
            try:
                proc = subprocess.run(
                    [sys.executable, '-m', 'unittest', test_id],
                    cwd=self.project_root,
                    capture_output=True, text=True, timeout=30
                )
                output = proc.stdout + proc.stderr
                status = "passed" if "OK" in output.splitlines()[-1] else "failed"
                self.test_finished.emit(test_id, status, output)
            except Exception as e:
                self.test_finished.emit(test_id, "failed", f"Failed to run test: {e}")
        self.finished.emit()

class TestRunnerWidget(QWidget):
    """A sidebar widget for discovering and running tests."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setObjectName("TestRunnerWidget")
        self.test_items = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Toolbar
        toolbar_layout = QHBoxLayout()
        discover_btn = QPushButton("Discover Tests")
        self.run_all_btn = QPushButton("Run All")
        toolbar_layout.addWidget(discover_btn)
        toolbar_layout.addWidget(self.run_all_btn)
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)

        # Test Tree
        self.test_tree = QTreeView()
        self.test_tree.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.test_tree.setModel(self.model)
        self.test_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.test_tree)

        # Connections
        discover_btn.clicked.connect(self.discover_tests)
        self.run_all_btn.clicked.connect(self.run_all_tests)
        self.test_tree.customContextMenuRequested.connect(self._show_test_context_menu)

    def _show_test_context_menu(self, point):
        """Shows a context menu for a test item."""
        index = self.test_tree.indexAt(point)
        if not index.isValid(): return

        item = self.model.itemFromIndex(index)
        if not item: return

        menu = QMenu()
        run_action = menu.addAction("Run")
        
        action = menu.exec_(self.test_tree.viewport().mapToGlobal(point))

        if action == run_action:
            test_ids = self._get_all_test_ids_from_item(item)
            if test_ids:
                self.run_tests(test_ids)

    def _get_all_test_ids_from_item(self, start_item):
        """Recursively collects all test IDs from a starting item and its children."""
        test_ids = []
        stack = [start_item]
        while stack:
            current_item = stack.pop()
            if not current_item.hasChildren():
                test_id = current_item.data(Qt.UserRole)
                if test_id: test_ids.append(test_id)
            else:
                for row in range(current_item.rowCount()):
                    stack.append(current_item.child(row))
        return test_ids

    def discover_tests(self):
        self.model.clear()
        self.test_items.clear()
        loader = unittest.TestLoader()
        suite = loader.discover(os.getcwd(), pattern='test_*.py')
        self._populate_tree(suite, self.model.invisibleRootItem())

    def _populate_tree(self, suite, parent_item):
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                suite_item = QStandardItem(test.id().split('.')[-1])
                suite_item.setEditable(False)
                suite_item.setData(test.id(), Qt.UserRole)
                parent_item.appendRow(suite_item)
                self.test_items[test.id()] = suite_item
                self._populate_tree(test, suite_item)
            else:
                test_name = test.id().split('.')[-1]
                test_item = QStandardItem(test_name)
                test_item.setEditable(False)
                test_item.setData(test.id(), Qt.UserRole)
                parent_item.appendRow(test_item)
                self.test_items[test.id()] = test_item

    def run_all_tests(self):
        test_ids = [key for key, val in self.test_items.items() if val.hasChildren() == False]
        self.run_tests(test_ids)

    def run_tests(self, test_ids):
        self.worker = TestRunnerWorker(test_ids, os.getcwd())
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.test_finished.connect(self.on_test_finished)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_test_finished(self, test_id, status, output):
        item = self.test_items.get(test_id)
        if not item: return
        icon = QIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton if status == 'passed' else QStyle.SP_DialogCancelButton))
        item.setIcon(icon)
        item.setToolTip(output)

class GitCherryPickDialog(QDialog):
    """A dialog to select a commit to cherry-pick."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Cherry-Pick a Commit")
        self.setMinimumSize(700, 400)
        self.selected_commit_hash = None

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Select a commit to apply to the current branch:"))
        
        self.commit_list = QListWidget()
        self.commit_list.setFont(QFont("Fira Code", 10))
        self.layout.addWidget(self.commit_list)
        
        self.cherry_pick_button = QPushButton("Cherry-Pick")
        self.layout.addWidget(self.cherry_pick_button)
        
        self.populate_commits()
        
        self.cherry_pick_button.clicked.connect(self.accept_selection)
        self.commit_list.itemDoubleClicked.connect(self.accept_selection)

    def populate_commits(self):
        self.commit_list.clear()
        # Format: hash|author|date|subject
        result = self.parent_app._run_git_command(['git', 'log', '--pretty=format:%h|%an|%ar|%s', '-n', '100'])
        if not result or not result.stdout:
            self.commit_list.addItem("Could not load commit history.")
            self.cherry_pick_button.setEnabled(False)
            return
        
        for line in result.stdout.strip().splitlines():
            parts = line.split('|', 3)
            item = QListWidgetItem(f"{parts[0]} - {parts[3]} ({parts[1]}, {parts[2]})")
            item.setData(Qt.UserRole, parts[0]) # Store hash
            self.commit_list.addItem(item)

    def accept_selection(self):
        selected_items = self.commit_list.selectedItems()
        if selected_items:
            self.selected_commit_hash = selected_items[0].data(Qt.UserRole)
            self.accept()

class TaskManagerDialog(QDialog):
    """A dialog to display system processes and resource usage."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(800, 600)
        
        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        self.timer = QTimer(self)
        self.timer.setInterval(3000) # Refresh every 3 seconds
        self.timer.timeout.connect(self.update_view)
        self.timer.start()
        
        self.update_view()

    def update_view(self):
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
            try:
                p.cpu_percent(interval=0.01); procs.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        
        procs.sort(key=lambda x: x.info['cpu_percent'], reverse=True)
        html = self._generate_html(procs)
        self.web_view.setHtml(html, baseUrl=QUrl("file://"))

    def _generate_html(self, procs):
        is_dark = self.palette().window().color().lightness() < 128
        bg_color, text_color, header_bg, border_color = ("#2b2b2b", "#bbbbbb", "#3c3f41", "#555555") if is_dark else ("#f0f0f0", "#000000", "#e1e1e1", "#cccccc")
        rows = ""
        for p in procs[:100]: # Limit to top 100 processes
            try:
                mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                rows += f"<tr><td>{p.info['pid']}</td><td>{p.info['name']}</td><td>{p.info['username'] or 'N/A'}</td><td>{p.info['cpu_percent']:.1f}%</td><td>{mem_mb:.1f} MB</td></tr>"
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError): continue
        return f"""<html><head><style>
                body {{ font-family: Segoe UI, sans-serif; background-color: {bg_color}; color: {text_color}; }}
                table {{ width: 100%; border-collapse: collapse; }} th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid {border_color}; }}
                thead {{ background-color: {header_bg}; }}
            </style></head><body><h2>Processes</h2><table><thead><tr><th>PID</th><th>Name</th><th>User</th><th>CPU</th><th>Memory</th></tr></thead>
                <tbody>{rows}</tbody></table></body></html>"""

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

class AstViewer(QWidget):
    """A widget to display a Python Abstract Syntax Tree."""
    node_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)
        self.layout.addWidget(self.tree_view)

        self.tree_view.doubleClicked.connect(self.on_node_activated)

    def clear(self):
        self.model.clear()

    def update_ast(self, source_code):
        self.clear()
        try:
            tree = ast.parse(source_code)
            self._populate_tree(self.model.invisibleRootItem(), tree)
        except SyntaxError as e:
            self.model.appendRow(QStandardItem(f"SyntaxError: {e.msg}"))

    def _populate_tree(self, parent_item, node):
        node_text = node.__class__.__name__
        item = QStandardItem(node_text); item.setEditable(False)
        if hasattr(node, 'lineno'): item.setData(node.lineno, Qt.UserRole)
        parent_item.appendRow(item)
        for child_node in ast.iter_child_nodes(node): self._populate_tree(item, child_node)

    def on_node_activated(self, index: QModelIndex):
        line_num = self.model.data(index, Qt.UserRole)
        if line_num: self.node_selected.emit(line_num)

class GitCommitDialog(QDialog):
    """A dialog for staging and committing Git changes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Commit Changes")
        self.setMinimumSize(700, 500)

        # --- Layouts ---
        main_layout = QVBoxLayout(self)
        h_splitter = QSplitter(Qt.Horizontal)

        # --- Unstaged Files ---
        unstaged_widget = QWidget()
        unstaged_layout = QVBoxLayout(unstaged_widget)
        unstaged_layout.addWidget(QLabel("Unstaged Changes:"))
        self.unstaged_list = QListWidget()
        self.unstaged_list.setSelectionMode(QListWidget.ExtendedSelection)
        unstaged_layout.addWidget(self.unstaged_list)
        h_splitter.addWidget(unstaged_widget)

        # --- Staging Buttons ---
        staging_buttons_layout = QVBoxLayout()
        staging_buttons_layout.addStretch()
        self.stage_button = QPushButton(" > ")
        self.stage_button.setToolTip("Stage Selected")
        self.unstage_button = QPushButton(" < ")
        self.unstage_button.setToolTip("Unstage Selected")
        staging_buttons_layout.addWidget(self.stage_button)
        staging_buttons_layout.addWidget(self.unstage_button)
        staging_buttons_layout.addStretch()
        staging_widget = QWidget()
        staging_widget.setLayout(staging_buttons_layout)
        h_splitter.addWidget(staging_widget)

        # --- Staged Files ---
        staged_widget = QWidget()
        staged_layout = QVBoxLayout(staged_widget)
        staged_layout.addWidget(QLabel("Staged Changes:"))
        self.staged_list = QListWidget()
        self.staged_list.setSelectionMode(QListWidget.ExtendedSelection)
        staged_layout.addWidget(self.staged_list)
        h_splitter.addWidget(staged_widget)
        
        h_splitter.setSizes([300, 50, 300])
        main_layout.addWidget(h_splitter)

        # --- Commit Message ---
        main_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message_input = QTextEdit()
        self.commit_message_input.setFixedHeight(100)
        main_layout.addWidget(self.commit_message_input)

        # --- Commit Button ---
        self.commit_button = QPushButton("Commit")
        main_layout.addWidget(self.commit_button, 0, Qt.AlignRight)

        # --- Connections ---
        self.stage_button.clicked.connect(self.stage_selected)
        self.unstage_button.clicked.connect(self.unstage_selected)
        self.commit_button.clicked.connect(self.commit_changes)
        self.unstaged_list.itemDoubleClicked.connect(self.stage_selected)
        self.staged_list.itemDoubleClicked.connect(self.unstage_selected)

        self.populate_files()

    def populate_files(self):
        self.unstaged_list.clear(); self.staged_list.clear()
        result = self.parent_app._run_git_command(['git', 'status', '--porcelain'])
        if not result or not result.stdout: return
        for line in result.stdout.strip().splitlines():
            status, file_path = line[:2], line[3:]
            item = QListWidgetItem(file_path); item.setData(Qt.UserRole, file_path)
            if status[1] in ('M', 'D', 'A', '?'): self.unstaged_list.addItem(item)
            if status[0] in ('M', 'A', 'D'): self.staged_list.addItem(QListWidgetItem(item))

    def stage_selected(self): self._move_items(self.unstaged_list, ['git', 'add'])
    def unstage_selected(self): self._move_items(self.staged_list, ['git', 'reset', 'HEAD', '--'])
    def _move_items(self, source_list, command):
        for item in source_list.selectedItems() or [source_list.item(i) for i in range(source_list.count())]:
            self.parent_app._run_git_command(command + [item.data(Qt.UserRole)])
        self.populate_files()

    def commit_changes(self):
        message = self.commit_message_input.toPlainText().strip()
        if not message: QMessageBox.warning(self, "Commit Error", "Commit message cannot be empty."); return
        if self.staged_list.count() == 0: QMessageBox.warning(self, "Commit Error", "There are no staged changes to commit."); return
        result = self.parent_app._run_git_command(['git', 'commit', '-m', message])
        if result and result.returncode == 0: self.parent_app.statusBar().showMessage("Commit successful.", 3000); self.accept()
        elif result: QMessageBox.critical(self, "Commit Failed", f"Error committing changes:\n\n{result.stderr}")
        else: QMessageBox.critical(self, "Commit Failed", "Failed to execute 'git commit' command.")

class IconFileSystemModel(QFileSystemModel):
    """A custom file system model that provides file icons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_provider = QFileIconProvider()
        self.changed_files = set()

    def set_git_changed_files(self, files_set):
        self.changed_files = files_set
        # A bit heavy, but ensures all visible items are re-evaluated for styling.
        self.layoutChanged.emit()

    def data(self, index, role):
        # Provide an icon for the first column
        if role == Qt.DecorationRole and index.column() == 0:
            file_info = self.fileInfo(index)
            return self.icon_provider.icon(file_info)
        
        if role == Qt.ForegroundRole and index.column() == 0:
            file_path = self.filePath(index)
            if Path(file_path).resolve() in self.changed_files:
                return QColor("#E2C08D") # Git-modified color (yellowish)

        return super().data(index, role)

class FileFilterProxyModel(QSortFilterProxyModel):
    """A proxy model to filter files and directories in the QTreeView."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def filterAcceptsRow(self, source_row, source_parent):
        # Get the index for the item in the source model
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        if not source_index.isValid():
            return False

        # 1. Always accept if the filter is empty
        filter_string = self.filterRegularExpression().pattern()
        if not filter_string:
            return True

        # 2. Check if the current item's name matches
        file_name = self.sourceModel().fileName(source_index)
        if self.filterRegularExpression().match(file_name).hasMatch():
            return True

        # 3. If it's a directory, check if any of its children match
        if self.sourceModel().isDir(source_index):
            for i in range(self.sourceModel().rowCount(source_index)):
                if self.filterAcceptsRow(i, source_index):
                    return True
        
        return False

class LineNumberArea(QWidget):
    """A widget to display line numbers for a CodeEditor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def mousePressEvent(self, event):
        """Handles clicks on the line number area, for folding."""
        self.codeEditor.toggle_fold_at_line(event.y())

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class MiniMap(QWidget):
    """A widget that displays a scaled-down overview of the code editor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        if not self.editor:
            return

        painter = QPainter(self)
        doc = self.editor.document()
        
        # Mini-map drawing parameters
        line_height = 2
        char_width = 1
        max_width = self.width()

        # Simple colors for syntax
        theme = self.editor.palette().window().color() # Get background color to decide on minimap colors
        if theme.lightness() < 128: # Dark theme
            comment_color = QColor("#6A9955")
            string_color = QColor("#ce9178")
            keyword_color = QColor("#569cd6")
            default_color = QColor(187, 187, 187, 150)
        else: # Light theme
            comment_color = QColor(0, 128, 0)
            string_color = QColor(163, 21, 21)
            keyword_color = QColor(0, 0, 255)
            default_color = QColor(50, 50, 50, 150)

        block = doc.firstBlock()
        block_num = 0
        while block.isValid():
            y = block_num * line_height
            text = block.text().lstrip()
            stripped_text = text.strip()
            indent = (len(block.text()) - len(text)) * char_width
            
            color = default_color
            if stripped_text.startswith(('#', '//', '/*')):
                color = comment_color
            elif stripped_text.startswith(('"', "'", "`")):
                color = string_color
            elif stripped_text.startswith(('def ', 'class ', 'function ')):
                color = keyword_color

            painter.setPen(color)
            painter.drawLine(indent, y, min(max_width, indent + len(text) * char_width), y)
            
            block = block.next()
            block_num += 1
            if y > self.height():
                break

        # Draw the visible area rectangle
        scrollbar = self.editor.verticalScrollBar()
        if scrollbar.maximum() > 0:
            scroll_fraction_start = scrollbar.value() / scrollbar.maximum()
            scroll_fraction_size = scrollbar.pageStep() / scrollbar.maximum()
            
            visible_rect_y = scroll_fraction_start * self.height()
            visible_rect_height = scroll_fraction_size * self.height()
            
            painter.fillRect(self.rect().adjusted(0, int(visible_rect_y), 0, -(self.height() - int(visible_rect_y + visible_rect_height))), QColor(128, 128, 128, 80))

    def _scroll_editor(self, event):
        """Scrolls the main editor based on the mouse position on the minimap."""
        y = event.y()
        scrollbar = self.editor.verticalScrollBar()
        target_value = (y / self.height()) * scrollbar.maximum()
        scrollbar.setValue(int(target_value))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._scroll_editor(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._scroll_editor(event)

class CodeEditor(QPlainTextEdit):
    """A QPlainTextEdit subclass with line numbers and current line highlighting."""
    modification_changed = pyqtSignal(bool)
    problems_found = pyqtSignal(str, list)
    bookmarks_changed = pyqtSignal(set)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.lineNumberArea = LineNumberArea(self)
        self.minimap = MiniMap(self)
        self._setup_completer()

        self.encoding = 'UTF-8'
        self.line_ending = 'LF'

        self.indent_style = 'space'
        self.indent_size = 4
        self.problems = []
        self.bookmarks = set()
        self.extra_cursors = []
        self.folding_regions = {}
        self.collapsed_blocks = set()

        # Snippet state
        self.in_snippet_mode = False
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

        # Settings toggles
        self.highlight_current_line = True
        self.show_visible_whitespace = False
        self.rounded_line_highlight = False

        self.folding_scan_timer = QTimer(self)
        self.folding_scan_timer.setSingleShot(True)
        self.folding_scan_timer.setInterval(500) # Debounce folding scan
        self.folding_scan_timer.timeout.connect(self.update_folding_regions)

        self.linter_timer = QTimer(self)
        self.linter_timer.setSingleShot(True)
        self.linter_timer.setInterval(750) # Debounce linter
        self.linter_timer.timeout.connect(self.run_linter)

        self.nebula_preview_timer = QTimer(self)
        self.nebula_preview_timer.setSingleShot(True)
        self.nebula_preview_timer.setInterval(1000) # Debounce preview
        self.nebula_preview_timer.timeout.connect(self._run_nebula_preview)

        self.textChanged.connect(self._on_text_changed)

        self.symbol_scan_timer = QTimer(self)
        self.symbol_scan_timer.setSingleShot(True)
        self.symbol_scan_timer.setInterval(1500) # Less frequent than linter
        self.symbol_scan_timer.timeout.connect(self._run_symbol_scan)

        self.update_folding_regions() # Initial scan

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self._update_extra_selections)
        self.document().modificationChanged.connect(self.modification_changed.emit)

        # Connect signals for minimap
        self.verticalScrollBar().valueChanged.connect(self.minimap.update)
        self.textChanged.connect(self.minimap.update)

        self.updateLineNumberAreaWidth(0)
        self._update_extra_selections()

    def _on_text_changed(self):
        """Handles text changes for multiple features."""
        self.folding_scan_timer.start()
        self.linter_timer.start()
        self.symbol_scan_timer.start()
        main_window = self.window()
        if isinstance(main_window, CodeRunnerApp):
            language = main_window.language_selector.currentText()
            if language == "Nebula":
                self.nebula_preview_timer.start()

    def set_visible_whitespace(self, enabled):
        """Sets whether to show visible whitespace characters."""
        self.show_visible_whitespace = enabled
        self.viewport().update() # Trigger a repaint

    def paintEvent(self, event):
        """Override paintEvent to draw extra cursors and visible whitespace."""
        # Custom rounded highlight for the current line
        if self.highlight_current_line and self.rounded_line_highlight and not self.textCursor().hasSelection():
            painter = QPainter(self.viewport())
            theme_bg = self.palette().base().color()
            lineColor = theme_bg.lighter(115) if theme_bg.lightness() < 128 else theme_bg.darker(105)
            rect = self.cursorRect()
            rect.setX(2)
            rect.setWidth(self.viewport().width() - 4)
            painter.fillRect(rect, QBrush(lineColor))
        super().paintEvent(event)
        painter = QPainter(self.viewport())

        # Draw extra cursors
        color = self.palette().text().color()
        painter.setPen(color)
        for cursor in self.extra_cursors:
            rect = self.cursorRect(cursor)
            painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

        # Draw visible whitespace
        if self.show_visible_whitespace:
            self._draw_whitespace(painter, event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events, primarily for showing tooltips for problems."""
        pos = event.pos()
        cursor = self.cursorForPosition(pos)
        line_num = cursor.blockNumber() + 1
        for problem in self.problems:
            if problem['line'] == line_num:
                QToolTip.showText(self.mapToGlobal(pos), problem['msg'], self)
                return
        QToolTip.hideText()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.modifiers() & Qt.AltModifier:
            # Add a new cursor
            cursor = self.cursorForPosition(event.pos())
            self.extra_cursors.append(cursor)
            self.viewport().update() # Force a repaint
            event.accept()
        else:
            # Clear extra cursors on a normal click
            if self.extra_cursors:
                self.extra_cursors.clear()
                self.viewport().update() # Force a repaint
            # Let the base class handle the event to move the main cursor
            super().mousePressEvent(event)

    def _draw_whitespace(self, painter, event):
        """Draws dots for spaces and arrows for tabs."""
        ws_color = self.palette().text().color()
        ws_color.setAlpha(80)
        painter.setPen(ws_color)
        font_metrics = self.fontMetrics()
        space_width = font_metrics.horizontalAdvance(' ')

        block = self.firstVisibleBlock()

        while block.isValid() and block.geometry().top() <= event.rect().bottom():
            if block.isVisible() and block.geometry().bottom() >= event.rect().top():
                text = block.text()
                cursor = QTextCursor(block)
                for i, char in enumerate(text):
                    if char == ' ':
                        cursor.setPosition(block.position() + i)
                        rect = self.cursorRect(cursor)
                        if event.rect().intersects(rect):
                            center_y, center_x = rect.center().y(), rect.left() + space_width // 2
                            painter.drawPoint(center_x, center_y)
                    elif char == '\t':
                        cursor.setPosition(block.position() + i)
                        rect = self.cursorRect(cursor)
                        if event.rect().intersects(rect):
                            center_y = rect.center().y()
                            painter.drawLine(rect.left() + 2, center_y, rect.right() - 2, center_y)
                            painter.drawLine(rect.right() - 4, center_y - 2, rect.right() - 2, center_y)
                            painter.drawLine(rect.right() - 4, center_y + 2, rect.right() - 2, center_y)
            block = block.next()

    def _update_completer_model(self):
        """Updates the completer's word list from the document content."""
        text = self.toPlainText()
        words = sorted(list(set(re.findall(r'\b\w{3,}\b', text))))
        self.word_model.setStringList(words)

    def textUnderCursor(self):
        """Gets the word currently under the text cursor."""
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def insert_completion(self, completion):
        """Inserts the selected completion, replacing the current prefix."""
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def insert_indent(self):
        """Inserts an indent (spaces or tab) based on current settings."""
        cursor = self.textCursor()
        if self.indent_style == 'space':
            cursor.insertText(' ' * self.indent_size)
        else:
            cursor.insertText('\t')

    def remove_indent(self):
        """Removes an indent level from the current line."""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        pos_in_block = cursor.positionInBlock()
        cursor.movePosition(QTextCursor.StartOfLine)
        
        # Check the text at the start of the line for an indent to remove
        if self.indent_style == 'space':
            for _ in range(self.indent_size):
                cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
                if cursor.selectedText() != ' ':
                    cursor.clearSelection(); break
            if cursor.selectedText().isspace(): cursor.removeSelectedText()
        else: # tab
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            if cursor.selectedText() == '\t': cursor.removeSelectedText()
        cursor.endEditBlock()

    def duplicate_line(self):
        """Duplicates the line(s) containing the current cursor(s)."""
        all_cursors = [self.textCursor()] + self.extra_cursors
        # To handle multiple cursors on the same line, we only care about unique blocks
        blocks_to_duplicate = sorted(list(set(c.block() for c in all_cursors)), key=lambda b: b.blockNumber(), reverse=True)
        self.document().beginEditBlock()
        for block in blocks_to_duplicate:
            text_to_duplicate = block.text()
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfBlock)
            cursor.insertText('\n' + text_to_duplicate)
        self.document().endEditBlock()

    def keyPressEvent(self, event):
        # Snippet mode takes precedence for Tab and Escape keys
        if self.in_snippet_mode and event.key() == Qt.Key_Tab:
            self.jump_to_next_placeholder(); return
        if self.in_snippet_mode and event.key() == Qt.Key_Escape:
            self.exit_snippet_mode(); return

        # If multi-cursor is active, try to handle the key event and exit if successful.
        if self.extra_cursors:
            if self._handle_multi_cursor_key_press(event):
                event.accept()
                return

        # Handle custom tab/indentation logic
        if event.key() == Qt.Key_Tab:
            if not self.try_expand_snippet():
                self.insert_indent()
            return
        if event.key() == Qt.Key_Backtab:
            self.remove_indent()
            return

        # If not in multi-cursor mode or the key wasn't handled (e.g., Escape),
        # proceed with normal single-cursor logic.
        # Handle completer activation
        if self.completer.popup().isVisible() and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.completer.popup().hide()
            self.insert_completion(self.completer.currentCompletion())
            return

        # Default key press handling
        super().keyPressEvent(event)

        # Logic to show the completer popup
        # (Don't show if multi-cursor is active, even if the key was a fallback)
        if self.extra_cursors:
            return

        if event.text() == '.':
            self._trigger_member_completion()
            return # Don't show normal completer

        prefix = self.textUnderCursor()
        if len(prefix) < 2 or event.text().isspace() or not event.text():
            self.completer.popup().hide()
            return # Don't show completer for short prefixes or after spaces

        self.completer.setCompletionPrefix(prefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def try_expand_snippet(self):
        """Checks if the word before the cursor is a snippet and expands it."""
        cursor = self.textCursor()
        if cursor.hasSelection(): return False

        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        prefix = cursor.selectedText()

        main_window = self.window()
        if isinstance(main_window, CodeRunnerApp) and prefix in main_window.snippets:
            snippet_body = main_window.snippets[prefix]['body']
            cursor.removeSelectedText()
            self.expand_snippet(snippet_body)
            return True
        return False

    def expand_snippet(self, body):
        """Inserts a snippet and prepares for tab-stop navigation."""
        cursor = self.textCursor()
        self.in_snippet_mode = True
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

        # Find all placeholders like ${1:default}
        placeholder_pattern = re.compile(r'\$(\{\d+(:[^}]*)?\})')
        
        # Store placeholder info before modifying the body
        start_pos = cursor.position()
        placeholders = []
        for match in placeholder_pattern.finditer(body):
            full_match, content = match.group(0), match.group(1)
            parts = content.strip('{}').split(':', 1)
            index = int(parts[0])
            default_text = parts[1] if len(parts) > 1 else ""
            placeholders.append({'index': index, 'default': default_text, 'match_obj': match})

        # Sort by index number
        placeholders.sort(key=lambda p: p['index'])

        # Replace placeholders in body and calculate final positions
        final_body = body
        offset = 0
        for p in placeholders:
            match = p['match_obj']
            final_body = final_body.replace(match.group(0), p['default'], 1)
            self.snippet_placeholders.append({'pos': start_pos + match.start() - offset, 'len': len(p['default'])})
            offset += len(match.group(0)) - len(p['default'])

        cursor.insertText(final_body)
        self.jump_to_next_placeholder()

    def jump_to_next_placeholder(self):
        self.current_placeholder_index += 1
        if self.current_placeholder_index >= len(self.snippet_placeholders):
            self.exit_snippet_mode(); return

        placeholder = self.snippet_placeholders[self.current_placeholder_index]
        cursor = self.textCursor()
        cursor.setPosition(placeholder['pos'])
        cursor.setPosition(placeholder['pos'] + placeholder['len'], QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def exit_snippet_mode(self):
        self.in_snippet_mode = False
        self.snippet_placeholders = []
        self.current_placeholder_index = -1

    def _handle_multi_cursor_key_press(self, event):
        """Processes a key press for all active cursors. Returns True if handled."""
        all_cursors = [self.textCursor()] + self.extra_cursors

        # --- Text Editing (Insertion/Deletion) ---
        if event.text() or event.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            # Sort cursors in reverse order to prevent edit positions from invalidating subsequent cursors.
            sorted_cursors = sorted(all_cursors, key=lambda c: c.position(), reverse=True)
            self.document().beginEditBlock()
            for cursor in sorted_cursors:
                if event.text(): cursor.insertText(event.text())
                elif event.key() == Qt.Key_Backspace: cursor.deletePreviousChar()
                elif event.key() == Qt.Key_Delete: cursor.deleteChar()
            self.document().endEditBlock()
            self.setTextCursor(sorted_cursors[0]); self.extra_cursors = sorted_cursors[1:]
            self.viewport().update()
            return True

        # --- Navigation and Selection ---
        move_mode = QTextCursor.KeepAnchor if event.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
        op_map = {Qt.Key_Left: QTextCursor.Left, Qt.Key_Right: QTextCursor.Right, Qt.Key_Up: QTextCursor.Up,
                  Qt.Key_Down: QTextCursor.Down, Qt.Key_Home: QTextCursor.StartOfLine, Qt.Key_End: QTextCursor.EndOfLine}
        move_op = op_map.get(event.key())
        if move_op is not None:
            for cursor in all_cursors: cursor.movePosition(move_op, move_mode)
            self.setTextCursor(all_cursors[0]); self.extra_cursors = all_cursors[1:]
            self.viewport().update()
            return True

        return False # Key was not handled by multi-cursor logic.

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        space += 15 # Add space for folding markers
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        # Position the line number area
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
        # Position the minimap
        minimap_width = 80
        self.minimap.setGeometry(cr.right() - minimap_width, cr.top(), minimap_width, cr.height())

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), self.palette().base().color().lighter(110))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                # Draw folding marker if this is a fold point
                if blockNumber in self.folding_regions:
                    painter.setPen(QColor("#8e8e8e"))
                    marker = "▶" if blockNumber in self.collapsed_blocks else "▼"
                    painter.drawText(5, top, 15, self.fontMetrics().height(), Qt.AlignCenter, marker)

                # Draw bookmark icon
                if blockNumber in self.bookmarks:
                    painter.setPen(QColor("#569cd6"))
                    # A simple bookmark icon
                    bookmark_poly = QPolygon([
                        QPoint(5, top + 2),
                        QPoint(self.lineNumberArea.width() - 20, top + 2),
                        QPoint(self.lineNumberArea.width() - 20, top + 12),
                        QPoint(self.lineNumberArea.width() - 25, top + 8),
                        QPoint(5, top + 12)
                    ])
                    painter.drawText(self.lineNumberArea.width() - 18, top, 15, self.fontMetrics().height(), Qt.AlignCenter, "B")

                painter.setPen(QColor("#6e7681"))
                painter.drawText(0, top, self.lineNumberArea.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def _update_extra_selections(self):
        """Manages all extra selections, like current line and bracket matching."""
        selections = []

        # 1. Current line highlighting
        if not self.isReadOnly() and not self.textCursor().hasSelection():
            use_standard_highlight = self.highlight_current_line and not self.rounded_line_highlight
            if use_standard_highlight:
                selection = QTextEdit.ExtraSelection()
                theme_bg = self.palette().base().color()
                lineColor = theme_bg.lighter(115) if theme_bg.lightness() < 128 else theme_bg.darker(105)

                selection.format.setBackground(lineColor)
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.cursor = self.textCursor()
                selection.cursor.clearSelection()
                selections.append(selection)

        # 2. Bracket matching
        match_selections = self._find_bracket_match()
        if match_selections:
            selections.extend(match_selections)

        # 3. Linter error highlighting
        error_format = QTextCharFormat()
        error_format.setUnderlineColor(Qt.red)
        error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        warning_format = QTextCharFormat()
        warning_format.setUnderlineColor(QColor("#FFC107")) # Amber/Yellow
        warning_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        for problem in self.problems:
            selection = QTextEdit.ExtraSelection()
            selection.format = error_format if problem['severity'] == 'error' else warning_format
            block = self.document().findBlockByNumber(problem['line'] - 1)
            if block.isValid():
                selection.cursor = QTextCursor(block)
                selections.append(selection)

        self.setExtraSelections(selections)

    def _setup_completer(self):
        """Initializes the code completer."""
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.word_model = QStringListModel()
        self.completer.setModel(self.word_model)
        self.textChanged.connect(self._update_completer_model)
        self.completer.activated.connect(self.insert_completion)

    def _find_bracket_match(self):
        """Finds matching brackets and returns ExtraSelection objects for them."""
        cursor = self.textCursor()
        if cursor.hasSelection(): return None

        pos = cursor.position()
        doc = self.document()
        
        matching_pairs = {'(': ')', '{': '}', '[': ']'}
        reverse_pairs = {v: k for k, v in matching_pairs.items()}
        
        # Check character BEFORE the cursor
        if pos > 0:
            char_before = doc.characterAt(pos - 1)
            if char_before in matching_pairs:
                return self._find_match_forward(pos - 1, char_before, matching_pairs[char_before])

        # Check character AT/AFTER the cursor
        char_after = doc.characterAt(pos)
        if char_after in reverse_pairs:
            return self._find_match_backward(pos, char_after, reverse_pairs[char_after])
            
        return None

    def _find_match_forward(self, start_pos, open_char, match_char):
        doc = self.document(); open_count = 1; search_pos = start_pos + 1
        while search_pos < doc.characterCount():
            char = doc.characterAt(search_pos)
            if char == open_char: open_count += 1
            elif char == match_char:
                open_count -= 1
                if open_count == 0: return self._create_bracket_selections(start_pos, search_pos)
            search_pos += 1
        return None

    def _find_match_backward(self, start_pos, close_char, match_char):
        doc = self.document(); close_count = 1; search_pos = start_pos - 1
        while search_pos >= 0:
            char = doc.characterAt(search_pos)
            if char == close_char: close_count += 1
            elif char == match_char:
                close_count -= 1
                if close_count == 0: return self._create_bracket_selections(search_pos, start_pos)
            search_pos -= 1
        return None

    def _create_bracket_selections(self, pos1, pos2):
        selections = []
        fmt = QTextCharFormat()
        theme = self.palette().window().color()
        color = QColor(80, 80, 80, 200) if theme.lightness() < 128 else QColor(200, 200, 200, 200)
        fmt.setBackground(color)
        for p in [pos1, pos2]:
            sel = QTextEdit.ExtraSelection()
            sel.format = fmt
            cursor = self.textCursor(); cursor.setPosition(p)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            sel.cursor = cursor
            selections.append(sel)
        return selections

    def run_linter(self):
        """Checks Python code for syntax errors and updates highlighting."""
        main_window = self.window()
        if not isinstance(main_window, CodeRunnerApp):
            return

        language = main_window.language_selector.currentText()
        code = self.toPlainText()

        if not code.strip():
            self.problems = []
            self.problems_found.emit(self.file_path or "Untitled", [])
            self._update_extra_selections()
            return

        if language == "Python":
            self._run_pyflakes_linter(code)
        elif language == "JavaScript":
            self._run_node_linter(code)
        else:
            # Clear problems for unsupported languages
            self.problems = []
            self.problems_found.emit(self.file_path or "Untitled", [])
            self._update_extra_selections()

    def _run_nebula_preview(self):
        main_window = self.window()
        if isinstance(main_window, CodeRunnerApp):
            main_window.run_nebula(self.toPlainText(), preview_only=True)

    def _run_pyflakes_linter(self, code):
        """Runs the pyflakes linter on the given Python code."""
        new_problems = []
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            proc = subprocess.run([sys.executable, '-m', 'pyflakes', temp_file_path], capture_output=True, text=True)
            os.unlink(temp_file_path)
            if proc.stdout:
                for line in proc.stdout.strip().splitlines():
                    parts = line.split(':', 3)
                    if len(parts) >= 3 and parts[1].isdigit():
                        lineno, msg = int(parts[1]), parts[-1].strip()
                        # Check for ignore comment
                        line_text = self.document().findBlockByNumber(lineno - 1).text()
                        if "# $IGNORE" in line_text:
                            continue # Skip this problem
                        severity = "error" if "undefined name" in msg or "invalid syntax" in msg else "warning"
                        problem = {'line': lineno, 'col': 1, 'msg': msg, 'severity': severity}
                        if "undefined name" in msg:
                            match = re.search(r"undefined name '([^']+)'", msg)
                            if match:
                                problem['symbol'] = match.group(1)
                                problem['quick_fix_type'] = 'import'
                        new_problems.append(problem)
        except Exception as e:
            print(f"Pyflakes linter failed: {e}")
        self.problems = new_problems
        self.problems_found.emit(self.file_path or "Untitled", self.problems)
        self._update_extra_selections()

    def _run_node_linter(self, code):
        """Runs the node.js syntax checker on the given JavaScript code."""
        new_problems = []
        try:
            proc = subprocess.run(['node', '--check'], input=code, capture_output=True, text=True, encoding='utf-8')
            if proc.returncode != 0 and proc.stderr:
                match = re.search(r'<anonymous>:(\d+)', proc.stderr)
                if match:
                    lineno = int(match.group(1))
                    line_text = self.document().findBlockByNumber(lineno - 1).text()
                    if "// $IGNORE" not in line_text:
                        msg = proc.stderr.strip().split('\n')[-1]
                        new_problems.append({'line': lineno, 'col': 1, 'msg': msg, 'severity': 'error'})
        except Exception as e:
            print(f"Node.js linter failed: {e}")
        self.problems = new_problems
        self.problems_found.emit(self.file_path or "Untitled", self.problems)
        self._update_extra_selections()

    def _run_symbol_scan(self):
        """Runs the AST symbol scanner on the current code."""
        main_window = self.window()
        if not isinstance(main_window, CodeRunnerApp) or self.parent().language_selector.currentText() != "Python":
            return

        code = self.toPlainText()
        if not code.strip():
            main_window.symbol_table = {}
            return

        try:
            tree = ast.parse(code)
            visitor = SymbolVisitor()
            visitor.visit(tree)
            main_window.symbol_table = visitor.symbols
            self._update_completer_model() # Refresh completer with new symbols
        except SyntaxError:
            pass # Ignore syntax errors, linter will catch them

    def update_folding_regions(self):
        """Scans the document for foldable regions based on indentation."""
        self.folding_regions.clear()
        indent_stack = [(0, -1)]  # (indent_level, line_number)
        block = self.document().firstBlock()
        block_num = 0
        while block.isValid():
            text = block.text()
            if text.strip():  # Only consider non-empty lines for folding
                indent = len(text) - len(text.lstrip())

                while indent <= indent_stack[-1][0] and len(indent_stack) > 1:
                    _start_indent, start_line = indent_stack.pop()
                    if block_num - 1 > start_line:
                        self.folding_regions[start_line] = block_num - 1

                if indent > indent_stack[-1][0]:
                    indent_stack.append((indent, block_num))

            block = block.next()
            block_num += 1

        # Close any remaining open blocks at the end of the file
        while len(indent_stack) > 1:
            _start_indent, start_line = indent_stack.pop()
            if block_num - 1 > start_line:
                self.folding_regions[start_line] = block_num - 1

        self.lineNumberArea.update()

    def toggle_fold_at_line(self, y_pos):
        """Finds the line number from a y-coordinate and toggles its fold state."""
        block = self.firstVisibleBlock()
        block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

        while block.isValid():
            block_bottom = block_top + self.blockBoundingRect(block).height()
            if block_top <= y_pos < block_bottom:
                line_num = block.blockNumber()
                if line_num in self.folding_regions:
                    self._toggle_fold_visibility(line_num)
                break
            block = block.next()
            block_top = block_bottom

    def _toggle_fold_visibility(self, start_line):
        """Hides or shows a block of code."""
        end_line = self.folding_regions.get(start_line, -1)
        if end_line == -1: return

        is_collapsing = start_line not in self.collapsed_blocks

        if is_collapsing: self.collapsed_blocks.add(start_line)
        else: self.collapsed_blocks.discard(start_line)

        block = self.document().findBlockByNumber(start_line).next()
        for i in range(start_line + 1, end_line + 1):
            if not block.isValid(): break
            block.setVisible(not is_collapsing)
            block = block.next()

        self.document().layout().update()
        self.lineNumberArea.update()

    def toggle_bookmark(self):
        """Toggles a bookmark on the current line."""
        line_num = self.textCursor().blockNumber()
        if line_num in self.bookmarks:
            self.bookmarks.remove(line_num)
        else:
            self.bookmarks.add(line_num)
        self.bookmarks_changed.emit(self.bookmarks)
        self.lineNumberArea.update()

    def next_bookmark(self):
        """Jumps the cursor to the next bookmark."""
        current_line = self.textCursor().blockNumber()
        sorted_bookmarks = sorted(list(self.bookmarks))
        for line in sorted_bookmarks:
            if line > current_line:
                self.go_to_line(line + 1)
                return
        # Wrap around to the first bookmark if at the end
        if sorted_bookmarks:
            self.go_to_line(sorted_bookmarks[0] + 1)

    def prev_bookmark(self):
        """Jumps the cursor to the previous bookmark."""
        current_line = self.textCursor().blockNumber()
        sorted_bookmarks = sorted(list(self.bookmarks), reverse=True)
        for line in sorted_bookmarks:
            if line < current_line:
                self.go_to_line(line + 1)
                return
        # Wrap around to the last bookmark if at the beginning
        if sorted_bookmarks:
            self.go_to_line(sorted_bookmarks[-1] + 1)

    def clear_bookmarks(self):
        """Removes all bookmarks from this editor."""
        self.bookmarks.clear()
        self.bookmarks_changed.emit(self.bookmarks)
        self.document().layout().update()
        self.lineNumberArea.update()

class FindReplaceWidget(QWidget):
    """A widget for finding and replacing text in a QTextEdit."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None
        self.setObjectName("FindReplaceWidget")
        self.setContentsMargins(5, 5, 5, 5)

        # --- Widgets ---
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace")

        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")

        self.case_sensitive_check = QCheckBox("Case Sensitive")
        self.whole_words_check = QCheckBox("Whole Words")

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("CloseFindBtn")

        # --- Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.find_input)
        input_layout.addWidget(self.replace_input)

        options_layout = QVBoxLayout()
        options_layout.addWidget(self.case_sensitive_check)
        options_layout.addWidget(self.whole_words_check)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(options_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.close_btn)

        # --- Connections ---
        self.close_btn.clicked.connect(self.hide)
        self.find_next_btn.clicked.connect(self.find_next)
        self.find_input.returnPressed.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace_one)
        self.replace_all_btn.clicked.connect(self.replace_all)

    def _get_find_flags(self):
        """Gets the search flags from the checkboxes."""
        flags = QTextDocument.FindFlags()
        if self.case_sensitive_check.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_words_check.isChecked():
            flags |= QTextDocument.FindWholeWords
        return flags

    def _unescape(self, text):
        """Interprets escape sequences like \t and \n."""
        return text.encode('utf-8').decode('unicode_escape')

    def find_next(self):
        find_text = self._unescape(self.find_input.text())
        if not find_text or not self.editor:
            return
        self.editor.find(find_text, self._get_find_flags())

    def replace_one(self):
        if not self.editor: return
        cursor = self.editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == self._unescape(self.find_input.text()):
            cursor.insertText(self._unescape(self.replace_input.text()))
        self.find_next()

    def replace_all(self):
        if not self.editor: return
        find_text = self._unescape(self.find_input.text())
        replace_text = self._unescape(self.replace_input.text())
        if not find_text: return

        # Use a cursor-based approach to preserve formatting
        document = self.editor.document()
        if not document: return
        cursor = QTextCursor(document)
        document.UndoStack().beginMacro("Replace All")
        while True:
            cursor = document.find(find_text, cursor, self._get_find_flags())
            if cursor.isNull(): break
            cursor.insertText(replace_text)
        document.UndoStack().endMacro()

class CodeRunnerApp(QMainWindow):
    """A desktop application for running code and shell commands."""

    def __init__(self):
        super().__init__()
        self.current_path = ""
        self.powershell_process = None
        self.powershell_thread = None
        self.output_queue = queue.Queue()

        self.profiles_dir = Path('.apicode') / 'profiles'
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.active_profile_path = self._get_active_profile_path()

        self.settings = {}
        self.highlighters = {}
        self.proxy_model = None
        self.recent_files = []
        self.snippets = {}
        self.tasks = {}
        self.debugger = None
        self.terminal_container = None # Will be set in init_ui
        self.all_problems = {} # {file_path: [problems]}
        self.profiles_menu = None
        self.editor_panes = []
        self.all_bookmarks = {} # {file_path: {line_num, ...}}
        self.file_to_compare = None
        self.active_editor_pane = None
        self.recent_files_actions = []
        self.untitled_counter = 1
        self.symbol_table = {} # For context-aware completion
        self.load_settings()
        self.init_ui()
        self.setAcceptDrops(True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.apply_settings() # Apply loaded settings on startup
        QApplication.instance().focusChanged.connect(self._on_focus_changed)
        self._setup_timers()
        self._create_rope_project(self.current_path)
        self._load_snippets()

    def _load_snippets(self):
        snippet_file = Path("snippets.json")
        if snippet_file.exists():
            with open(snippet_file, 'r') as f:
                self.snippets = json.load(f)

    def _create_rope_project(self, path):
        # This method is a placeholder for future rope integration
        # For now, it does nothing to avoid errors if rope isn't fully set up.
        pass

    def init_ui(self):
        self.setWindowTitle("APICode")
        self.setGeometry(150, 150, 900, 700)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setWindowIcon(QIcon("assets/apicode.ico"))
        self.file_menu = self.menuBar().addMenu("File")
        edit_menu = self.menuBar().addMenu("Edit")
        selection_menu = self.menuBar().addMenu("Selection")
        view_menu = self.menuBar().addMenu("View")
        go_menu = self.menuBar().addMenu("Go")
        git_menu = self.menuBar().addMenu("Git")
        run_menu = self.menuBar().addMenu("Run")
        help_menu = self.menuBar().addMenu("Help")
        self.new_file_action = QAction("New File", self)
        self.new_file_action.setShortcut("Ctrl+N")
        self.load_action = QAction("Open File...", self)
        self.new_profile_action = QAction("New Profile...", self)
        self.manage_profiles_action = QAction("Manage Profiles...", self)
        self.save_action = QAction("Save File...", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.settings_action = QAction("Settings...", self)
        self.local_history_action = QAction("Local History...", self)
        self.exit_action = QAction("Exit", self)
        self.close_all_tabs_action = QAction("Close All Tabs", self)
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.find_action = QAction("Find/Replace...", self)
        self.find_action.setShortcut("Ctrl+F")
        self.extract_block_action = QAction("Extract Code Block...", self)
        self.extract_block_action.setShortcut("Ctrl+Shift+E")
        self.move_line_up_action = QAction("Move Line Up", self)
        self.move_line_up_action.setShortcut("Alt+Up")
        self.move_line_down_action = QAction("Move Line Down", self)
        self.move_line_down_action.setShortcut("Alt+Down")
        self.format_document_action = QAction("Format Document", self)
        self.format_document_action.setShortcut("Shift+Alt+F")


        # Selection Menu Actions
        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut("Ctrl+A")

        # Case conversion actions
        self.to_upper_action = QAction("UPPER CASE", self)
        self.to_lower_action = QAction("lower case", self)
        self.to_title_action = QAction("Title Case", self)
        self.to_camel_action = QAction("camelCase", self)
        self.to_snake_action = QAction("snake_case", self)
        self.to_kebab_action = QAction("kebab-case", self)

        self.split_editor_action = QAction("Split Editor", self)
        # View Menu Actions
        self.word_wrap_action = QAction("Toggle Word Wrap", self)
        self.word_wrap_action.setCheckable(True)

        # Selection Menu Actions (continued)
        self.column_select_action = QAction("Column Selection Mode", self)
        self.column_select_action.setCheckable(True)

        # Case conversion actions
        self.to_upper_action = QAction("UPPER CASE", self)
        self.to_lower_action = QAction("lower case", self)
        self.to_title_action = QAction("Title Case", self)
        self.to_camel_action = QAction("camelCase", self)
        self.to_snake_action = QAction("snake_case", self)
        self.to_kebab_action = QAction("kebab-case", self)

        # Go Menu Actions
        self.go_to_line_action = QAction("Go to Line...", self)
        self.go_to_line_action.setShortcut("Ctrl+G")

        # Bookmark Actions
        self.toggle_bookmark_action = QAction("Toggle Bookmark", self)
        self.toggle_bookmark_action.setShortcut("Ctrl+F2")
        self.next_bookmark_action = QAction("Next Bookmark", self)
        self.next_bookmark_action.setShortcut("F2")
        self.prev_bookmark_action = QAction("Previous Bookmark", self)
        self.prev_bookmark_action.setShortcut("Shift+F2")
        self.clear_bookmarks_action = QAction("Clear All Bookmarks", self)


        # Command Palette
        self.command_palette_action = QAction("Command Palette...", self)
        self.command_palette_action.setShortcut("Ctrl+Shift+P")

        # Run/Help Menu Actions
        self.go_to_definition_action = QAction("Go to Definition", self)
        self.go_to_definition_action.setShortcut("F12")

        # Run/Help Menu Actions
        self.peek_definition_action = QAction("Peek Definition", self)
        self.peek_definition_action.setShortcut("Alt+F12")

        # Run/Help Menu Actions
        self.find_all_references_action = QAction("Find All References", self)
        self.find_all_references_action.setShortcut("Shift+F12")

        # Git Menu Actions
        self.manage_branches_action = QAction("Manage Branches...", self)
        self.commit_action = QAction("Commit...", self)
        self.commit_action.setShortcut("Ctrl+K")
        self.push_action = QAction("Push...", self)
        self.push_action.setShortcut("Ctrl+Shift+K")
        self.stash_action = QAction("Stash Changes...", self)
        self.apply_stash_action = QAction("Apply Latest Stash", self)
        self.stash_list_action = QAction("Stash List...", self)
        self.pull_action = QAction("Pull...", self)
        self.cherry_pick_action = QAction("Cherry-Pick...", self)
        self.git_log_action = QAction("Show Log...", self)


        self.pull_action.setShortcut("Ctrl+Shift+L")

        # View Menu Actions
        self.task_manager_action = QAction("Task Manager...", self)
        self.about_action = QAction("About APICode...", self)
        self.run_action = QAction("Run Code", self)
        self.go_to_symbol_action = QAction("Go to Symbol in File...", self)
        self.go_to_symbol_action.setShortcut("Ctrl+Shift+O")
        self.find_in_files_action = QAction("Find in Files...", self)
        self.find_in_files_action.setShortcut("Ctrl+Shift+F")
        self.check_for_updates_action = QAction("Check for Updates...", self)
        self.feedback_action = QAction("Submit Feedback...", self)

        # Debug Menu Actions
        self.start_debugging_action = QAction("Start Debugging", self)
        self.start_debugging_action.setShortcut("F5")
        self.toggle_breakpoint_action = QAction("Toggle Breakpoint", self)
        self.toggle_breakpoint_action.setShortcut("F9")

        # Populate Menus
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.load_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.local_history_action)
        self.recent_files_separator = self.file_menu.addSeparator()
        self.file_menu.addSeparator()
        self.profiles_menu = self.file_menu.addMenu("Profiles")
        self.new_profile_action.triggered.connect(self._create_new_profile)
        self.manage_profiles_action.triggered.connect(self._show_manage_profiles_dialog)
        self._update_profiles_menu()
        # The actions are added inside _update_profiles_menu to ensure correct order
        # self.profiles_menu.addSeparator()
        # self.profiles_menu.addAction(self.manage_profiles_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_all_tabs_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addAction(self.exit_action)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.find_in_files_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.duplicate_line_action)
        edit_menu.addAction(self.move_line_up_action)
        edit_menu.addAction(self.move_line_down_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.to_uppercase_action)
        edit_menu.addAction(self.to_lowercase_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.extract_block_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.format_document_action)

        selection_menu.addSeparator()
        selection_menu.addAction(self.select_all_action)
        selection_menu.addAction(self.column_select_action)
        selection_menu.addSeparator()
        selection_menu.addAction(self.move_line_up_action)
        selection_menu.addAction(self.move_line_down_action)


        view_menu.addAction(self.split_editor_action)
        theme_menu = view_menu.addMenu("Theme")
        self.theme_group = QActionGroup(self)
        for theme_name in sorted(THEME_PALETTES.keys()):
            action = theme_menu.addAction(theme_name)
            action.setCheckable(True)
            self.theme_group.addAction(action)
        view_menu.addSeparator()
        view_menu.addAction(self.command_palette_action)
        view_menu.addAction(self.task_manager_action)

        view_menu.addAction(self.word_wrap_action)
        go_menu.addAction(self.go_to_line_action)
        go_menu.addAction(self.go_to_definition_action)
        go_menu.addAction(self.peek_definition_action)
        go_menu.addSeparator()
        go_menu.addAction(self.toggle_bookmark_action)
        go_menu.addAction(self.next_bookmark_action)
        go_menu.addAction(self.prev_bookmark_action)
        go_menu.addAction(self.clear_bookmarks_action)
        go_menu.addSeparator()
        go_menu.addAction(self.find_all_references_action)

        git_menu.addAction(self.manage_branches_action)
        git_menu.addAction(self.commit_action)
        git_menu.addAction(self.push_action)
        git_menu.addSeparator()
        git_menu.addAction(self.stash_action)
        git_menu.addAction(self.apply_stash_action)
        git_menu.addAction(self.stash_list_action)
        git_menu.addSeparator()
        git_menu.addAction(self.cherry_pick_action)
        git_menu.addSeparator()
        git_menu.addAction(self.git_log_action)
        git_menu.addSeparator()
        git_menu.addAction(self.pull_action)
        run_menu.addAction(self.run_action)
        debug_menu.addAction(self.start_debugging_action)
        debug_menu.addSeparator()
        debug_menu.addAction(self.toggle_breakpoint_action)
        help_menu.addAction(self.check_for_updates_action)
        help_menu.addSeparator()
        help_menu.addAction(self.feedback_action)
        help_menu.addAction(self.about_action)

        # --- Widgets ---
        # Terminal Panel (self.terminal_container is set here)
        terminal_container = QWidget()
        terminal_container.setObjectName("TerminalContainer")

        self.terminal_output = QTextEdit()
        self.terminal_output.setObjectName("TerminalOutput")
        self.terminal_output.setContextMenuPolicy(Qt.CustomContextMenu)
        self.terminal_output.setReadOnly(True)

        self.command_input = QLineEdit()
        self.command_input.setObjectName("TerminalInput")
        self.command_input.setPlaceholderText("PS > Enter command...")

        # Code Runner Panel
        self.language_selector = QComboBox()
        self.language_selector.addItems([
            "Python",
            "JavaScript",
            "TypeScript",
            "Java",
            "C++",
            "C#",
            "Go",
            "Rust",
            "Nebula",
            "PHP",
            "Visual Basic",
            "Batch",
            "PowerShell",
            "HTML"
        ])
        self.language_selector.addItems(["HTML", "CSS"])

        self.output_view = QWebEngineView()
        self.output_view.setHtml(
            "<body style='background-color: #3c3f41; color: #bbbbbb; font-family: Segoe UI; padding: 5px;'>Code Output</body>"
        )
        self.copy_button = QPushButton("Copy")
        self.copy_button.setObjectName("CopyButton")

        self.editor_splitter = QSplitter(Qt.Horizontal)
        self.editor_splitter.setObjectName("EditorSplitter")

        # --- Layouts ---
        # Terminal Panel Layout
        terminal_layout = QVBoxLayout(terminal_container)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        
        terminal_button_bar = QHBoxLayout()
        terminal_button_bar.addStretch()
        self.copy_output_button = QPushButton("Copy Output")
        self.copy_output_button.setObjectName("CopyButton")
        terminal_button_bar.addWidget(self.copy_output_button)
        
        terminal_layout.addLayout(terminal_button_bar)
        terminal_layout.addWidget(self.terminal_output)
        terminal_layout.addWidget(self.command_input)

        # Code Editor side top bar (language selector)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.language_selector)

        # Code Editor side main content (editor and output)
        code_splitter = QSplitter(Qt.Vertical)
        code_splitter.addWidget(self.editor_splitter)

        # Code Editor button bar
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()

        # Breadcrumbs
        self.breadcrumb_bar = QWidget()
        self.breadcrumb_bar.setObjectName("BreadcrumbBar")
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_bar)
        self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)

        # Combine Code Editor side layouts
        self.find_widget = FindReplaceWidget(self)
        self.find_widget.hide()
        code_editor_layout = QVBoxLayout()
        code_editor_layout.insertWidget(0, self.find_widget)
        code_editor_layout.addWidget(self.breadcrumb_bar)
        editor_bottom_splitter = QSplitter(Qt.Vertical)
        editor_bottom_splitter.addWidget(self.editor_splitter)
        code_editor_layout.addWidget(editor_bottom_splitter)
        code_editor_layout.addLayout(button_layout)

        # --- File Explorer Layout ---
        file_explorer_layout = QVBoxLayout()
        file_explorer_layout.setContentsMargins(0, 0, 0, 0)
        file_explorer_layout.setSpacing(0)

        self.open_editors_label = QLabel("OPEN EDITORS")
        self.open_editors_label.setObjectName("OpenEditorsLabel")
        self.open_editors_list = QListWidget()
        self.open_editors_list.setObjectName("OpenEditorsList")

        file_explorer_layout.addWidget(self.open_editors_label)
        file_explorer_layout.addWidget(self.open_editors_list)

        file_explorer_toolbar = QHBoxLayout()
        file_explorer_toolbar.setSpacing(2)
        self.file_search_input = QLineEdit()
        self.file_search_input.setPlaceholderText("Search files...")
        self.file_search_input.setStyleSheet("padding: 5px; border-radius: 0; border-bottom: 1px solid #555555;")
        self.git_refresh_button = QPushButton("⟳")
        self.git_refresh_button.setToolTip("Refresh Git Status")
        self.git_refresh_button.setFixedSize(30, 30)
        self.git_refresh_button.setStyleSheet("padding: 4px;")
        file_explorer_toolbar.addWidget(self.file_search_input)
        file_explorer_toolbar.addWidget(self.git_refresh_button)
        
        file_explorer_widget = QWidget()
        file_explorer_widget.setLayout(file_explorer_layout)

        # --- Left Panel Tab Widget ---
        self.left_panel_tabs = QTabWidget()
        self.left_panel_tabs.addTab(file_explorer_widget, "Explorer")
        self.ast_viewer = AstViewer()
        self.left_panel_tabs.addTab(self.ast_viewer, "AST Explorer")

        # --- Outline & Bookmarks ---
        self.outline_widget = self.create_outline_bookmark_widget()
        self.left_panel_tabs.addTab(self.outline_widget, "Outline")

        # --- Code Visualizer ---
        self.visualizer_widget = CodeVisualizerWidget(self)
        self.left_panel_tabs.addTab(self.visualizer_widget, "Visualizer")

        # --- Variable Inspector ---
        self.variable_inspector = VariableInspectorWidget(self)
        self.left_panel_tabs.addTab(self.variable_inspector, "Variable Inspector")

        # --- File Explorer ---
        self.file_model = IconFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.proxy_model = FileFilterProxyModel()
        self.proxy_model.setSourceModel(self.file_model)
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.proxy_model)
        source_root_index = self.file_model.index(os.getcwd())
        proxy_root_index = self.proxy_model.mapFromSource(source_root_index)
        self.file_tree.setRootIndex(proxy_root_index)
        self.file_tree.setColumnWidth(0, 250) # Make the name column wider
        self.file_tree.hideColumn(1) # Hide size
        self.file_tree.hideColumn(2) # Hide type
        self.file_tree.hideColumn(3) # Hide date modified
        self.file_tree.setObjectName("FileTree")
        self.file_tree.setDragEnabled(True)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)

        file_explorer_layout.addLayout(file_explorer_toolbar)
        file_explorer_layout.addWidget(self.file_tree)

        # --- Main Content Splitter ---
        # This splitter separates the code editor from the terminal
        editor_terminal_splitter = QSplitter(Qt.Horizontal)

        # This splitter separates the file explorer from the rest of the UI
        body_splitter = QSplitter(Qt.Horizontal)
        body_splitter.addWidget(self.left_panel_tabs)
        body_splitter.addWidget(editor_terminal_splitter)
        body_splitter.setSizes([250, 750]) # Initial sizes for file tree and the rest

        main_layout.addWidget(body_splitter)

        # --- Status Bar ---
        self.setStatusBar(QStatusBar(self))
        self.cpu_label = QLabel("CPU: -% ")
        self.mem_label = QLabel("Mem: -% ")
        self.git_label = QLabel("") # This will be populated by _update_status_bar
        self.gpu_label = QLabel("GPU: -% ")
        self.indent_label = QLabel("")
        self.encoding_label = QLabel("")
        self.line_ending_label = QLabel("")

        self.statusBar().addPermanentWidget(self.encoding_label)
        self.statusBar().addPermanentWidget(self.line_ending_label)
        self.indent_label.hide()

        self.statusBar().addPermanentWidget(self.indent_label)
        self.git_label.setCursor(Qt.PointingHandCursor)
        self.git_label.mousePressEvent = lambda event: self._show_git_branch_dialog()
        self.statusBar().insertPermanentWidget(0, self.git_label)
        self.statusBar().addPermanentWidget(self.cpu_label)
        self.statusBar().addPermanentWidget(self.mem_label)
        self.statusBar().addPermanentWidget(self.gpu_label)

        # --- Connections ---
        self.new_file_action.triggered.connect(self._create_new_tab)
        self.run_action.triggered.connect(self.run_code)
        self.load_action.triggered.connect(self.load_code_from_file)
        self.save_action.triggered.connect(self.save_code_to_file)
        self.save_as_action.triggered.connect(self.save_as)
        self.settings_action.triggered.connect(self.show_settings_dialog)
        self.local_history_action.triggered.connect(self._show_local_history_dialog)
        self.close_all_tabs_action.triggered.connect(self._close_all_tabs)
        self.split_editor_action.triggered.connect(self._create_new_editor_pane)
        self.find_action.triggered.connect(self.show_find_widget)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.go_to_line_action.triggered.connect(self.go_to_line)
        self.command_palette_action.triggered.connect(self._show_command_palette)
        self.manage_branches_action.triggered.connect(self._show_git_branch_dialog)
        self.commit_action.triggered.connect(self._show_git_commit_dialog)
        self.push_action.triggered.connect(self._git_push)
        self.stash_action.triggered.connect(self._git_stash)
        self.apply_stash_action.triggered.connect(self._git_apply_stash)
        self.stash_list_action.triggered.connect(self._show_git_stash_dialog)
        self.cherry_pick_action.triggered.connect(self._show_git_cherry_pick_dialog)
        self.git_log_action.triggered.connect(self._show_git_log_dialog)
        self.pull_action.triggered.connect(self._git_pull)
        self.task_manager_action.triggered.connect(self._show_task_manager)
        self.go_to_definition_action.triggered.connect(self._go_to_definition)
        self.peek_definition_action.triggered.connect(self._peek_definition)
        self.find_all_references_action.triggered.connect(self._find_all_references)
        self.toggle_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.toggle_bookmark()))
        self.next_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.next_bookmark()))
        self.prev_bookmark_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.prev_bookmark()))
        self.clear_bookmarks_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.clear_bookmarks()))
        self.go_to_symbol_action.triggered.connect(self._show_go_to_symbol_dialog)
        self.find_in_files_action.triggered.connect(self._show_find_in_files_dialog)
        self.theme_group.triggered.connect(self._on_theme_changed)
        self.feedback_action.triggered.connect(self._show_feedback_dialog)
        self.go_to_symbol_action.triggered.connect(self._show_go_to_symbol_dialog)
        self.column_select_action.toggled.connect(self._toggle_column_select_info)
        self.exit_action.triggered.connect(self.close)
        self.word_wrap_action.triggered.connect(self.toggle_word_wrap)

        self.format_document_action.triggered.connect(self._format_document)
        self.extract_block_action.triggered.connect(self._show_extract_block_dialog)
        # Editor-specific actions
        self.undo_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.undo()))
        self.redo_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.redo()))
        self.cut_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.cut()))
        self.copy_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.copy()))
        self.paste_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.paste()))
        self.select_all_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.selectAll()))
        self.duplicate_line_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.duplicate_line()))
        self.to_uppercase_action.triggered.connect(lambda: self._safe_editor_action(lambda e: e.to_uppercase()))
        self.copy_button.clicked.connect(self.copy_code_to_clipboard)
        self.copy_output_button.clicked.connect(self.copy_terminal_output)
        self.command_input.returnPressed.connect(self.run_terminal_command)
        self.terminal_output.customContextMenuRequested.connect(self._show_terminal_context_menu)

        # --- Bottom Panel (Terminal, Output, Problems) ---
        self.bottom_tabs = QTabWidget()
        self.bottom_tabs.addTab(terminal_container, "Terminal")
        self.bottom_tabs.addTab(self.output_view, "Output")
        self.problems_table = QTableWidget()
        self.problems_table.setColumnCount(4)
        self.problems_table.setHorizontalHeaderLabels(["File", "Line", "Column", "Description"])
        self.problems_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.problems_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.problems_table.verticalHeader().setVisible(False)
        self.problems_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.problems_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bottom_tabs.addTab(self.problems_table, "Problems (0)")

        # Nebula Preview Panel
        self.nebula_preview = NebulaPreviewWidget(self)
        self.bottom_tabs.addTab(self.nebula_preview, "Nebula Preview")

        editor_bottom_splitter.addWidget(self.bottom_tabs)
        editor_bottom_splitter.setSizes([500, 200])

        self.open_editors_list.itemClicked.connect(self._on_open_editor_clicked)
        self.file_tree.doubleClicked.connect(self._open_file_from_tree)
        self.file_tree.customContextMenuRequested.connect(self._show_file_tree_context_menu)
        self.git_refresh_button.clicked.connect(self._update_git_status)
        self.ast_viewer.node_selected.connect(self.go_to_line)
        self.problems_table.cellDoubleClicked.connect(self._on_problem_activated)
        self.file_search_input.textChanged.connect(self._on_file_search_changed)

        self._create_new_editor_pane()
        self._update_recent_files_menu()
        # Set initial state
        self._create_new_tab() # Start with one empty tab
        self.terminal_container = terminal_container
        self.visualizer_widget.node_selected.connect(self.go_to_line)
        self.problems_table.customContextMenuRequested.connect(self._show_problems_context_menu)

    def dragEnterEvent(self, event):
        """Accepts drag events if they contain file URLs."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handles dropped files by opening them in new tabs."""
        for url in event.mimeData().urls():
            if url.isLocalFile():
                path = url.toLocalFile()
                if not Path(path).is_dir():
                    self._open_file(path)


    def _on_focus_changed(self, old, new):
        for pane in self.editor_panes:
            if new is pane or (new and new.parent() is pane):
                self.active_editor_pane = pane
                return

    def _safe_editor_action(self, action):
        """Executes an action on the current editor if it exists."""
        editor = self.get_current_editor()
        if editor:
            action(editor)

    def _on_tab_close_btn_clicked(self):
        btn = self.sender()
        parent = btn.parent()
        while parent:
            if isinstance(parent, QTabBar):
                tab_bar = parent
                break
            parent = parent.parent()
        else: return
        for i in range(tab_bar.count()):
            if tab_bar.tabButton(i, QTabBar.RightSide) == btn:
                tab_bar.parent().tabCloseRequested.emit(i)
                break

    def _create_new_editor_pane(self):
        pane = QTabWidget()
        pane.setMovable(True)
        pane.setContextMenuPolicy(Qt.CustomContextMenu)
        pane.setObjectName("CodeTabs")
        pane.currentChanged.connect(self._on_tab_changed)
        pane.tabCloseRequested.connect(self._close_tab)
        pane.customContextMenuRequested.connect(self._show_tab_context_menu)
        self.editor_splitter.addWidget(pane)
        self.editor_panes.append(pane)
        self.active_editor_pane = pane
        return pane

    def create_outline_bookmark_widget(self):
        """Creates the combined widget for Code Outline and Bookmarks."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        
        # Outline
        layout.addWidget(QLabel("OUTLINE"))
        self.outline_tree = QTreeView()
        self.outline_tree.setHeaderHidden(True)
        self.outline_model = QStandardItemModel()
        self.outline_tree.setModel(self.outline_model)
        self.outline_tree.doubleClicked.connect(self._on_outline_activated)

        # Bookmarks
        layout.addWidget(QLabel("BOOKMARKS"))
        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(self._on_bookmark_activated)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.outline_tree)
        splitter.addWidget(self.bookmark_list)
        splitter.setSizes([400, 200])

        layout.addWidget(splitter)
        return widget


    def _create_image_tab(self, file_path):
        """Creates a new tab with an ImageViewer."""
        viewer = ImageViewer(file_path)
        tab_title = Path(file_path).name

        pane = self.active_editor_pane
        if not pane and self.editor_panes:
            pane = self.editor_panes[0]
        index = pane.addTab(viewer, tab_title)
        pane.setCurrentIndex(index)

        # Add custom close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("TabCloseButton")
        close_btn.setCursor(Qt.PointingHandCursor)
        pane.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)
        close_btn.clicked.connect(self._on_tab_close_btn_clicked)

        self._on_tab_changed(index)
        self._update_open_editors_list()

    def _create_new_tab(self, checked=False, file_path=None, content=""):
        editor = CodeEditor()
        editor.setPlaceholderText("Enter your code here...")
        editor.file_path = file_path
        editor.setPlainText(content)
        editor.document().setModified(False) # Start in a clean state

        if file_path:
            path = Path(file_path)
            tab_title = path.name
            self._add_to_recent_files(file_path)
        else:
            tab_title = f"Untitled-{self.untitled_counter}"
            self.untitled_counter += 1

        pane = self.active_editor_pane
        if not pane and self.editor_panes:
            pane = self.editor_panes[0]
        index = pane.addTab(editor, tab_title)
        pane.setCurrentIndex(index)

        # Add custom close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("TabCloseButton")
        close_btn.setCursor(Qt.PointingHandCursor)
        pane.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)
        close_btn.clicked.connect(self._on_tab_close_btn_clicked)
        editor.problems_found.connect(self._update_problems_panel)
        editor.bookmarks_changed.connect(self._update_bookmarks_view)
        editor.modification_changed.connect(self._on_modification_changed)

        # Apply settings and highlighter
        self._apply_editor_settings(editor)
        self._on_tab_changed(index) # This will set up highlighter and language
        self._update_open_editors_list()
        return editor

    def _close_tab(self, index):
        pane = self.sender()
        if not isinstance(pane, QTabWidget): return
        editor_to_close = pane.widget(index)

        if editor_to_close and editor_to_close.document().isModified():
            pane.setCurrentIndex(index)
            file_name = pane.tabText(index).replace(" •", "")
            reply = QMessageBox.question(self, "Unsaved Changes",
                                         f"'{file_name}' has unsaved changes. Do you want to save them?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                if not self.save_code_to_file():
                    return # User cancelled the save dialog, so abort closing
            elif reply == QMessageBox.Cancel:
                return # Abort closing the tab

        # Clear problems for this file
        if editor_to_close and editor_to_close.file_path:
            self._update_problems_panel(editor_to_close.file_path, [])

        # Clear bookmarks for this file
        if editor_to_close and editor_to_close.file_path:
            self.all_bookmarks.pop(editor_to_close.file_path, None)
            self._update_bookmarks_view()
        editor = pane.widget(index)
        if editor:
            doc_id = id(editor.document())
            if doc_id in self.highlighters:
                self.highlighters[doc_id].setDocument(None)
                del self.highlighters[doc_id]
        pane.removeTab(index)
        if pane.count() == 0 and len(self.editor_panes) > 1:
            self.editor_panes.remove(pane)
            pane.deleteLater()
            if self.active_editor_pane is pane:
                self.active_editor_pane = self.editor_panes[0] if self.editor_panes else None
        self._update_open_editors_list()

    def _close_other_tabs(self, index_to_keep):
        pane = self.active_editor_pane
        if not pane: return
        for i in range(pane.count() - 1, -1, -1):
            if i != index_to_keep:
                pane.tabCloseRequested.emit(i)

    def _close_all_tabs(self):
        for pane in list(self.editor_panes):
            while pane.count() > 0:
                pane.tabCloseRequested.emit(0)

    def _show_tab_context_menu(self, point):
        """Shows a context menu for the code editor tabs."""
        tab_widget = self.sender()
        if not isinstance(tab_widget, QTabWidget): return

        tab_bar = tab_widget.tabBar()
        index = tab_bar.tabAt(point)
        if index == -1:
            return

        menu = QMenu()
        close_action = menu.addAction("Close")
        close_others_action = menu.addAction("Close Others")
        close_all_action = menu.addAction("Close All")
        menu.addSeparator()
        reveal_action = menu.addAction("Reveal in File Explorer")

        editor = tab_widget.widget(index)
        if not editor or not hasattr(editor, 'file_path') or not editor.file_path:
            reveal_action.setEnabled(False)

        action = menu.exec_(tab_bar.mapToGlobal(point))

        if action == close_action:
            tab_widget.tabCloseRequested.emit(index)
        elif action == close_others_action and self.active_editor_pane is tab_widget:
            self._close_other_tabs(index)
        elif action == close_all_action:
            self._close_all_tabs()
        elif action == reveal_action and editor and editor.file_path:
            subprocess.run(['explorer', '/select,', str(Path(editor.file_path).resolve())])

    def _show_terminal_context_menu(self, point):
        """Shows a context menu for the terminal output."""
        menu = QMenu()

        copy_action = menu.addAction("Copy")
        select_all_action = menu.addAction("Select All")
        menu.addSeparator()
        clear_action = menu.addAction("Clear")

        # Disable copy if no text is selected
        if not self.terminal_output.textCursor().hasSelection():
            copy_action.setEnabled(False)

        action = menu.exec_(self.terminal_output.viewport().mapToGlobal(point))

        if action == copy_action:
            self.terminal_output.copy()
        elif action == select_all_action:
            self.terminal_output.selectAll()
        elif action == clear_action:
            self.terminal_output.clear()

    def _on_tab_changed(self, index):
        """Handles logic when the active tab changes."""
        pane = self.sender()
        if not isinstance(pane, QTabWidget): return
        self.active_editor_pane = pane
        if index == -1: # No tabs left
            self.find_widget.hide()
            self._update_editor_actions_state(False)
            return

        self._sync_open_editors_selection()

        widget = self.active_editor_pane.currentWidget()
        is_editor = isinstance(widget, CodeEditor)
        self._update_editor_actions_state(is_editor)

        if is_editor:
            self.find_widget.editor = widget
            file_path = widget.file_path
            lang = "Python" # Default
            if file_path:
                ext = Path(file_path).suffix.lower()
                if ext in ['.js', '.ts']: lang = "JavaScript"
                elif ext in ['.html', '.htm']: lang = "HTML"
                elif ext == '.css': lang = "CSS"
                elif ext in ['.cpp', '.cxx', '.h', '.hpp']: lang = "C++"
            
            self.language_selector.blockSignals(True)
            self.language_selector.setCurrentText(lang)
            self.language_selector.blockSignals(False)
            self._update_breadcrumbs(file_path)

            # .editorconfig handling
            try:
                config = editorconfig.get_properties(file_path) if file_path else {}
                widget.indent_style = config.get('indent_style', 'space')
                widget.indent_size = int(config.get('indent_size', 4))
                self.indent_label.setText(f"{widget.indent_style.capitalize()}: {widget.indent_size}")
                self.indent_label.show()
            except Exception:
                self.indent_label.hide()
                self.encoding_label.hide()
                self.line_ending_label.hide()
                # Fallback to defaults
                widget.indent_style = 'space'
                widget.indent_size = 4

            self._update_title_bar(file_path)
            
            if lang == "Python":
                self.ast_viewer.update_ast(widget.toPlainText())
                widget.run_linter() # Run linter on tab change
                self._update_outline_view(widget.toPlainText(), lang)
                self._update_bookmarks_view()
            else:
                self.ast_viewer.clear()
            self._update_syntax_highlighter(widget, lang)
        else:
            # This is an image viewer or other non-editor widget
            self.find_widget.hide()
            self.ast_viewer.clear()
            self._update_breadcrumbs(widget.file_path)
            self._update_title_bar(widget.file_path)
            self._update_problems_panel(widget.file_path, []) # Clear problems for non-code files
            self._update_outline_view("", "") # Clear outline
            self._update_bookmarks_view()

    def _on_modification_changed(self, is_modified):
        """Updates the tab text to show a 'dirty' indicator."""
        editor = self.sender()
        if not isinstance(editor, CodeEditor): return

        # Find the tab for this editor
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if not isinstance(widget, CodeEditor): continue
                if widget != editor: continue

                if pane.widget(i) == editor:
                    current_text = pane.tabText(i)
                    # Remove indicator if it exists to prevent duplication
                    if " •" in current_text:
                        current_text = current_text.replace(" •", "")
                    
                    new_text = f"{current_text} •" if is_modified else current_text
                    pane.setTabText(i, new_text)
                    return


    def _update_open_editors_list(self):
        """Clears and rebuilds the 'Open Editors' list to match the current tabs."""
        self.open_editors_list.blockSignals(True)
        current_selection = self.open_editors_list.currentItem()
        current_data = (current_selection.data(Qt.UserRole) if current_selection else None)
        self.open_editors_list.clear()
        for pane_idx, pane in enumerate(self.editor_panes):
            for tab_idx in range(pane.count()):
                item = QListWidgetItem(pane.tabText(tab_idx))
                item.setData(Qt.UserRole, (pane_idx, tab_idx))
                self.open_editors_list.addItem(item)
        self.open_editors_list.blockSignals(False)
        self._sync_open_editors_selection()

    def _on_open_editor_clicked(self, item):
        """Switches to the tab corresponding to the clicked item in the 'Open Editors' list."""
        data = item.data(Qt.UserRole)
        if data:
            pane_idx, tab_idx = data
            if pane_idx < len(self.editor_panes):
                self.editor_panes[pane_idx].setCurrentIndex(tab_idx)

    def _sync_open_editors_selection(self):
        """Selects the correct item in the 'Open Editors' list when the tab changes."""
        if not self.active_editor_pane: return
        pane_idx = self.editor_panes.index(self.active_editor_pane)
        tab_idx = self.active_editor_pane.currentIndex()
        index = -1
        for i in range(self.open_editors_list.count()):
            if self.open_editors_list.item(i).data(Qt.UserRole) == (pane_idx, tab_idx):
                index = i
                break
        if index >= 0 and index < self.open_editors_list.count():
            self.open_editors_list.setCurrentRow(index)

    def _update_breadcrumbs(self, file_path):
        """Updates the breadcrumb navigation bar."""
        # Clear existing breadcrumbs by deleting all child widgets
        while self.breadcrumb_layout.count():
            child = self.breadcrumb_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.breadcrumb_layout.setSpacing(4)
        if file_path:
            path = Path(file_path)
            
            # Build a list of full paths for each part
            path_segments = []
            for p in reversed(path.parents):
                path_segments.append(p)
            path_segments.append(path)

            for p in path_segments[:-1]:
                button = QPushButton(p.name)
                button.setCursor(Qt.PointingHandCursor)
                button.clicked.connect(lambda checked=False, path_to_go=p: self._navigate_to_path_in_tree(str(path_to_go)))
                self.breadcrumb_layout.addWidget(button)
                self.breadcrumb_layout.addWidget(QLabel("›")) # Use a nicer separator
            self.breadcrumb_layout.addWidget(QLabel(path_segments[-1].name, objectName="CurrentFileCrumb"))
        self.breadcrumb_layout.addStretch()

    def _update_title_bar(self, file_path=None):
        """Updates the main window title and the custom title bar's path label."""
        if file_path:
            try:
                # Show relative path if possible
                rel_path = Path(file_path).relative_to(os.getcwd())
                display_text = f"{rel_path} - APICode"
            except ValueError:
                display_text = f"{Path(file_path).name} - APICode"
        else:
            display_text = "APICode"
        
        self.setWindowTitle(display_text) # Also update taskbar title

    def _update_outline_view(self, text, language):
        """Parses code and updates the outline view."""
        self.outline_model.clear()
        if not text or not language: return

        pattern = None
        if language == "Python":
            pattern = re.compile(r"^(?P<indent>\s*)(?:def|class)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^(?P<indent>\s*)(?:function|class|const|let|var)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:\s*=\s*\(|\s*\()")
        
        if not pattern: return

        parent_stack = [(self.outline_model.invisibleRootItem(), -1)] # (item, indent_level)
        for i, line in enumerate(text.splitlines()):
            match = pattern.match(line)
            if match:
                indent_len = len(match.group('indent'))
                name = match.group('name')
                
                while indent_len <= parent_stack[-1][1]:
                    parent_stack.pop()
                
                parent_item, _ = parent_stack[-1]
                item = QStandardItem(name)
                item.setData(i, Qt.UserRole)
                parent_item.appendRow(item)
                parent_stack.append((item, indent_len))

    def _on_outline_activated(self, index):
        line_num = self.outline_model.data(index, Qt.UserRole)
        if line_num is not None:
            self.go_to_line(line_num + 1)

    def _update_bookmarks_view(self):
        """Updates the global bookmarks list from all open editors."""
        self.bookmark_list.clear()
        editor = self.get_current_editor()
        if not editor: return

        for line_num in sorted(list(editor.bookmarks)):
            line_text = editor.document().findBlockByNumber(line_num).text().strip()
            item = QListWidgetItem(f"L{line_num + 1}: {line_text}")
            item.setData(Qt.UserRole, line_num)
            self.bookmark_list.addItem(item)

    def _on_bookmark_activated(self, item):
        line_num = item.data(Qt.UserRole)
        if line_num is not None:
            self.go_to_line(line_num + 1)

    def _navigate_to_path_in_tree(self, path_str):
        """Sets the file tree root to the given path."""
        source_index = self.file_model.index(path_str)
        if source_index.isValid() and self.file_model.isDir(source_index):
            proxy_index = self.proxy_model.mapFromSource(source_index)
            self.file_tree.setRootIndex(proxy_index)
            self.file_tree.expand(proxy_index)

    def _on_language_changed(self, language: str):
        """Updates the highlighter when the user manually changes the language."""
        self._update_syntax_highlighter(self.get_current_editor(), language)

    def _update_syntax_highlighter(self, editor, language: str):
        """Updates the syntax highlighter based on the selected language."""
        if not editor: return
        doc = editor.document()
        doc_id = id(doc)

        # Clean up old highlighter for this document if it exists
        if doc_id in self.highlighters:
            self.highlighters[doc_id].setDocument(None)

        highlighter_class = {
            "Python": PythonHighlighter,
            "JavaScript": JavaScriptHighlighter,
            "TypeScript": JavaScriptHighlighter,
            "C++": CppHighlighter,
            "C#": CppHighlighter,
            "Java": CppHighlighter,
            "Rust": CppHighlighter,
            "HTML": HtmlHighlighter,
            "CSS": CssHighlighter,
            "Go": CppHighlighter,
        }.get(language)

        if highlighter_class:
            highlighter = highlighter_class(doc)
            self.highlighters[doc_id] = highlighter
            highlighter.rehighlight()
        else:
            self.highlighters.pop(doc_id, None)

    def _on_file_search_changed(self, text):
        """Filters the file tree based on the search input."""
        self.proxy_model.setFilterRegularExpression(text)

    def _get_active_profile_path(self):
        last_profile_file = self.profiles_dir / 'last_profile.txt'
        if last_profile_file.exists():
            profile_name = last_profile_file.read_text().strip()
            profile_path = self.profiles_dir / f"{profile_name}.json"
            if profile_path.exists():
                return profile_path
        default_profile_path = self.profiles_dir / 'default.json'
        if not default_profile_path.exists():
            with open(default_profile_path, 'w') as f:
                json.dump({'theme': 'Dark', 'font_size': 14}, f, indent=4)
        return default_profile_path

    def _set_active_profile(self, profile_name):
        last_profile_file = self.profiles_dir / 'last_profile.txt'
        last_profile_file.write_text(profile_name)
        self.active_profile_path = self.profiles_dir / f"{profile_name}.json"

    def _switch_profile(self, profile_name):
        self._set_active_profile(profile_name)
        self.load_settings()
        self.apply_settings()
        self._update_profiles_menu()
        self.statusBar().showMessage(f"Switched to profile: {profile_name}", 3000)

    def _create_new_profile(self):
        profile_name, ok = QInputDialog.getText(self, "New Profile", "Enter new profile name:")
        if ok and profile_name:
            new_profile_path = self.profiles_dir / f"{profile_name}.json"
            if new_profile_path.exists():
                QMessageBox.warning(self, "Profile Exists", "A profile with this name already exists.")
                return
            with open(new_profile_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            self._switch_profile(profile_name)

    def load_settings(self):
        """Loads settings from the active profile JSON file or sets defaults."""
        if self.active_profile_path.exists():
            with open(self.active_profile_path, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}
        
        # Ensure all settings have a default value
        defaults = {
            'font_size': 14, 'version': '2.0.3', 'theme': 'Dark',
            'highlight_current_line': True, 'rounded_line_highlight': False,
            'show_minimap': True, 'show_visible_whitespace': False,
            'format_on_save': False, 'auto_save_on_focus_loss': False,
            'default_line_ending': 'LF'
        }
        for key, value in defaults.items():
            self.settings.setdefault(key, value)

        self.recent_files = self.settings.get('recent_files', [])

    def save_settings(self):
        """Saves the current settings to the active profile JSON file."""
        # Ensure theme name is saved correctly
        self.settings['theme'] = self.property("theme_name") or "Dark"
        self.settings['recent_files'] = self.recent_files
        with open(self.active_profile_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def apply_settings(self):
        """Applies the current settings to the UI."""
        self._apply_theme()
        # Apply font settings to all editors in all panes
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if isinstance(editor, CodeEditor):
                    self._apply_editor_settings(editor)
                    self._update_completer_model_for_editor(editor) # Refresh completer after settings change
        # Apply to terminal
        font_size = self.settings.get('font_size', 14)
        font = QFont("Consolas", font_size)
        self.terminal_output.setFont(font)
        self.command_input.setFont(font)

    def _apply_editor_settings(self, editor):
        """Applies font settings to a single editor widget."""
        if not editor: return
        # Font
        font_size = self.settings.get('font_size', 14)
        font = QFont("Fira Code", font_size) # Fira Code is great for ligatures
        font.setStyleStrategy(QFont.PreferAntialias)
        editor.setFont(font)
        # Other settings
        editor.highlight_current_line = self.settings.get('highlight_current_line', True)
        editor.rounded_line_highlight = self.settings.get('rounded_line_highlight', False)
        editor.minimap.setVisible(self.settings.get('show_minimap', True))
        editor.set_visible_whitespace(self.settings.get('show_visible_whitespace', False))
        editor._update_extra_selections() # Refresh highlights
        self._update_completer_model_for_editor(editor)

    def _apply_theme(self):
        """Applies the currently selected theme stylesheet."""
        theme = self.settings.get('theme', 'Dark')
        self.setProperty("theme_name", theme) # Store for highlighters

        icon_path = "assets/apicoderainbow.png" if theme == "Rainbow" else "assets/apicode.ico"
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)
        if hasattr(self, 'title_bar'):
            self.title_bar.icon_label.setPixmap(app_icon.pixmap(16, 16))

        self.setStyleSheet(generate_qss(theme))
        for action in self.theme_group.actions():
            if action.text() == theme:
                action.setChecked(True)
                break

    def show_settings_dialog(self):
        """Opens the settings dialog and applies changes if accepted."""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == QDialog.Accepted:
            self.settings = dialog.get_settings()
            self.apply_settings()
            self.save_settings()

    def _on_theme_changed(self, action):
        """Handles theme change from the menu."""
        theme = action.text()
        self.settings['theme'] = theme
        self._apply_theme()
        self.save_settings()
        self.recreate_all_highlighters()

    def _update_profiles_menu(self):
        if not self.profiles_menu: return
        self.profiles_menu.clear()
        
        profile_group = QActionGroup(self)

        # Add static actions first
        self.profiles_menu.addAction(self.new_profile_action)
        self.profiles_menu.addAction(self.manage_profiles_action)
        self.profiles_menu.addSeparator()
        
        profile_files = sorted(self.profiles_dir.glob("*.json"))
        active_profile_name = self.active_profile_path.stem
        
        for profile_path in profile_files:
            profile_name = profile_path.stem
            action = self.profiles_menu.addAction(profile_name)
            action.setCheckable(True)
            if profile_name == active_profile_name:
                action.setChecked(True)
            action.triggered.connect(lambda checked, name=profile_name: self._switch_profile(name))
            profile_group.addAction(action)

    def _update_completer_model_for_editor(self, editor):
        """Updates the completer model for a specific editor, including symbols."""
        if not isinstance(editor, CodeEditor): return

        text = editor.toPlainText()
        words = set(re.findall(r'\b\w{3,}\b', text))

        # Add symbols from the global symbol table
        for symbol, data in self.symbol_table.items():
            words.add(symbol)

        editor.word_model.setStringList(sorted(list(words)))

    def _trigger_member_completion(self, editor):
        """Triggers completion for members of an object (after a '.')."""
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 2)
        cursor.select(QTextCursor.WordUnderCursor)
        var_name = cursor.selectedText()

        completions = []
        # Simple hardcoded example for lists
        if "list" in var_name.lower(): # Very basic type inference
            completions.extend(['append', 'pop', 'sort', 'reverse', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'remove'])

        editor.completer.model().setStringList(completions)
        editor.completer.setCompletionPrefix("") # Start fresh
        editor.completer.complete()

    def _get_and_increment_version(self):
        """Gets the current version from settings, increments it, and saves it back."""
        version_str = self.settings.get('version', '1.0.0')
        
        try:
            major, minor, patch = map(int, version_str.split('.'))
            
            patch += 1
            if patch >= 10:
                patch = 0
                minor += 1
            if minor >= 100:
                minor = 0
                major += 1
            
            new_version_str = f"{major}.{minor}.{patch}"
            self.settings['version'] = new_version_str
            self.save_settings()
            return new_version_str
        except (ValueError, IndexError):
            self.settings['version'] = '1.0.0'
            self.save_settings()
            return '1.0.0'

    def show_about_dialog(self):
        """Displays the About dialog with version information."""
        version = self._get_and_increment_version()
        windowsver = platform.release()
        qtver = PYSIDE_VERSION
        psutilversion = psutil.__version__
        gpustatversion = getattr(gpustat, '__version__', 'N/A')
        pythonversion = platform.python_version()
        lgplversion = "3" # Assuming LGPLv3

        about_text = (
            f"APICode v{version} [tags: Windows {windowsver}, PyQt {qtver}, psutil {psutilversion}, "
            f"gpustat {gpustatversion}, Python {pythonversion}]\nFeatures Added: Git Integration, Split-Screen Editing.\n"
            f"Release Start: 8/30/2025 1:03 PM.\n"
            f"Licence: Found in LICENCE file, LGPLv{lgplversion}.\n\n"
            "Core Libraries: sys, os, json, subprocess, re, platform, pathlib, datetime, shutil, psutil, gpustat, tempfile, queue, ast, difflib, hashlib.\n"
            "Framework: PyQt5 (QtWidgets, QtWebEngineWidgets, QtCore, QtGui)."
            "Languages: Python."
        )
        QMessageBox.about(self, "About APICode", about_text)

    def show_find_widget(self):
        """Shows or hides the find/replace widget."""
        if self.find_widget.isVisible():
            self.find_widget.hide()
        else:
            # Pre-fill find input with selected text if any
            editor = self.get_current_editor()
            if not editor: return
            selected_text = editor.textCursor().selectedText()
            if selected_text:
                self.find_widget.find_input.setText(selected_text)
            self.find_widget.show()
            self.find_widget.find_input.setFocus()

    def go_to_line(self, line_num=None):
        """Shows a dialog to go to a line, or goes directly if line_num is provided."""
        editor = self.get_current_editor()
        if not editor:
            return

        if line_num is None:
            line_num, ok = QInputDialog.getInt(self, "Go to Line", "Line number:",
                                               editor.textCursor().blockNumber() + 1,
                                               min=1, max=editor.blockCount())
            if not ok:
                return
        
        if line_num > 0 and line_num <= editor.blockCount():
            cursor = QTextCursor(editor.document().findBlockByNumber(line_num - 1))
            editor.setTextCursor(cursor)
            editor.setFocus()

    def _show_go_to_symbol_dialog(self):
        """Parses the current file for symbols and shows the GoToSymbolDialog."""
        editor = self.get_current_editor()
        if not editor: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()
        symbols = []

        # Simple regex for Python and JS. Can be expanded.
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s*=\s*\(|\s*\()")
        else:
            self.statusBar().showMessage("Go to Symbol not supported for this language yet.", 3000)
            return

        for i, line in enumerate(text.splitlines()):
            match = pattern.match(line)
            if match:
                symbols.append((match.group(1), i))

        if not symbols:
            self.statusBar().showMessage("No symbols found in this file.", 3000)
            return

        dialog = GoToSymbolDialog(symbols, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_line != -1:
            self.go_to_line(dialog.selected_line + 1)

    def _toggle_column_select_info(self, checked):
        """Shows or clears a status bar message about column selection."""
        if checked:
            self.statusBar().showMessage("Column Selection Mode: Hold Alt+Shift and drag the mouse to select a block of text.", 0)
        else:
            self.statusBar().clearMessage()

    def _show_find_in_files_dialog(self):
        """Shows the 'Find in Files' dialog."""
        dialog = FindInFilesDialog(self)
        dialog.file_open_requested.connect(self._open_file_at_line)
        dialog.exec_()

    def _find_all_references(self):
        """Finds all references to the symbol under the cursor across the project."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol:
            self.statusBar().showMessage("No symbol selected to find references for.", 3000)
            return

        dialog = FindInFilesDialog(self)
        dialog.setWindowTitle(f"References to '{symbol}'")
        dialog.file_open_requested.connect(self._open_file_at_line)
        dialog.search_input.setText(symbol)
        dialog.whole_word_check.setChecked(True)
        dialog.case_sensitive_check.setChecked(True)
        dialog.start_search()
        dialog.exec_()

    def _peek_definition(self):
        """Shows the definition of the symbol under the cursor in a popup."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()

        pattern = None
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+" + re.escape(symbol) + r"\b")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+" + re.escape(symbol) + r"\b")

        if pattern:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if pattern.match(line):
                    # Found the definition, now extract context
                    start_line = i
                    # A simple way to get context: grab the next 15 lines or until indentation decreases
                    context_lines = [lines[start_line]]
                    base_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                    for j in range(start_line + 1, len(lines)):
                        next_line = lines[j]
                        if next_line.strip() == "": continue # Skip empty lines
                        next_indent = len(next_line) - len(next_line.lstrip())
                        if next_indent <= base_indent and j > start_line + 1:
                            break # End of block
                        context_lines.append(next_line)
                        if len(context_lines) >= 15:
                            break
                    
                    context_text = "\n".join(context_lines)

                    # Create and show the peek view
                    peek_view = PeekView(editor)
                    peek_view.setPlainText(context_text)
                    
                    # Apply font and highlighter
                    self._apply_editor_settings(peek_view)
                    self._update_syntax_highlighter(peek_view, language)

                    # Position and show
                    cursor_rect = editor.cursorRect()
                    global_pos = editor.mapToGlobal(cursor_rect.bottomLeft())
                    peek_view.move(global_pos)
                    peek_view.resize(editor.width() * 0.8, 250) # 80% of editor width
                    peek_view.show()
                    peek_view.setFocus()
                    return

        self.statusBar().showMessage(f"Definition of '{symbol}' not found.", 3000)

    def _run_git_command(self, command, file_path=None):
        """Helper to run a Git command in the file's directory."""
        cwd = os.path.dirname(file_path) if file_path else os.getcwd()
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(
                command, capture_output=True, text=True, check=True, cwd=cwd, startupinfo=si, creationflags=0x08000000
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _go_to_definition(self):
        """Jumps to the definition of the symbol under the cursor."""
        editor = self.get_current_editor()
        if not editor: return

        symbol = editor.textUnderCursor()
        if not symbol: return

        text = editor.toPlainText()
        language = self.language_selector.currentText()

        pattern = None
        if language == "Python":
            pattern = re.compile(r"^\s*(?:def|class)\s+" + re.escape(symbol) + r"\b")
        elif language in ["JavaScript", "TypeScript"]:
            pattern = re.compile(r"^\s*(?:function|class|const|let|var)\s+" + re.escape(symbol) + r"\b")

        if pattern:
            for i, line in enumerate(text.splitlines()):
                if pattern.match(line):
                    self.go_to_line(i + 1)
                    return
        self.statusBar().showMessage(f"Definition of '{symbol}' not found.", 3000)

    def _is_in_git_repo(self, file_path):
        """Checks if a file is within a Git repository."""
        return self._run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], file_path) is not None

    def _collect_actions_recursive(self, menu, collected_actions):
        for action in menu.actions():
            if action.menu(): # If it's a submenu
                self._collect_actions_recursive(action.menu(), collected_actions)
            elif not action.isSeparator() and action.text() and action.isEnabled():
                collected_actions.append(action)

    def _get_all_actions(self):
        all_actions = []
        # Iterate through the main menu bar's actions (which are the top-level menus)
        # Since self.setMenuBar(self.title_bar.menu_bar) is called, this correctly
        # iterates through the menus in the custom title bar.
        for menu_action in self.menuBar().actions():
            menu = menu_action.menu()
            if menu: self._collect_actions_recursive(menu, all_actions)
        return all_actions

    def _show_command_palette(self):
        actions = self._get_all_actions()
        palette = CommandPalette(actions, self)
        palette.exec_()

    def _show_manage_profiles_dialog(self):
        active_profile_name = self.active_profile_path.stem
        dialog = ManageProfilesDialog(self.profiles_dir, active_profile_name, self)
        dialog.exec_()

    @staticmethod
    def _is_module_installed(module_name):
        """Checks if a top-level module can be imported."""
        top_level_module = module_name.split('.')[0]
        try:
            return importlib.util.find_spec(top_level_module) is not None
        except (ValueError, ModuleNotFoundError):
            return False

    def _get_import_suggestions(self, symbol):
        """Generates a list of potential import or install statements for a given symbol."""
        suggestions = []
        if symbol in QUICK_FIX_IMPORTS:
            info = QUICK_FIX_IMPORTS[symbol]
            module_name = info['module']
            package_name = info.get('package_name')

            if self._is_module_installed(module_name):
                # Suggest import statement
                if info['type'] == 'from':
                    text = f"from {module_name} import {symbol}"
                    suggestions.append({'text': text, 'line': text, 'type': 'import'})
                elif info['type'] == 'direct':
                    alias = info.get('alias')
                    text = f"import {module_name}" + (f" as {alias}" if alias else "")
                    suggestions.append({'text': text, 'line': text, 'type': 'import'})
            elif package_name:
                # Suggest installation
                text = f"Install package '{package_name}'"
                suggestions.append({'text': text, 'package': package_name, 'type': 'install'})
        return suggestions

    def _apply_quick_fix_install(self, package_name, file_path_to_recheck):
        """Shows a confirmation and then installs a package using pip."""
        reply = QMessageBox.question(self, "Install Package", f"Do you want to install the package '{package_name}' using pip?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.bottom_tabs.setCurrentWidget(self.terminal_container)
            command = f'"{sys.executable}" -m pip install {package_name}'
            self.run_terminal_command(command=command, from_user=False)
            def recheck_linter():
                editor = self._find_open_editor(file_path_to_recheck)
                if editor: editor.run_linter()
            QTimer.singleShot(15000, recheck_linter) # Re-check after 15s

    def _apply_quick_fix_import(self, file_path, suggestion_data):
        editor = self._find_open_editor(file_path)
        if not editor: return
        import_line = suggestion_data['line']
        if import_line in editor.toPlainText(): return
        cursor = QTextCursor(editor.document())
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(import_line + '\n')
        editor.run_linter()

    def _show_problems_context_menu(self, pos):
        item = self.problems_table.itemAt(pos)
        if not item: return
        
        row = item.row()
        file_path = self.problems_table.item(row, 0).data(Qt.UserRole)
        line_num = int(self.problems_table.item(row, 1).text())
        problem_msg = self.problems_table.item(row, 3).text()

        problem_data = None
        if file_path in self.all_problems:
            for p in self.all_problems[file_path]:
                if p['line'] == line_num and p['msg'] == problem_msg:
                    problem_data = p
                    break
        
        menu = QMenu()
        quick_fix_menu = menu.addMenu("Quick Fix")

        import_suggestions_added = False
        if problem_data and problem_data.get('quick_fix_type') == 'import':
            symbol = problem_data.get('symbol')
            suggestions = self._get_import_suggestions(symbol)
            if suggestions:
                for suggestion in suggestions:
                    action = quick_fix_menu.addAction(suggestion['text'])
                    if suggestion['type'] == 'import':
                        action.triggered.connect(lambda checked, s=suggestion: self._apply_quick_fix_import(file_path, s))
                    elif suggestion['type'] == 'install':
                        action.triggered.connect(lambda checked, s=suggestion, f=file_path: self._apply_quick_fix_install(s['package'], f))
                import_suggestions_added = True
        
        if not import_suggestions_added: quick_fix_menu.setEnabled(False)

        menu.addSeparator()
        ignore_action = menu.addAction("Disable for this line")
        ignore_action.triggered.connect(lambda: self._apply_quick_fix_ignore(file_path, line_num))
        menu.exec_(self.problems_table.viewport().mapToGlobal(pos))

    def _apply_quick_fix_ignore(self, file_path, line_num):
        editor = self._find_open_editor(file_path)
        if not editor:
            self.statusBar().showMessage("File must be open to apply quick fix.", 3000)
            return
        
        block = editor.document().findBlockByNumber(line_num - 1)
        if block.isValid():
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfBlock)
            comment = "  # $IGNORE" if self.language_selector.currentText() == "Python" else "  // $IGNORE"
            cursor.insertText(comment)

    def _format_document(self):
        """Formats the current document using an external tool (e.g., autopep8)."""
        editor = self.get_current_editor()
        language = self.language_selector.currentText()
        if not editor or language != "Python":
            self.statusBar().showMessage("Formatting is only available for Python files.", 3000)
            return

        code = editor.toPlainText()
        try:
            result = subprocess.run(
                ['autopep8', '-'], input=code, capture_output=True,
                text=True, check=True, encoding='utf-8'
            )
            formatted_code = result.stdout
            if formatted_code != code:
                editor.setPlainText(formatted_code)
                self.statusBar().showMessage("Document formatted.", 2000)
        except FileNotFoundError:
            QMessageBox.warning(self, "Formatter Not Found", "The 'autopep8' command was not found. Please install it using 'pip install autopep8' and ensure it's in your system's PATH.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Formatting Error", f"An error occurred during formatting:\n\n{e.stderr}")

    def _on_problem_activated(self, row, column):
        file_item = self.problems_table.item(row, 0)
        line_item = self.problems_table.item(row, 1)
        if file_item and line_item:
            file_path = file_item.data(Qt.UserRole)
            line_num = int(line_item.text())
            self._open_file_at_line(file_path, line_num)

    def _update_problems_panel(self, file_path, problems):
        if file_path:
            if problems:
                self.all_problems[file_path] = problems
            else:
                self.all_problems.pop(file_path, None)
        
        self.problems_table.setRowCount(0)
        total_problems = 0
        for f_path, f_problems in self.all_problems.items():
            total_problems += len(f_problems)
            for problem in f_problems:
                row = self.problems_table.rowCount()
                self.problems_table.insertRow(row)
                file_name_item = QTableWidgetItem(Path(f_path).name)
                file_name_item.setData(Qt.UserRole, f_path)
                self.problems_table.setItem(row, 0, file_name_item)
                self.problems_table.setItem(row, 1, QTableWidgetItem(str(problem['line'])))
                self.problems_table.setItem(row, 2, QTableWidgetItem(str(problem['col'])))
                self.problems_table.setItem(row, 3, QTableWidgetItem(problem['msg']))
                color = QColor("#f44747") if problem['severity'] == 'error' else QColor("#FFC107")
                for i in range(4): self.problems_table.item(row, i).setForeground(color)
        self.bottom_tabs.setTabText(2, f"Problems ({total_problems})")

    def _show_local_history_dialog(self):
        editor = self.get_current_editor()
        if not editor or not editor.file_path:
            self.statusBar().showMessage("Open and save a file to view its history.", 3000)
            return
        dialog = LocalHistoryDialog(editor.file_path, editor.toPlainText(), self)
        dialog.exec_()

    def _get_local_history_path(self, file_path):
        file_hash = hashlib.sha1(str(Path(file_path).resolve()).encode()).hexdigest()
        return Path('.apicode') / 'history' / file_hash

    def _create_local_history_snapshot(self, file_path):
        if not file_path: return
        try:
            history_dir = self._get_local_history_path(file_path)
            history_dir.mkdir(parents=True, exist_ok=True)
            content = Path(file_path).read_text(encoding='utf-8')
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            (history_dir / f"{timestamp}.snapshot").write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"Could not create local history snapshot for {file_path}: {e}")

    def _show_extract_block_dialog(self):
        editor = self.get_current_editor()
        if not editor: return

        cursor = editor.textCursor()
        if not cursor.hasSelection():
            self.statusBar().showMessage("Please select a block of code to extract.", 3000)
            return

        selected_text = cursor.selectedText()
        language = self.language_selector.currentText()

        dialog = CodeBlockEditorDialog(selected_text, language, self)
        if dialog.exec_() == QDialog.Accepted:
            new_text = dialog.get_edited_text()
            # The original cursor still holds the selection, so inserting text will replace it.
            cursor.insertText(new_text)
            self.statusBar().showMessage("Code block updated.", 3000)

    def _show_git_branch_dialog(self):
        dialog = GitBranchDialog(self)
        dialog.exec_()

    def _show_git_stash_dialog(self):
        dialog = GitStashDialog(self)
        dialog.exec_()

    def _show_git_log_dialog(self):
        dialog = GitLogDialog(self)
        dialog.exec_()

    def _show_git_commit_dialog(self):
        dialog = GitCommitDialog(self)
        dialog.exec_()
        self._update_git_status() # Refresh file tree colors after commit

    def _git_create_branch_from_commit(self, commit_hash):
        """Creates and checks out a new branch from a specific commit."""
        if not commit_hash: return
        branch_name, ok = QInputDialog.getText(self, "Create Branch", "Enter new branch name:")
        if ok and branch_name:
            result = self._run_git_command(['git', 'checkout', '-b', branch_name, commit_hash])
            if result and result.returncode == 0:
                QMessageBox.information(self, "Branch Created", f"Successfully created and switched to branch '{branch_name}'.")
                self._update_status_bar()
            elif result:
                QMessageBox.critical(self, "Branch Creation Failed", f"Error creating branch:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Branch Creation Failed", "Failed to execute 'git checkout' command.")

    def _git_cherry_pick(self, commit_hash):
        """Helper function to perform a cherry-pick and show results."""
        if not commit_hash: return
        result = self._run_git_command(['git', 'cherry-pick', commit_hash])
        if result and result.returncode == 0:
            QMessageBox.information(self, "Cherry-Pick Success", f"Successfully cherry-picked commit {commit_hash[:7]}.")
            self._update_git_status()
        elif result:
            QMessageBox.critical(self, "Cherry-Pick Failed", f"Error cherry-picking commit:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Cherry-Pick Failed", "Failed to execute 'git cherry-pick' command.")

    def _git_revert(self, commit_hash):
        """Performs a git revert for the given commit hash."""
        if not commit_hash: return
        reply = QMessageBox.question(self, "Confirm Revert", 
                                     f"This will create a new commit that undoes the changes from {commit_hash[:7]}.\n\nAre you sure you want to continue?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # --no-edit prevents git from opening an editor for the commit message
            result = self._run_git_command(['git', 'revert', '--no-edit', commit_hash])
            if result and result.returncode == 0:
                QMessageBox.information(self, "Revert Success", f"Successfully reverted commit {commit_hash[:7]}.")
                self._update_git_status()
            elif result:
                QMessageBox.critical(self, "Revert Failed", f"Error reverting commit:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Revert Failed", "Failed to execute 'git revert' command.")

    def _show_git_cherry_pick_dialog(self):
        dialog = GitCherryPickDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self._git_cherry_pick(dialog.selected_commit_hash)

    def _git_push(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Git Push")
        msg_box.setText("Pushing to remote...")
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        QApplication.processEvents()

        result = self._run_git_command(['git', 'push'])
        msg_box.hide()

        if result and result.returncode == 0:
            QMessageBox.information(self, "Git Push", f"Push successful.\n\n{result.stdout}")
        elif result:
            QMessageBox.critical(self, "Git Push Failed", f"Error pushing to remote:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Git Push Failed", "Failed to execute 'git push' command.")

    def _git_stash(self):
        message, ok = QInputDialog.getText(self, "Stash Changes", "Enter an optional stash message:")
        if ok:
            command = ['git', 'stash']
            if message:
                command.extend(['push', '-m', message])
            
            result = self._run_git_command(command)
            if result and result.returncode == 0:
                QMessageBox.information(self, "Git Stash", "Changes stashed successfully.")
                self._update_git_status()
            elif result:
                QMessageBox.critical(self, "Git Stash Failed", f"Error stashing changes:\n\n{result.stderr}")
            else:
                QMessageBox.critical(self, "Git Stash Failed", "Failed to execute 'git stash' command.")

    def _git_apply_stash(self):
        result = self._run_git_command(['git', 'stash', 'apply'])
        if result and result.returncode == 0:
            QMessageBox.information(self, "Apply Stash", "Latest stash applied successfully.")
            self._update_git_status()
        elif result:
            QMessageBox.critical(self, "Apply Stash Failed", f"Error applying stash:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Apply Stash Failed", "Failed to execute 'git stash apply' command.")

    def _git_pull(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Git Pull")
        msg_box.setText("Pulling from remote...")
        msg_box.setStandardButtons(QMessageBox.NoButton)
        msg_box.show()
        QApplication.processEvents()

        result = self._run_git_command(['git', 'pull'])
        msg_box.hide()

        if result and result.returncode == 0:
            QMessageBox.information(self, "Git Pull", f"Pull successful.\n\n{result.stdout}")
            self._update_git_status() # Refresh file tree in case of changes
        elif result:
            QMessageBox.critical(self, "Git Pull Failed", f"Error pulling from remote:\n\n{result.stderr}")
        else:
            QMessageBox.critical(self, "Git Pull Failed", "Failed to execute 'git pull' command.")

    def _show_task_manager(self):
        dialog = TaskManagerDialog(self)
        dialog.show() # Use show() for a non-modal dialog

    def _setup_timers(self):
        """Initializes all background timers."""
        # Setup a timer to batch process output from the queue
        self.output_timer = QTimer(self)
        self.output_timer.setInterval(50)  # Process queue every 50ms
        self.output_timer.timeout.connect(self._process_output_queue)

        # Setup a timer to update the status bar
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(2000) # Update every 2 seconds
        self.status_timer.timeout.connect(self._update_status_bar)

    def _is_in_git_repo(self, file_path):
        """Checks if a file is within a Git repository."""
        return self._run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], file_path) is not None

    def _has_git_changes(self, file_path):
        """Checks if a file has uncommitted changes."""
        result = self._run_git_command(['git', 'status', '--porcelain', '--', file_path], file_path)
        return result and result.stdout.strip() != ""

    def _show_diff_view(self, file_path):
        """Shows a dialog with the diff for a given file."""
        # Use --no-color to get plain text diff
        result = self._run_git_command(['git', '--no-pager', 'diff', 'HEAD', '--', file_path], file_path)
        if result:
            dialog = DiffViewDialog(result.stdout, Path(file_path).name, file_path, self)
            dialog.exec_()
        else:
            QMessageBox.information(self, "No Changes", "No changes found for this file compared to the last commit.")

    def _open_file_at_line(self, file_path, line_num):
        """Opens a file and jumps to a specific line."""
        self._open_file(file_path)
        self.go_to_line(line_num)

    def _reload_file_if_open(self, file_path):
        """Checks if a file is open in any tab and reloads its content from disk."""
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if editor.file_path and Path(editor.file_path).resolve() == resolved_path:
                    with open(resolved_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    cursor_pos = editor.textCursor().position()
                    editor.setPlainText(content)
                    cursor = editor.textCursor()
                    cursor.setPosition(min(cursor_pos, len(content)))
                    editor.setTextCursor(cursor)
                    self.statusBar().showMessage(f"Reloaded {resolved_path.name} due to external changes.", 3000)
                    return # Exit after reloading

    def _show_feedback_dialog(self):
        """Opens a dialog for the user to submit feedback."""
        text, ok = QInputDialog.getMultiLineText(self, "Submit Feedback", "Please provide your feedback for APICode and the development team to review:")
        if ok and text:
            feedback_dir = Path("feedback")
            feedback_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = feedback_dir / f"feedback_{timestamp}.txt"
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Feedback Submitted", "Thank you! Your feedback will be reviewed soon.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save feedback: {e}")

    def toggle_word_wrap(self):
        """Toggles word wrap for the current editor."""
        editor = self.get_current_editor()
        if not editor: return
        current_mode = editor.lineWrapMode()
        new_mode = QPlainTextEdit.NoWrap if current_mode == QPlainTextEdit.WidgetWidth else QPlainTextEdit.WidgetWidth
        editor.setLineWrapMode(new_mode)

    def _update_recent_files_menu(self):
        """Clears and rebuilds the 'Recent Files' part of the File menu."""
        # Remove all old recent file actions
        for action in self.recent_files_actions:
            self.file_menu.removeAction(action)
        self.recent_files_actions.clear()

        # Add the new actions
        self.recent_files_separator.setVisible(bool(self.recent_files))
        if self.recent_files:
            for path in self.recent_files:
                action = QAction(path, self)
                action.triggered.connect(lambda checked=False, p=path: self._open_recent_file(p))
                self.file_menu.insertAction(self.recent_files_separator, action)
                self.recent_files_actions.append(action)

    def _add_to_recent_files(self, file_path):
        """Adds a file path to the top of the recent files list."""
        if not file_path:
            return
        
        resolved_path = str(Path(file_path).resolve())
        if resolved_path in self.recent_files:
            self.recent_files.remove(resolved_path)
        
        self.recent_files.insert(0, resolved_path)
        self.recent_files = self.recent_files[:10] # Limit to 10 recent files
        
        self.save_settings()
        self._update_recent_files_menu()

    def _open_file_in_active_pane(self, file_path):
        if not self.active_editor_pane:
            if not self.editor_panes:
                self._create_new_editor_pane()
            self.active_editor_pane = self.editor_panes[0]
        self._open_file(file_path)

    def _open_file_from_tree(self, index):
        source_index = self.proxy_model.mapToSource(index)
        path = self.file_model.filePath(source_index)
        if not self.file_model.isDir(source_index):
            self._open_file_in_active_pane(path)

    def _show_file_tree_context_menu(self, point):
        """Creates and shows a context menu for the file tree."""
        proxy_index = self.file_tree.indexAt(point)
        # If clicking on empty space, use the root as the context
        if not proxy_index.isValid():
            proxy_index = self.file_tree.rootIndex()
        source_index = self.proxy_model.mapToSource(proxy_index)
        path = self.file_model.filePath(source_index)

        is_git_repo = self._is_in_git_repo(path)
        has_changes = is_git_repo and self._has_git_changes(path)

        is_dir = self.file_model.isDir(source_index)

        menu = QMenu()
        open_action = None
        if not is_dir:
            open_action = menu.addAction("Open")

        compare_action = None
        open_editor = self._find_open_editor(path)
        if open_editor and open_editor.document().isModified():
            compare_action = menu.addAction("Compare with Saved")

        view_changes_action = None
        if has_changes and not is_dir:
            view_changes_action = menu.addAction("View Changes")

        # --- Compare Logic ---
        menu.addSeparator()
        select_for_compare_action = None
        if not is_dir:
            select_for_compare_action = menu.addAction("Select for Compare")

        compare_with_action = None
        if self.file_to_compare and not is_dir and path != self.file_to_compare:
            compare_with_action = menu.addAction(f"Compare with '{Path(self.file_to_compare).name}'")

        cancel_compare_action = None
        if self.file_to_compare:
            cancel_compare_action = menu.addAction("Cancel Compare")
        # --- End Compare Logic ---

        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        rename_action = menu.addAction("Rename")
        menu.addSeparator()
        open_with_default_action = menu.addAction("Open with Default App")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")

        if not path: # Disable actions that don't make sense for empty space
            rename_action.setEnabled(False)
            delete_action.setEnabled(False)
            open_with_default_action.setEnabled(False)

        action = menu.exec_(self.file_tree.viewport().mapToGlobal(point))

        if action == open_action:
            self._open_file_in_active_pane(path)
        elif action == compare_action:
            self._show_editor_vs_disk_diff(open_editor)
        elif action == view_changes_action:
            self._show_diff_view(path)
        elif action == select_for_compare_action:
            self.file_to_compare = path
            self.statusBar().showMessage(f"Selected '{Path(path).name}' for comparison.", 3000)
        elif action == compare_with_action:
            self._show_file_diff(self.file_to_compare, path)
            self.file_to_compare = None # Reset after comparison
        elif action == cancel_compare_action:
            self.file_to_compare = None
            self.statusBar().showMessage("Comparison cancelled.", 2000)
        elif action == new_file_action:
            self._create_new_file_handler(path)
        elif action == new_folder_action:
            self._create_new_folder_handler(path)
        elif action == rename_action:
            self._rename_item_handler(path)
        elif action == open_with_default_action:
            if path: os.startfile(path)
        elif action == delete_action:
            self._delete_item_handler(path)

    def _rename_item_handler(self, old_path_str):
        """Handles the 'Rename' action from the context menu."""
        if not old_path_str: return
        old_path = Path(old_path_str)
        
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=old_path.name)
        
        if ok and new_name and new_name != old_path.name:
            new_path = old_path.parent / new_name
            if new_path.exists():
                QMessageBox.warning(self, "Error", "A file or folder with that name already exists.")
                return
            try:
                old_path.rename(new_path)
                
                # Update any open tabs with the new path (This logic was buggy, simplified)
                self._update_tab_path(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not rename item: {e}")

    def _create_new_file_handler(self, path):
        """Handles the 'New File' action from the context menu."""
        base_path = Path(path)
        if not base_path.is_dir():
            base_path = base_path.parent

        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
        if ok and file_name:
            new_file_path = base_path / file_name
            if not new_file_path.exists():
                new_file_path.touch() # Create the file
                self._open_file_in_active_pane(str(new_file_path))
            else:
                QMessageBox.warning(self, "Error", "A file with that name already exists.")

    def _update_tab_path(self, old_path, new_path):
        """Updates the path and title of an open tab after a rename."""
        for pane in self.editor_panes:
            for i in range(pane.count()):
                editor = pane.widget(i)
                if editor.file_path and Path(editor.file_path).resolve() == old_path.resolve():
                    editor.file_path = str(new_path)
                    pane.setTabText(i, new_path.name)
                    self._update_open_editors_list()
                    return

    def _create_new_folder_handler(self, path):
        """Handles the 'New Folder' action from the context menu."""
        base_path = Path(path)
        if not base_path.is_dir():
            base_path = base_path.parent

        folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and folder_name:
            new_folder_path = base_path / folder_name
            if not new_folder_path.exists():
                new_folder_path.mkdir()
            else:
                QMessageBox.warning(self, "Error", "A folder with that name already exists.")

    def _delete_item_handler(self, path):
        """Handles the 'Delete' action from the context menu."""
        if not path: return
        p = Path(path)
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{p.name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete item: {e}")

    def _open_file(self, file_path):
        """Helper function to open a file and create a new tab for it."""
        resolved_path = Path(file_path).resolve()
        # Check if the file is already open in any pane
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if hasattr(widget, 'file_path') and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    pane.setCurrentIndex(i)
                    self.active_editor_pane = pane
                    return

        IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
        if resolved_path.suffix.lower() in IMAGE_EXTENSIONS:
            self._create_image_tab(str(resolved_path))
        else:
            try:
                with open(resolved_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._create_new_tab(file_path=str(resolved_path), content=content)
                self.statusBar().showMessage(f"Loaded {resolved_path}", 3000)
            except UnicodeDecodeError:
                reply = QMessageBox.question(self, "Binary File Detected",
                                             "This file does not appear to be text. Open with default application?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    os.startfile(str(resolved_path))
            except Exception as e:
                self.statusBar().showMessage(f"Error opening file: {e}", 5000)

    def _update_editor_actions_state(self, is_editor):
        """Enables or disables actions based on whether the current tab is an editor."""
        actions_to_toggle = [
            self.save_action, self.save_as_action, self.undo_action, self.redo_action,
            self.cut_action, self.copy_action, self.paste_action, self.find_action,
            self.duplicate_line_action, self.select_all_action, self.word_wrap_action,
            self.go_to_line_action, self.go_to_definition_action, self.peek_definition_action,
            self.find_all_references_action, self.go_to_symbol_action
        ]
        for action in actions_to_toggle:
            action.setEnabled(is_editor)

    def _find_open_editor(self, file_path):
        """Finds and returns the editor widget for a given file path, if open."""
        if not file_path: return None
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if isinstance(widget, CodeEditor) and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    return widget
        return None

    def _show_editor_vs_disk_diff(self, editor):
        """Shows a diff between the editor's content and the version on disk."""
        if not editor or not editor.file_path: return
            
        file_path = editor.file_path
        editor_content = editor.toPlainText().splitlines()
        
        try:
            disk_content = Path(file_path).read_text(encoding='utf-8').splitlines()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read file from disk: {e}")
            return
            
        diff = difflib.unified_diff(disk_content, editor_content, fromfile="saved on disk", tofile="current in editor", lineterm='')
        diff_text = "\n".join(list(diff))
        
        dialog = DiffViewDialog(diff_text, Path(file_path).name, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

    def _show_file_diff(self, path1, path2):
        """Shows a diff view for two arbitrary files."""
        try:
            content1 = Path(path1).read_text(encoding='utf-8', errors='ignore').splitlines()
            content2 = Path(path2).read_text(encoding='utf-8').splitlines()
        except Exception as e:
            QMessageBox.critical(self, "Error Reading Files", f"Could not read one of the files for comparison:\n{e}")
            return

        diff = difflib.unified_diff(content1, content2, fromfile=Path(path1).name, tofile=Path(path2).name, lineterm='')
        diff_text = "\n".join(list(diff))

        dialog_title = f"Comparing Files"
        dialog = DiffViewDialog(diff_text, dialog_title, file_path=None, parent=self, show_git_buttons=False)
        dialog.exec_()

    def _open_recent_file(self, path):
        """Opens a file from the recent files list."""
        file = Path(path)
        if file.exists():
            self._open_file_in_active_pane(path)
        else:
            self.recent_files.remove(path)
            self._update_recent_files_menu()
            self.statusBar().showMessage(f"File not found: {path}", 3000)

    def _update_status_bar(self):
        """Periodically updates the resource usage in the status bar."""
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")

        # Memory
        mem_percent = psutil.virtual_memory().percent
        self.mem_label.setText(f"Mem: {mem_percent:.1f}%")

        # GPU (NVIDIA only, via gpustat)
        try:
            gpu_stats = gpustat.new_query()
            if gpu_stats:
                gpu = gpu_stats[0] # Take the first GPU
                self.gpu_label.setText(f"GPU: {gpu.utilization}%")
            else:
                self.gpu_label.setText("GPU: N/A")
        except Exception:
            self.gpu_label.setText("GPU: N/A")
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True, cwd=os.getcwd(), startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW
            )
            branch_name = result.stdout.strip()
            self.git_label.setText(f" {branch_name}")
            self.git_label.show()
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.git_label.hide()

    def _update_git_status(self):
        """Gets git status and tells the file model to update its styling."""
        changed_files = self._get_git_changed_files_set()
        if hasattr(self.file_model, 'set_git_changed_files'):
            self.file_model.set_git_changed_files(changed_files)

    def _get_git_changed_files_set(self):
        """Runs 'git status' and returns a set of absolute paths for modified files."""
        result = self._run_git_command(['git', 'status', '--porcelain'])
        changed = set()
        if result and result.stdout:
            for line in result.stdout.strip().splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    abs_path = Path(os.getcwd()) / parts[1].replace('"', '')
                    changed.add(abs_path.resolve())
        return changed

    def setup_powershell_backend(self):
        """Starts a persistent PowerShell process and a thread to read its output."""
        self.powershell_process = subprocess.Popen(
            ['powershell.exe', '-NoLogo', '-NoProfile', '-NoExit', '-Command', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            shell=True,
            bufsize=1 # Line-buffered
        )

        self.powershell_thread = QThread()
        self.worker = PowerShellWorker(self.powershell_process.stdout, self.output_queue)
        self.worker.moveToThread(self.powershell_thread)

        self.powershell_thread.started.connect(self.worker.run)
        self.powershell_thread.start()

        # Send initial commands to set directory and get the first prompt path
        self.powershell_process.stdin.write("cd C:\\\n")
        self.powershell_process.stdin.write("Write-Host \"PROMPT_PATH:$((Get-Location).Path)\"\n")
        self.powershell_process.stdin.flush()

    def load_code_from_file(self):
        """Opens a file dialog to load code into the editor."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Code File", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self._open_file_in_active_pane(file_name)

    def save_code_to_file(self):
        """Opens a file dialog to save the code from the editor."""
        editor = self.get_current_editor()
        if not editor: return
        
        file_path = editor.file_path
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self._create_local_history_snapshot(file_path)
            editor.document().setModified(False)
            self.statusBar().showMessage(f"Saved {file_path}", 3000)
            return True
        else:
            return self.save_as()

    def save_as(self):
        """Saves the current tab's content to a new file."""
        editor = self.get_current_editor()
        if not editor: return
        pane = self.active_editor_pane
        index = pane.currentIndex()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self._create_local_history_snapshot(file_name)
            editor.file_path = file_name
            editor.document().setModified(False)
            pane.setTabText(index, Path(file_name).name)
            self._add_to_recent_files(file_name)
            self.statusBar().showMessage(f"Saved to {file_name}", 3000)
            return True
        return False

    def _restore_file_content(self, file_path, content):
        """Finds the tab for a file and replaces its content."""
        resolved_path = Path(file_path).resolve()
        for pane in self.editor_panes:
            for i in range(pane.count()):
                widget = pane.widget(i)
                if isinstance(widget, CodeEditor) and widget.file_path and Path(widget.file_path).resolve() == resolved_path:
                    widget.setPlainText(content)
                    self.statusBar().showMessage(f"Restored content for {Path(file_path).name}", 3000)
                    return

    def copy_code_to_clipboard(self):
        """Copies the content of the code editor to the clipboard."""
        self._safe_editor_action(lambda e: QApplication.clipboard().setText(e.toPlainText()))

    def copy_terminal_output(self):
        """Copies the content of the terminal output to the clipboard."""
        QApplication.clipboard().setText(self.terminal_output.toPlainText())

    def _display_output(self, output, is_error=False):
        """Helper to format and display text in the code output view."""
        color = "#f44747" if is_error else "#bbbbbb"
        escaped_output = output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if is_error:
            # Highlight file paths in magenta, like in VS Code
            escaped_output = re.sub(
                r'(File &quot;[^&;]+&quot;)',
                r'<span style="color: #c586c0;">\1</span>',
                escaped_output
            )

        html_output = f"<pre style='color: {color}; font-family: Consolas, Courier New;'>{escaped_output}</pre>"
        self.output_view.setHtml(html_output)

    def run_code(self):
        """Executes the code in the editor based on the selected language."""
        editor = self.get_current_editor()
        if not editor: return
        code = editor.toPlainText()
        if not code.strip():
            self._display_output("No code to run.", is_error=False)
            return

        language = self.language_selector.currentText()

        dispatch_map = {
            "Python": self.run_python,
            "JavaScript": lambda c: self.run_script(c, "node"),
            "TypeScript": self.run_typescript,
            "PHP": lambda c: self.run_script(c, "php"),
            "Go": self.run_go,
            "Java": self.run_java,
            "C++": self.run_cpp,
            "C#": self.run_csharp,
            "Rust": self.run_rust,
            "Visual Basic": self.run_vb,
            "Batch": self.run_shell,
            "PowerShell": self.run_powershell,
            "HTML": self.run_html,
        }

        runner = dispatch_map.get(language)
        if runner:
            try:
                runner(code)
            except FileNotFoundError as e:
                self._display_output(f"Error: Command '{e.filename}' not found. Is it installed and in your system's PATH?", is_error=True)
            except subprocess.TimeoutExpired:
                self._display_output("Error: Execution timed out.", is_error=True)
            except Exception as e:
                self._display_output(f"An unexpected error occurred: {e}", is_error=True)
        else:
            self._display_output(f"Language '{language}' not supported for execution.", is_error=True)

    def run_script(self, code: str, interpreter: str):
        """Executes a script using a given interpreter via stdin."""
        result = subprocess.run(
            [interpreter, "-"], input=code, capture_output=True, text=True, timeout=10
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_typescript(self, code: str):
        """Compiles and runs a TypeScript program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.ts"
            source_path.write_text(code, encoding='utf-8')
            js_path = Path(tempdir) / "source.js"

            # Compile TypeScript to JavaScript
            compile_proc = subprocess.run(
                ['tsc', str(source_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            # Run the resulting JavaScript file
            self.run_script(f'require("{js_path.as_posix()}");', "node")

    def run_go(self, code: str):
        """Compiles and runs a Go program using 'go run'."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(code)
            source_path = temp_file.name
        try:
            result = subprocess.run(
                ['go', 'run', source_path], capture_output=True, text=True, timeout=20
            )
            self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)
        finally:
            os.remove(source_path)

    def run_java(self, code: str):
        """Compiles and runs a Java program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "Main.java"
            source_path.write_text(code, encoding='utf-8')

            compile_proc = subprocess.run(
                ['javac', str(source_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            run_proc = subprocess.run(
                ['java', 'Main'], cwd=tempdir, capture_output=True, text=True, timeout=10
            )
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def _compile_and_run(self, code, ext, compile_cmd, exe_name="source.exe"):
        """Generic helper to compile and run languages that produce an .exe."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / f"source{ext}"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / exe_name

            compile_proc = subprocess.run(
                compile_cmd + [str(source_path), '/out:' + str(exe_path)],
                capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return

            run_proc = subprocess.run(
                [str(exe_path)], capture_output=True, text=True, timeout=10
            )
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_cpp(self, code: str):
        """Compiles and runs a C++ program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.cpp"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / "source.exe"
            compile_proc = subprocess.run(
                ['g++', str(source_path), '-o', str(exe_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return
            run_proc = subprocess.run([str(exe_path)], capture_output=True, text=True, timeout=10)
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_csharp(self, code: str):
        """Compiles and runs a C# program."""
        self._compile_and_run(code, '.cs', ['csc'])

    def run_rust(self, code: str):
        """Compiles and runs a Rust program."""
        with tempfile.TemporaryDirectory() as tempdir:
            source_path = Path(tempdir) / "source.rs"
            source_path.write_text(code, encoding='utf-8')
            exe_path = Path(tempdir) / "source.exe"
            compile_proc = subprocess.run(
                ['rustc', str(source_path), '-o', str(exe_path)], capture_output=True, text=True, timeout=15
            )
            if compile_proc.returncode != 0:
                self._display_output(compile_proc.stdout + compile_proc.stderr, is_error=True)
                return
            run_proc = subprocess.run([str(exe_path)], capture_output=True, text=True, timeout=10)
            self._display_output(run_proc.stdout + run_proc.stderr, is_error=run_proc.returncode != 0)

    def run_vb(self, code: str):
        """Compiles and runs a Visual Basic program."""
        self._compile_and_run(code, '.vb', ['vbc'])

    def run_powershell(self, code: str):
        """Executes a PowerShell script and displays the output."""
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-Command', code],
            capture_output=True, text=True, timeout=15
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_python(self, code: str):
        """Executes a Python script in a subprocess and displays the output."""
        # sys.executable ensures we use the same Python interpreter that runs the app
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, timeout=10
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def run_html(self, code: str):
        """Renders HTML code directly in the web view."""
        self.output_view.setHtml(code)

    def run_shell(self, command: str):
        """Executes a shell command and displays the output."""
        # Using shell=True allows execution of shell built-ins (e.g., 'dir', 'echo').
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        self._display_output(result.stdout + result.stderr, is_error=result.returncode != 0)

    def format_terminal_output(self, text, is_error=False):
        """Formats text with HTML for rich color display in the terminal."""
        # Escape base HTML characters
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if is_error:
            text = f"<span style='color: #f44747;'>{text}</span>"
            # Highlight file paths in magenta
            text = re.sub(
                r'(File\s+)(&quot;[^&;]+&quot;)',
                r'\1<span style="color: #c586c0;">\2</span>',
                text
            )
        else:
            # Highlight PowerShell-like variables ($...) in green
            text = re.sub(r'(\$\w+)', r'<span style="color: #98c379;">\1</span>', text)
            # Highlight single-quoted strings in blue
            text = re.sub(r"('[^']+')", r'<span style="color: #569cd6;">\1</span>', text)

        return text
    def run_terminal_command(self, command=None, from_user=True):
        """Executes the command from the input line in the integrated terminal."""
        command_to_run = command if command is not None else self.command_input.text().strip()
        if from_user:
            self.command_input.clear()

        if not command_to_run: return

        safe_path = self.current_path.replace("<", "&lt;").replace(">", "&gt;")
        prompt_html = f"<span style='color: #bbbbbb;'>PS {safe_path}&gt; </span><span style='color: #dcdcaa;'>{command_to_run}</span>"
        self.terminal_output.append(prompt_html)
        self.powershell_process.stdin.write(command_to_run + '\n')
        self.powershell_process.stdin.write("Write-Host \"PROMPT_PATH:$((Get-Location).Path)\"\n")
        self.powershell_process.stdin.flush()
    def _process_output_queue(self):
        if self.output_queue.empty():
            return
        lines = []
        while not self.output_queue.empty():
            try:
                lines.append(self.output_queue.get_nowait())
            except queue.Empty:
                break
        output_html = []
        for line in lines:
            stripped_text = line.strip()
            if stripped_text.startswith("PROMPT_PATH:"):
                self.current_path = stripped_text.replace("PROMPT_PATH:", "").strip()
                self.command_input.setPlaceholderText(f"PS {self.current_path}> Enter command...")
                continue  # Do not display this special line
            is_error = "error" in stripped_text.lower() or "exception" in stripped_text.lower()
            formatted_text = self.format_terminal_output(stripped_text, is_error=is_error)
            if formatted_text:  # Don't append empty lines
                output_html.append(formatted_text)
        if output_html:
            self.terminal_output.append("<br>".join(output_html))
            self.terminal_output.verticalScrollBar().setValue(self.terminal_output.verticalScrollBar().maximum())

    def _post_init_setup(self):
        """Tasks to run after the main window is shown to prevent startup issues."""
        self.setup_powershell_backend()
        self.output_timer.start()
        self.status_timer.start()
        # Initial update
        self._update_git_status()
        # Connect debugger signals
        if self.debugger:
            self.debugger.variables_updated.connect(self.variable_inspector.update_variables)
            self.debugger.debugging_stopped.connect(self.variable_inspector.clear_variables)

    def get_current_editor(self):
        """Returns the CodeEditor widget in the currently active tab."""
        if self.active_editor_pane:
            widget = self.active_editor_pane.currentWidget()
            if isinstance(widget, CodeEditor):
                return widget
        return None

    def save_code_to_file(self, editor=None):
        """Opens a file dialog to save the code from the editor."""
        editor = editor or self.get_current_editor()
        if not editor: return
        
        if self.settings.get('format_on_save', False) and self.language_selector.currentText() == "Python":
            self._format_document(editor_to_format=editor)

        file_path = editor.file_path
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self._create_local_history_snapshot(file_path)
            editor.document().setModified(False)
            self.statusBar().showMessage(f"Saved {file_path}", 3000)
            return True
        else:
            return self.save_as()
            # -----------------------------
# Nebula UI Wrapper Classes
# -----------------------------
class NebulaWindow(QWidget):
    def __init__(self, *children, **kwargs):
        super().__init__()
        self.setWindowTitle(kwargs.get("title", "Nebula App"))
        layout = QVBoxLayout()
        for c in children:
            if isinstance(c, QWidget): layout.addWidget(c)
        self.setLayout(layout)

class NebulaVLayout(QWidget):
    def __init__(self, orientation, *children):
        super().__init__()
        layout = QVBoxLayout() if orientation == 'vertical' else QHBoxLayout()
        for c in children:
            if isinstance(c, QWidget): layout.addWidget(c)
        self.setLayout(layout)

class NebulaLabel(QLabel):
    def __init__(self, text="", **kwargs): super().__init__(text)

class NebulaButton(QPushButton):
    def __init__(self, text="", on_click=None, **kwargs):
        super().__init__(text)
        if on_click: self.clicked.connect(on_click)# -----------------------------
# Nebula UI Wrapper Classes
# -----------------------------
class NebulaWindow(QWidget):
    def __init__(self, *children, **kwargs):
        super().__init__()
        self.setWindowTitle(kwargs.get("title", "Nebula App"))
        layout = QVBoxLayout()
        for c in children:
            if isinstance(c, QWidget): layout.addWidget(c)
        self.setLayout(layout)

class NebulaVLayout(QWidget):
    def __init__(self, orientation, *children):
        super().__init__()
        layout = QVBoxLayout() if orientation == 'vertical' else QHBoxLayout()
        for c in children:
            if isinstance(c, QWidget): layout.addWidget(c)
        self.setLayout(layout)

class NebulaLabel(QLabel):
    def __init__(self, text="", **kwargs): super().__init__(text)

class NebulaButton(QPushButton):
    def __init__(self, text="", on_click=None, **kwargs):
        super().__init__(text)
        if on_click: self.clicked.connect(on_click)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = CodeRunnerApp()
    manager.show()
    QTimer.singleShot(0, manager._post_init_setup)
    sys.exit(app.exec())
