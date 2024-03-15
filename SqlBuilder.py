class SQLQueryBuilder:
    def __init__(self):
        self.query_type = None
        self.columns = None
        self.table = None
        self.joins = []
        self.conditions = []
        self.set_values = {}
        self.limit = None
        self.order_by = None

    def Select(self, *columns):
        self.query_type = "SELECT"
        self.columns = ", ".join(columns)
        return self

    def Insert(self, table, **values):
        self.query_type = "INSERT"
        self.table = table
        self.set_values = values
        return self

    def Update(self, table):
        self.query_type = "UPDATE"
        self.table = table
        return self

    def Delete(self, table):
        self.query_type = "DELETE"
        self.table = table
        return self

    def From(self, table):
        self.table = table
        return self

    def Join(self, table, on_condition, join_type="INNER"):
        self.joins.append((join_type, table, on_condition))
        return self

    def Where(self, condition):
        self.conditions.append(condition)
        return self

    def Set(self, **values):
        self.set_values = values
        return self

    def Limit(self, limit):
        self.limit = limit
        return self

    def OrderBy(self, column, order="ASC"):
        self.order_by = f"{column} {order}"
        return self

    def Build(self):
        if self.query_type == "SELECT":
            query = f"SELECT {self.columns} FROM {self.table}"
        elif self.query_type == "INSERT":
            query = f"INSERT INTO {self.table} ({', '.join(self.set_values.keys())}) VALUES ({', '.join(['%s']*len(self.set_values))})"
        elif self.query_type == "UPDATE":
            query = f"UPDATE {self.table} SET {', '.join([f'{key}=%s' for key in self.set_values.keys()])}"
        elif self.query_type == "DELETE":
            query = f"DELETE FROM {self.table}"

        for join in self.joins:
            join_type, join_table, on_condition = join
            query += f" {join_type} JOIN {join_table} ON {on_condition}"

        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        if self.order_by:
            query += f" ORDER BY {self.order_by}"
        if self.limit:
            query += f" LIMIT {self.limit}"

        if self.query_type == "UPDATE":
            query += " WHERE " + " AND ".join([f'{key}=%s' for key in self.set_values.keys()])

        return query

