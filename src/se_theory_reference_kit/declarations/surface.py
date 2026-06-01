"""declarations/surface.py - Repo-owned Lean public surface declaration shape."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Self

EMPTY_SURFACE_MAP: dict[str, frozenset[str]] = {}
EMPTY_STRING_SET: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class SurfaceSymbols:
    """Kinded public Lean surface symbols for one theory repository."""

    by_kind: Mapping[str, frozenset[str]] = field(
        default_factory=lambda: EMPTY_SURFACE_MAP
    )

    def symbols_for_kind(self, kind: str) -> frozenset[str]:
        """Return public symbols for one surface kind."""
        return self.by_kind.get(kind, EMPTY_STRING_SET)

    @property
    def all_symbols(self) -> frozenset[str]:
        """Return all declared public surface symbols."""
        return frozenset(
            symbol for symbols in self.by_kind.values() for symbol in symbols
        )

    @classmethod
    def from_optional_kinds(
        cls,
        *,
        types: frozenset[str] = EMPTY_STRING_SET,
        predicates: frozenset[str] = EMPTY_STRING_SET,
        axioms: frozenset[str] = EMPTY_STRING_SET,
        theorems: frozenset[str] = EMPTY_STRING_SET,
        requirements: frozenset[str] = EMPTY_STRING_SET,
        vocabulary: frozenset[str] = EMPTY_STRING_SET,
        witnesses: frozenset[str] = EMPTY_STRING_SET,
    ) -> Self:
        """Build a surface declaration from common optional surface kinds."""
        return cls(
            by_kind={
                "type": types,
                "predicate": predicates,
                "axiom": axioms,
                "theorem": theorems,
                "requirement": requirements,
                "vocabulary": vocabulary,
                "witness": witnesses,
            }
        )
