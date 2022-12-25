# What is generic table template

It is ninja template to render db records as a table

# Variables needed

- ```title``` : the title
- ```order_by_col_no``` : column number to sort by starts with 0
- ```col_names``` : a dictionary that contains column names and their type. Dictionary key matches column name and dictionary value matches column type as a text. Column types are strings such as "date", "numeric", which are evaluated and based on the column type the template renders them with appropriate format. Specifically it uses ```momentum``` library to render date or datetime values. It renders with comman notation numeric values.
- ```records``` : ORM (object relational mapping) records
- ```remove_func_name``` : the function name as string that is responsible for removing a record
- ```edit_func_name``` : the function name as string that is responsible for editing a record

# How it works

It prints header by iterating over ````col_names```
It iterates over records to render them.
For each record, it iterates over ```col_names``` dictionary by accessing both keys and values. And depending on the column type it renders the record field with appropriate format.


