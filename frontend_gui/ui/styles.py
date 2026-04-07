"""Qt Stylesheet and color constants for the QLSVSDH GUI.

Follows the python-patterns and frontend-design skills:
- CSS variables replaced with Qt QSS equivalent
- Dark professional palette suitable for enterprise data apps
- Consistent spacing using 4px grid
"""
from __future__ import annotations

from qtpy.QtCore import QColor, Qt
from qtpy.QtGui import QFont, QPalette
from qtpy.QtWidgets import QApplication


# ── Colors ──────────────────────────────────────────────────────────────
DARK_BG      = "#1a1a2e"
SURFACE      = "#16213e"
SURFACE2     = "#0f3460"
ACCENT       = "#e94560"
ACCENT_HOVER = "#ff6b6b"
TEXT_PRIMARY = "#eaeaea"
TEXT_SECOND  = "#94a3b8"
BORDER       = "#2a3a5e"
SUCCESS      = "#10b981"
WARNING      = "#f59e0b"
ERROR        = "#ef4444"
INFO         = "#3b82f6"


def _apply_palette(app: QApplication) -> None:
    """Apply dark palette to application for native Qt controls."""
    dark = QPalette()
    dark.setColor(QPalette.Window,           QColor(DARK_BG))
    dark.setColor(QPalette.WindowText,        QColor(TEXT_PRIMARY))
    dark.setColor(QPalette.Base,             QColor(SURFACE))
    dark.setColor(QPalette.AlternateBase,    QColor(SURFACE2))
    dark.setColor(QPalette.ToolTipBase,      QColor(SURFACE2))
    dark.setColor(QPalette.ToolTipText,      QColor(TEXT_PRIMARY))
    dark.setColor(QPalette.Text,             QColor(TEXT_PRIMARY))
    dark.setColor(QPalette.Button,           QColor(SURFACE2))
    dark.setColor(QPalette.ButtonText,        QColor(TEXT_PRIMARY))
    dark.setColor(QPalette.BrightText,       QColor(ACCENT))
    dark.setColor(QPalette.Highlight,        QColor(ACCENT))
    dark.setColor(QPalette.HighlightedText,  QColor(DARK_BG))
    dark.setColor(QPalette.Link,             QColor(INFO))
    dark.setColor(QPalette.LinkVisited,      QColor(ACCENT))
    dark.setColor(QPalette.PlaceholderText,   QColor(TEXT_SECOND))
    dark.setColor(QPalette.Disabled, QPalette.WindowText, QColor(TEXT_SECOND))
    dark.setColor(QPalette.Disabled, QPalette.Text,       QColor(TEXT_SECOND))
    app.setPalette(dark)


def _base_font(size: int = 10, weight: int = 50) -> QFont:
    f = QFont("Segoe UI", size)
    f.setWeight(weight)
    return f


def base_stylesheet() -> str:
    """Base application-level stylesheet (applied before widgets load)."""
    return f"""
QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI";
    font-size: 10pt;
}}
QWidget#centralWidget {{
    background-color: {DARK_BG};
}}
QFrame#sidebar {{
    background-color: {SURFACE};
    border-right: 1px solid {BORDER};
}}
QListWidget#navList {{
    background-color: {SURFACE};
    border: none;
    outline: none;
    padding: 8px 0;
}}
QListWidget#navList::item {{
    padding: 10px 16px;
    border: none;
    color: {TEXT_SECOND};
    font-size: 10pt;
}}
QListWidget#navList::item:selected {{
    background-color: {SURFACE2};
    color: {ACCENT};
    border-left: 3px solid {ACCENT};
}}
QListWidget#navList::item:hover:!selected {{
    background-color: {SURFACE2};
    color: {TEXT_PRIMARY};
}}
QLabel#header {{
    color: {TEXT_PRIMARY};
    font-size: 18pt;
    font-weight: 600;
}}
QLabel#subheader {{
    color: {TEXT_SECOND};
    font-size: 10pt;
}}
QLabel#cardValue {{
    color: {ACCENT};
    font-size: 22pt;
    font-weight: 700;
}}
QLabel#cardLabel {{
    color: {TEXT_SECOND};
    font-size: 9pt;
}}
QPushButton {{
    background-color: {SURFACE2};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 16px;
    min-width: 80px;
}}
QPushButton:hover {{
    background-color: {SURFACE2};
    border-color: {ACCENT};
    color: {ACCENT};
}}
QPushButton:pressed {{
    background-color: {SURFACE};
}}
QPushButton:disabled {{
    background-color: {DARK_BG};
    border-color: {BORDER};
    color: {TEXT_SECOND};
}}
QPushButton#primaryBtn {{
    background-color: {ACCENT};
    color: {DARK_BG};
    border-color: {ACCENT};
    font-weight: 600;
}}
QPushButton#primaryBtn:hover {{
    background-color: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
    color: {DARK_BG};
}}
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {ACCENT};
}}
QLineEdit:disabled, QTextEdit:disabled {{
    background-color: {DARK_BG};
    color: {TEXT_SECOND};
}}
QTableWidget, QTableView {{
    background-color: {SURFACE};
    alternate-background-color: {SURFACE2};
    gridline-color: {BORDER};
    border: 1px solid {BORDER};
    border-radius: 6px;
    grid-colored: true;
}}
QTableWidget::item, QTableView::item {{
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: {SURFACE2};
    color: {TEXT_PRIMARY};
    padding: 8px 10px;
    border: none;
    border-right: 1px solid {BORDER};
    font-weight: 600;
    font-size: 10pt;
}}
QHeaderView::section:hover {{
    background-color: {SURFACE};
}}
QTabWidget::pane {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px;
}}
QTabBar::tab {{
    background-color: {SURFACE2};
    color: {TEXT_SECOND};
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {SURFACE};
    color: {ACCENT};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_PRIMARY};
}}
QComboBox {{
    background-color: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 12px;
}}
QComboBox:hover {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    selection-background-color: {SURFACE2};
    outline: none;
}}
QMessageBox {{
    background-color: {SURFACE};
}}
QScrollBar:vertical {{
    background-color: {DARK_BG};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {SURFACE2};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {BORDER};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background-color: {DARK_BG};
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background-color: {SURFACE2};
    border-radius: 4px;
    min-width: 20px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {BORDER};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QGroupBox {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 12px;
    margin-top: 8px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
    color: {ACCENT};
}}
QToolTip {{
    background-color: {SURFACE2};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 4px 8px;
}}
"""


def configure_app(app: QApplication) -> None:
    """Configure app-wide styles and palette. Call once before show()."""
    _apply_palette(app)
    app.setStyleSheet(base_stylesheet())
    app.setFont(_base_font())