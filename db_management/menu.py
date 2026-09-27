import create_json
import mongo_services
import modify_taxonomy_docs


# It's a menu that allows the user to choose what to do.
# :return: The menu() unless the user wants to exit.
def menu():
    print("Welcome, what would you like to do?")
    print("1. Insert rna_sequences files (.txt) into mongodb.")
    print("2. Insert additional files (.dbn, .fasta, .ct, .bpseq, with and without header).")
    print("3. Modify a single rna sequence.")
    print("4. Add one field to all documents in rna sequences collection.")
    print("5. Delete a single rna sequence.")
    print("6. Delete all.")
    print("7. Remove expired session's collections.")
    print("8. Create taxonomy file.")
    print("9. Insert a json file into mongodb.")
    print("0. Exit.")
    result = input("Insert the number of the action you want to do: ")
    if not result.isnumeric():
        print("Sorry, you have to insert a number.")
        menu()
    else:
        result = int(result)
    if result == 0:
        return
    elif result == 1:
        print("You chose to insert one or more txt files into mongo db.")
        output_path = create_json.read_files()
        print("Output Path: ", output_path)
        #mongo_services.insert_to_mongo(output_path)
        menu()
    elif result == 2:
        mongo_services.insert_files()
        menu()
    elif result == 3:
        print("You chose to update one document of mongo db.")
        mongo_services.update_one_field()
        menu()
    elif result == 4:
        print("You chose to add a field to all documents.")
        mongo_services.add_one_field_all_docs()
        menu()
    elif result == 5:
        print("You chose to delete one document of mongo db.")
        mongo_services.delete_one()
        menu()
    elif result == 6:
        print("You chose to delete all documents in a collection.")
        mongo_services.delete_all()
        menu()
    elif result == 7:
        print("You chose to delete all the expired session's collections.")
        mongo_services.delete_unused_collection()
        menu()
    elif result == 8:
        print("You chose to create the taxonomy file.")
        modify_taxonomy_docs.modify_file()
        menu()
    elif result == 9:
        print("You chose to add a json file into mongodb.")
        mongo_services.insert_to_mongo("files/json_files")
        menu()

menu()
