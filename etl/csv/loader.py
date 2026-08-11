class CSVLoader:
    def load(self, manager, database, df):
        # prepare data to insert
        orders = [
            (row.order_id, row.order_date, row.total_value)
            for row in df.itertuples(index=False)
        ]
        # insert data into right database using the manager
        manager.insert_orders(database, orders)
