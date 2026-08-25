import unittest
from unittest.mock import patch

from secretdataagent.tools import run_sql_query, validate_sql_query


REPORTED_QUERY = '''
SELECT COALESCE(SUM("TransactionAmount"), 0) AS total_investments
FROM "SecretTransactions"
WHERE "IsDeleted" = false
  AND "LedgerType" = 'Investments'
  AND "PartitionKey" = TO_CHAR(CURRENT_DATE, 'Mon-YYYY')
'''


class ToolTests(unittest.TestCase):
    def test_validate_reported_postgresql_query(self):
        self.assertEqual(
            validate_sql_query.invoke({"sql_query": REPORTED_QUERY}), "VALID"
        )


    def test_validate_accepts_read_only_with_query(self):
        query = "WITH totals AS (SELECT 1 AS value) SELECT value FROM totals"

        self.assertEqual(validate_sql_query.invoke({"sql_query": query}), "VALID")


    def test_validate_rejects_malformed_sql(self):
        result = validate_sql_query.invoke({"sql_query": "SELECT FROM"})

        self.assertTrue(result.startswith("INVALID:"))


    def test_validate_rejects_multiple_statements(self):
        result = validate_sql_query.invoke({"sql_query": "SELECT 1; SELECT 2"})

        self.assertEqual(result, "INVALID: only one SQL statement is allowed")


    def test_validate_rejects_write_statements(self):
        result = validate_sql_query.invoke(
            {"sql_query": "DELETE FROM \"SecretTransactions\""}
        )

        self.assertEqual(result, "INVALID: only read-only queries are allowed")


    def test_run_sql_query_does_not_execute_invalid_sql(self):
        with patch(
            "secretdataagent.tools.postgres_client.execute_query"
        ) as execute_query:
            result = run_sql_query.invoke({"sql_query": "DROP TABLE users"})

        self.assertEqual(result, "INVALID: only read-only queries are allowed")
        execute_query.assert_not_called()


    def test_run_sql_query_executes_valid_sql(self):
        with patch(
            "secretdataagent.tools.postgres_client.execute_query",
            return_value=[{"value": 1}],
        ) as execute_query:
            result = run_sql_query.invoke({"sql_query": "SELECT 1 AS value"})

        self.assertEqual(result, "[{'value': 1}]")
        execute_query.assert_called_once_with("SELECT 1 AS value")
