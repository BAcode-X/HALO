<div align="center">

# HALO v0.1 📚
![python-3-9]
 <br>
  Simple Database Management System
 </br>
</div>


# Getting Started

Requirements:
* Python v3.0  or above

## Installation
```shell
git clone https://github.com/<username>/HALO
cd HALO
```

### HALO Authentication Language Operations
| Operation                 | Input Format                   |     OutPut                          |           
|---------------------------| :-------------------------------| :----------------------------|
| Register | register user <username_> <password_> <password_>   | None |
| Login    | login <username_> <password_> | None |
| Logout   | logout | None |


### HALO Definition Language Operations
| Operation                 | Input Format                   |     OutPut           |          
|---------------------------|:---------------------------|:----------------------|
| Create | create type <type_name> <no_of_field> <field_1> <fied_2>   | None |
| Delete    | delete type <type_name> | None |
| Inherit   | inherit type <target_type> <source_type> <additional_fields> | None |
| List    | list type | <type_1> <br> <type_2> <br> ... |
  
### HALO Management Language Operations
| Operation                 | Input Format                   |     OutPut                                     
|----------------------|:---------------------|:---------------------------|
| Create | create record <type_name> <field_1> <fied_2>   | None |
| Delete    | delete record <type_name> <pk> | None |
| Update    | update record <type_name> <pk> <field_2_value> <field_3_value> | None |
| Search    | search record <type_name> <pk> | <field_1_value> <field_2_value> ... |
| List   | list record <type_name> | <record1_field1_value> <record1_field2_value> ... <br> <record2_field1_value> <record2_field2_value> ... <br> ... |
| Filter  | filter record <type_name> <condition_> | <record1_field1_value> <record1_field2_value> ... <br> <record2_field1_value> <record2_field2_value> ... <br> ... |

 
  
[python-3-9]: https://img.shields.io/badge/Python-3.9-green
