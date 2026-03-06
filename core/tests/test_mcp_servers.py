"""MCP server smoke tests — verify each server imports and has a server object."""

import importlib

import pytest

# (module_path, attribute_name)
SERVERS = [
    ("core.mcp.work_server", "app"),
    ("core.mcp.career_server", "app"),
    ("core.mcp.resume_server", "app"),
    ("core.mcp.calendar_server", "app"),
    ("core.mcp.commitment_server", "server"),
    ("core.mcp.onboarding_server", "app"),
    ("core.mcp.demo_mode_server", "server"),
    ("core.mcp.session_memory_server", "app"),
    ("core.mcp.update_checker", "mcp"),
]


@pytest.mark.parametrize(
    "module_path,attr_name",
    SERVERS,
    ids=[m.rsplit(".", 1)[-1] for m, _ in SERVERS],
)
def test_server_imports_and_has_object(module_path: str, attr_name: str):
    """Each MCP server module should import without error and expose its server object."""
    mod = importlib.import_module(module_path)
    assert hasattr(mod, attr_name), (
        f"{module_path} imported OK but has no '{attr_name}' attribute"
    )
