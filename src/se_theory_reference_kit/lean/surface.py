"""lean/surface.py - Compare repo-owned public surface declarations."""

from se_theory_reference_kit.declarations.surface import SurfaceSymbols

__all__ = [
    "expected_symbols_for_kind",
    "missing_expected_surface_symbols",
]


def expected_symbols_for_kind(surface: SurfaceSymbols, kind: str) -> frozenset[str]:
    """Return expected public Lean symbols for a surface kind.

    Missing kinds return an empty set. The owning theory repository supplies the
    surface symbols; the kit only reads the generic shape.

    Args:
        surface: Repo-owned public surface declaration.
        kind: Surface kind.

    Returns:
        Expected symbols for that kind.
    """
    return surface.symbols_for_kind(kind)


def missing_expected_surface_symbols(
    *,
    surface: SurfaceSymbols,
    registered: set[str],
) -> set[str]:
    """Return expected public-surface symbols missing from reference registries.

    Args:
        surface: Repo-owned public surface declaration.
        registered: Lean symbols already registered in reference artifacts.

    Returns:
        Expected symbols not present in registered symbols.
    """
    return set(surface.all_symbols) - registered
