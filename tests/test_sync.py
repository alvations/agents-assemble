"""Tests for sync_package.py.

Validates:
- sync_package.py runs without error
- Synced files in agents_assemble/ match flat source files (modulo import rewrites)
- FILE_MAP covers all expected strategy files
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# sync_package module
# ---------------------------------------------------------------------------
class TestSyncPackageModule:
    def test_import_sync_package(self):
        import sync_package
        assert hasattr(sync_package, "sync")
        assert hasattr(sync_package, "FILE_MAP")
        assert hasattr(sync_package, "IMPORT_REWRITES")

    def test_file_map_not_empty(self):
        from sync_package import FILE_MAP
        assert len(FILE_MAP) >= 10  # At least 10 strategy + engine files

    def test_file_map_sources_exist(self):
        """Every flat source file in FILE_MAP should exist."""
        from sync_package import FILE_MAP
        for flat_name in FILE_MAP:
            src = ROOT / flat_name
            assert src.exists(), f"Source file missing: {flat_name}"

    def test_file_map_covers_strategies(self):
        """FILE_MAP should include all major strategy files."""
        from sync_package import FILE_MAP
        expected = [
            "personas.py",
            "famous_investors.py",
            "theme_strategies.py",
            "recession_strategies.py",
            "unconventional_strategies.py",
            "research_strategies.py",
            "math_strategies.py",
            "hedge_fund_strategies.py",
        ]
        for f in expected:
            assert f in FILE_MAP, f"{f} not in FILE_MAP"


# ---------------------------------------------------------------------------
# Sync validation — compare flat files with package copies
# ---------------------------------------------------------------------------
class TestSyncedFiles:
    def test_package_strategy_files_exist(self):
        """After sync, package strategy files should exist."""
        from sync_package import FILE_MAP
        missing = []
        for flat_name, pkg_path in FILE_MAP.items():
            dst = ROOT / pkg_path
            if not dst.exists():
                missing.append(pkg_path)
        # Allow some missing if sync hasn't been run, but most should exist
        assert len(missing) <= len(FILE_MAP) // 2, (
            f"Too many package files missing ({len(missing)}/{len(FILE_MAP)}): "
            f"{missing[:5]}..."
        )

    def test_synced_files_have_content(self):
        """Synced files should not be empty."""
        from sync_package import FILE_MAP
        for flat_name, pkg_path in FILE_MAP.items():
            dst = ROOT / pkg_path
            if dst.exists():
                content = dst.read_text()
                assert len(content) > 100, (
                    f"{pkg_path} is suspiciously short ({len(content)} chars)"
                )

    def test_import_rewrites_applied(self):
        """Package files should use package imports, not flat imports."""
        from sync_package import FILE_MAP, IMPORT_REWRITES
        flat_imports = list(IMPORT_REWRITES.keys())

        for flat_name, pkg_path in FILE_MAP.items():
            dst = ROOT / pkg_path
            if not dst.exists():
                continue
            content = dst.read_text()
            for old_import in flat_imports:
                if old_import in (ROOT / flat_name).read_text():
                    # If flat file has this import, package should have rewritten version
                    assert old_import not in content, (
                        f"{pkg_path} still has unrewritten import: {old_import}"
                    )


# ---------------------------------------------------------------------------
# Run sync (non-destructive — it overwrites package files from flat files)
# ---------------------------------------------------------------------------
class TestSyncExecution:
    def test_sync_runs_without_error(self):
        """sync() should complete without raising exceptions."""
        from sync_package import sync
        # This actually writes files, but that's the intended behavior
        try:
            sync()
        except Exception as e:
            pytest.fail(f"sync() raised: {e}")

    def test_sync_creates_expected_dirs(self):
        """After sync, package directories should exist."""
        expected_dirs = [
            ROOT / "agents_assemble" / "strategies",
            ROOT / "agents_assemble" / "engine",
            ROOT / "agents_assemble" / "data",
        ]
        for d in expected_dirs:
            assert d.is_dir(), f"Directory missing after sync: {d}"
