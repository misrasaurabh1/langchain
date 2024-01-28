from typing import Dict, Tuple, Union

from langchain.chains.query_constructor.ir import (
    Comparator,
    Comparison,
    Operation,
    Operator,
    StructuredQuery,
    Visitor,
)


class PineconeTranslator(Visitor):
    """Translate `Pinecone` internal query language elements to valid filters."""

    allowed_comparators = (
        Comparator.EQ,
        Comparator.NE,
        Comparator.LT,
        Comparator.LTE,
        Comparator.GT,
        Comparator.GTE,
        Comparator.IN,
        Comparator.NIN,
    )
    """Subset of allowed logical comparators."""
    allowed_operators = (Operator.AND, Operator.OR)
    """Subset of allowed logical operators."""

    def _format_func(self, func: Union[Operator, Comparator]) -> str:
        self._validate_func(func)
        return f"${func.value}"

    def visit_operation(self, operation: Operation) -> Dict:
        args = [arg.accept(self) for arg in operation.arguments]
        return {self._format_func(operation.operator): args}

    def visit_comparison(self, comparison: Comparison) -> Dict:
        if comparison.comparator in (Comparator.IN, Comparator.NIN) and not isinstance(
            comparison.value, list
        ):
            comparison.value = [comparison.value]

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


def _validate_func(self, func: Union[Operator, Comparator]) -> None:
    func_type_allowed, type_name = (
        (self.allowed_operators, "operator")
        if isinstance(func, Operator)
        else (self.allowed_comparators, "comparator")
        if isinstance(func, Comparator)
        else (None, None)
    )

    if func_type_allowed is not None and func not in func_type_allowed:
        raise ValueError(
            f"Received disallowed {type_name} {func}. Allowed "
            f"comparators are {func_type_allowed}"
        )
