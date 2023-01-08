# What is generic table template

It is ninja template to render db records as a table

# Variables needed

- ```title``` : the title
- ```order_by_col_no``` : column number to sort by starts with 0
- ```summary_records``` : a list of ```DotDict``` objects. ```DotDict``` is just a dictionary whose keys can be accessed by dot. Each ```DotDict``` in *summary_records* has below key values.
  - *description* : Description of a summary record
  - *type* : data type of the summary record. This can be "date", "numeric" or "text"
  - *value* : the value of the summary record
- ```col_names``` : a list of ```DotDict``` records that describe each column of database record. Each ```DotDict``` will have below key value pairs:
  - *description* : This will appear as table column name of table record
  - *db_name* : This is column name of the record field in database table
  - *type* : data type of the record field. Column types are strings such as "date", "numeric", which are evaluated and based on the column type the template renders them with appropriate format. Specifically it uses ```momentum``` library to render date or datetime values. It renders with comman notation numeric values.
- ```records``` : ORM (object relational mapping) records
- ```add_func_name``` : the function name as string is responsible to add records. Ex: "admin_bp.add_new_shipment_weight"
- ```remove_func_name``` : the function name as string that is responsible for removing a record
- ```edit_func_name``` : the function name as string that is responsible for editing a record

# How it works

It prints header by iterating over *col_names*
It iterates over records to render them.
For each record, it iterates over *col_names*
, list of ```DotDict``` s and renders field values by accessing *db_name* of ```DotDict```. Also it formats the field by accessing *type* of ```DotDict```


