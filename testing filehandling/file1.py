
# b = 5
# while True:
#     try:
#         dep=int(input("ENTER======="))
#         print (type(dep))

#         b= b+dep
#         print(b)
#         break 
#     except Exception as e:
#         print("enter Valid") 
#         print("error======4",e)
# d= b+20
# print(d)       
#     # except Exception as e:
#     #     exc_type, exc_obj, exc_tb = sys.exc_info()
#     #     writeLog("File:dualcavity-->Method:dualCavityPO_load-->Line No:"+str(exc_tb.tb_lineno),str(e))
#     #     print(e)

import sys

def writeLog(location, error_message):
    try:
        # Open the log file in append mode, create it if it doesn't exist
        with open("error_log.txt", "a") as log_file:
            # Write the error details to the log file
            log_file.write(f"Location: {location}, Error: {error_message}\n")
    except Exception as e:
        # Print an error message if logging fails
        print(f"Error writing to log: {e}")
        
def write():
    b = 5
    while True:
        try:
            dep = int(input("ENTER======="))
            print(type(dep))

            b = b + dep
            print(b)
            break
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Error occurred at line {exc_tb.tb_lineno}:")
            print(f"Exception Type: {exc_type}")
            print(f"Exception Object: {exc_obj}")
            print(f"Traceback: {exc_tb}")
            
            
            # print("enter Valid")
            # print("error======4", e)
            # # Get exception information
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # # Log the error
            # writeLog(f"File:dualcavity-->Method:dualCavityPO_load-->Line No:{exc_tb.tb_lineno}", str(e))

    d = b + 20
    print(d)
write()
