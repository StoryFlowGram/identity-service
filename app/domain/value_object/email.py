from dataclasses import dataclass
import re
from app.domain.value_object.error import DomainValidationError
from typing import Tuple

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise DomainValidationError("Email должен быть строкой")
        normalized = self.value.strip().lower()
        if not normalized:
            raise DomainValidationError("Email не должен быть пустой")
        if not _EMAIL_RE.match(normalized):
            raise DomainValidationError(f"Некорректный email: {self.value!r}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value

    def parts(self) -> Tuple[str, str]:
        local, _, domain = self.value.partition("@")
        return local, domain

    @property
    def domain(self) -> str:
        return self.parts()[1]

    def is_same_domain(self, other_domain: str) -> bool:
        return self.domain == (other_domain or "").strip().lower()