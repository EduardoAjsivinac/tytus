from AST.sentence import InsertAll, Insert
from storageManager.TypeChecker_Manager import *
from storageManager.jsonMode import *

import sys
sys.path.append("../")
from console import print_error, print_success


#def insert(database: str, table: str, register: list) -> int:
#0 -> Successful operation
#1 -> Operation error    
#2 -> Database does not exist
#3 -> Table does not exist
#4 -> Duplicate primary key
#5 -> Columns out of bounds
#anything else -> Operation error

def executeInsertAll(self, InsertAll_):

    # InsertAll : {
    #     table: "table_name",
    #     values: [ { type: ('Entero' | 'Decimal' | 'Cadena' | 'Variable' | 'Regex' | 'All'), value: "" } ]
    #     #values: [ { type: (1       | 2         |  3       |  4         | 5       | 6    ), value: "" } ]
    # }

    # Insert : {
    #     table: "table_name",
    #     columns: [ "column_name", "column_name" ],
    #     values: [ { type: ('Entero' | 'Decimal' | 'Cadena' | 'Variable' | 'Regex' | 'All'), value: "" } ]
    #     #values: [ { type: (1       | 2         |  3       |  4         | 5       | 6    ), value: "" } ]
    # }
    
    insertAll: InsertAll = InsertAll_
    table_name = insertAll.table
    values = insertAll.values
    
    TypeChecker_Manager_ = get_TypeChecker_Manager()
    if  TypeChecker_Manager_ != None:
        
        use_: str = get_use(TypeChecker_Manager_)
        if use_ != None:
            
            database_ = get_database(use_, TypeChecker_Manager_)
            if database_ != None:
                
                table_ = get_table(table_name, database_)
                if table_ != None:
                    
                    if len(table_.columns) == len(values):
                        
                        check_type_ = check_type(table_.columns, values)
                        if check_type_ == None:
                        
                            check_null_ = check_null(table_.columns, values)
                            if check_null_ == None:

                                check_maxlength_ = check_maxlength(table_.columns, values)
                                if check_maxlength_ == None:

                                    check_checks_ = check_checks(table_.columns, values)
                                    if check_checks_ == None:
                                        
                                        try:
                                            #success
                                            values_list = []
                                            i = 0
                                            while i < len(values):
                                                values_list.append(values[i].value)
                                                i += 1
                                            result_insert= insert(database_.name, table_.name, values_list)
                                            if result_insert == 0:
                                                print_success("QUERY", "Insert in " + str(table_.name) + " table, done successfully")
                                            elif result_insert == 1:
                                                print_error("Unknown Error", "Operation error")
                                            elif result_insert == 2:
                                                print_error("Semantic Error", "Database does not exist")
                                            elif result_insert == 3:
                                                print_error("Semantic Error", "Table does not exist")
                                            elif result_insert == 4:
                                                print_error("Semantic Error", "Duplicate primary key")
                                            elif result_insert == 5:
                                                print_error("Semantic Error", "Columns out of bounds")
                                            else:
                                                print_error("Unknown Error", "Operation error")
                                        except Exception as e:
                                            print_error("Unknown Error", "instruction not executed")
                                            #print(e)

                                    else:
                                        print_error("Semantic Error", check_checks_)

                                else:
                                    print_error("Semantic Error", check_maxlength_)

                            else:
                                print_error("Semantic Error", check_null_)

                        else:
                            print_error("Semantic Error", check_type_)
                        
                    else:
                        print_error("Semantic Error", "Wrong arguments submitted for table. " + str(len(table_.columns)) + " required and " + str(len(values)) + " received")

                else:
                    print_error("Semantic Error", "Table does not exist")

            else:
                print_error("Semantic Error", "Database to use does not exist")

        else:
            print_error("Runtime Error", "Undefined database to use")
    else:
        print_error("Unknown Error", "instruction not executed")


type_int = ["SMALLINT", "INTEGER", "BIGINT", "REAL"]
type_float = ["DECIMAL", "NUMERIC", "DOUBLE PRECISION", "PRECISION", "MONEY"]
type_char = ["CHARACTER", "CHAR", "TEXT"]
type_string = ["TEXT"]
# type_bool = ["BOOLEAN"]
# | TIMESTAMP
# | DATE
# | TIME 
# | INTERVAL
# | TIME WITHOUT TIME ZONE
# | TIME WITH TIME ZONE
# | INTERVAL INT
# | TIMESTAMP WITH TIME ZONE
# | ID


def check_type(columns_, values_) -> str:

    return_ = None

    i = 0
    while i < len(columns_):
        
        column_type = ((str(columns_[i].type_)).upper())        

        if ( column_type in type_int ) == True:
            if values_[i].type != 1:
                return_ = "Argument " + str((i+1)) + " of wrong type. It should be a " + str(column_type) + " type."
                i = len(columns_)
        
        elif ( column_type in type_float ) == True:
            if values_[i].type != 2:
                return_ = "Argument " + str((i+1)) + " of wrong type. It should be a " + str(column_type) + " type."
                i = len(columns_)
        
        elif ( column_type in type_char ) == True:
            if values_[i].type != 3:
                return_ = "Argument " + str((i+1)) + " of wrong type. It should be a " + str(column_type) + " type."
                i = len(columns_)
        
        elif ( column_type in type_string ) == True:
            if values_[i].type != 3:
                return_ = "Argument " + str((i+1)) + " of wrong type. It should be a " + str(column_type) + " type."
                i = len(columns_)
        
        i += 1

    return return_


def check_null(columns_, values_) -> str:

    return_ = None

    i = 0
    while i < len(columns_):

        if columns_[i].null_ != None:
            if columns_[i].null_ == False:
                if values_[i].value == None:
                    return_ = "Argument " + str((i+1)) + " is null and the column does not allow null values."
                    i = len(columns_)

        i += 1

    return return_


def check_maxlength(columns_, values_) -> str:

    return_ = None

    i = 0
    while i < len(columns_):

        if columns_[i].maxlength_ != None:
            if ( columns_[i].maxlength_ < len(str(values_[i].value)) ) == True:
                return_ = "Argument " + str((i+1)) + " exceeds the maximum length allowed by the column."
                i = len(columns_)

        i += 1

    return return_


def check_checks(columns_, values_) -> str:

    return_ = None
    error_encontrado = False

    i = 0
    while i < len(columns_) and error_encontrado == False:

        value = str(values_[i].value)
        j = 0
        while j < len(columns_[i].checks) and error_encontrado == False:

            check_operation = columns_[i].checks[j].operation
            check_value = columns_[i].checks[j].value

            if str(check_operation) == "<":
                if not(str(value) < str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            elif str(check_operation) == ">":
                if not(str(value) > str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            elif str(check_operation) == "<=":
                if not(str(value) <= str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            elif str(check_operation) == ">=":
                if not(str(value) >= str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            elif str(check_operation) == "==":
                if not(str(value) == str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            elif str(check_operation) == "!=":
                if not(str(value) != str(check_value)):
                    return_ = "Argument " + str((i+1)) + " must be " + str(check_operation) + " to "
                    is_int_or_float_ = is_int_or_float(check_value)
                    if is_int_or_float_== True:
                        return_ += str(check_value) + "."
                    else:
                        return_ += "\"" + str(check_value) + "\"."
                    error_encontrado = True
            
            j += 1

        i += 1

    return return_