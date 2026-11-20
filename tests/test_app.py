import os
import pytest
from streamlit.testing.v1 import AppTest
from src.ui import render_tailwind_header, render_kpi_card, render_insight_box

def test_ui_module_components():
    """TC-T-10: Verify reusable UI module functions callable without errors."""
    assert callable(render_tailwind_header)
    assert callable(render_kpi_card)
    assert callable(render_insight_box)

def test_config_toml_theme_presence():
    """TC-T-11A: Verify .streamlit/config.toml exists and configures the healthcare palette."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".streamlit", "config.toml"))
    assert os.path.exists(config_path), "Missing .streamlit/config.toml"
    with open(config_path, "r") as f:
        content = f.read()
    assert "primaryColor" in content
    assert "#2B6CB0" in content

def test_streamlit_apptest_startup():
    """TC-T-11B: Execute Streamlit AppTest on app.py to verify page renders without unhandled exceptions."""
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))
    assert os.path.exists(app_path), f"app.py missing at {app_path}"

    at = AppTest.from_file(app_path, default_timeout=15)
    at.run()
    assert not at.exception, f"Streamlit application encountered unhandled exception: {at.exception}"
