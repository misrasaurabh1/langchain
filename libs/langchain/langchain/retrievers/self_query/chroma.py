from typing import Dict, Tuple, Union

from langchain.chains.query_constructor.ir import (
    Comparator,
    Comparison,
    Operation,
    Operator,
    StructuredQuery,
    Visitor,
)


class ChromaTranslator(Visitor):
    """Translate `Chroma` internal query language elements to valid filters."""

    allowed_operators = [Operator.AND, Operator.OR]
    """Subset of allowed logical operators."""
    allowed_comparators = [
        Comparator.EQ,
        Comparator.NE,
        Comparator.GT,
        Comparator.GTE,
        Comparator.LT,
        Comparator.LTE,
    ]
    """Subset of allowed logical comparators."""

    def _format_func(self, func: Union[Operator, Comparator]) -> str:
        if isinstance(func, Operator):
            self._validate_operator_func(func)
        elif isinstance(func, Comparator):
            self._validate_comparator_func(func)
        return f"${func.value}"

    def visit_operation(self, operation: Operation) -> Dict:
        args = [arg.accept(self) for arg in operation.arguments]
        return {self._format_func(operation.operator): args}

    def visit_comparison(self, comparison: Comparison) -> Dict:
        return {
            comparison.attribute: {
                self._format_func(comparison.comparator): comparison.value
            }
        }

    def visit_structured_query(
        self, structured_query: StructuredQuery
    ) -> Tuple[str, dict]:
        if structured_query.filter is None:
            kwargs = {}
        else:
            kwargs = {"filter": structured_query.filter.accept(self)}
        return structured_query.query, kwargs


def _validate_operator_func(self, func: Operator) -> None:
    if self.allowed_operators is not None and func not in self.allowed_operators:
        raise ValueError(
            f"Received disallowed operator {func}. Allowed "
            f"operators are {self.allowed_operators}"
        )


def _validate_comparator_func(self, func: Comparator) -> None:
    if self.allowed_comparators is not None and func not in self.allowed_comparators:
        raise ValueError(
            f"Received disallowed comparator {func}. Allowed "
            f"comparators are {self.allowed_comparators}"
        )
