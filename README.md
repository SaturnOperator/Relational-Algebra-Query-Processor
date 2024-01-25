# Relational Algebra Query Processor

```
January 24, 2023
COMP 3005
```

## Video Demo

https://youtu.be/c0vPJ9s8WdM

## Supported Operations

### Selection

The selection operand works by using the `--select` argument then specifying the table name first followed by as many columns as you want to display.

Here is an example to query a column named `names` from the `friends` table: 

```bash
python3 query_process.py --select 'friends' 'name'
```

You can add as many columns as you want to select or display:

```bash
python3 query_process.py --select 'friends' 'name' 'city' 'age'
```



### Projection

You can use a matching operand by adding an inequality to the `--select` argument after listing the column name, this supports `>`, `>=`, `<`, `<=`, and `==` conditions. This function adds onto the existing select operand. 

For example adding `age>25` will only return matches where the `age` value is above 25. *Note: we also need to include `age`* to also show the age column, adding the inequality is evaluated as a match rather than select.

```bash
python3 query_process.py --select 'friends' 'name' 'age' 'age>25'
```

Just like with the selection operand, you can also add multiple inequalities:

```bash
python3 query_process.py --select 'friends' 'name' 'age' 'age>25' 'city' 'city==Ottawa'
```



### Set

You can update fields using the `--set` column, it takes a column name and a value as arguments. You need to add the `--set` argument after a selection query, the matched results will be updated.

Here is an example that will set all `city` entries to `Vancouver` as the select operand has no match filter. 

```bash
python3 query_process.py --select 'friends' 'city' --set 'city' 'Vancouver'
```

This example uses the matching operand to only use the `--set` operand in certain conditions, in this only when `age>25` and `city==Ottawa`:

```bash
python3 query_process.py --select 'friends' 'age>25' 'city==Ottawa' --set 'city' 'Vancouver'
```



### Join

The `--join` operand works by providing two tables and a column to match.

Here's an example that appends the properties of table 2 to table 1 based on the given matching column:

```bash
python3 query_process.py --join 'friends' 'universities' 'city' 
```

This query will assign the respective university in that city to each friend.
