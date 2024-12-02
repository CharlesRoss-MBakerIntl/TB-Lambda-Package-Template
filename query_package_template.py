

#Set List of Available Projects
project_list = ['Helene', "Milton"]

#User Selected Project
sel_project = ""

#Project Dictionary
project_dict = {
    "Helene": 34,
    'Mitlon': 0 
}

#Singe, Nested Dictionary
single_repeat_dict = {
    {"Single":{
        'source_id': "id",
        'join_id': 'application_id'}
    },

    {"Repeating": {
        'source': 'repeating_answer_section_id',
        'join_id': 'repeating_answer_section_id'}
    }
}




# Create Source Information
source = {
    #Main for Joining as Application ID as Unique ID
    'table': 'applications_application',

    #Alias Name for Table
    'name' : 'app',

    #Fields to Pull from 
    'fields': [{'application_number' : 'application_number',
                       'created_at' : 'created_at'}],

    #Which Overal Project to Pull Data from, Comes from User Selection
    'project': project_dict[sel_project],

    #Orders by Application ID
    'order': 'id'
}




# Create Join List, Contains Each Column of Data that Needs to be Pulled and its Cleaning Instructions. Example has first package for a single row of data available, for additonal data, copy, paste, and fill out the next section.
join_list = [
    
    
    {
     #Step Name for SQL Join, this is used throughout the SQL pull to reference the step.
     'name': 'hotel_name',

     #Soure of Question, Either JOIN_SOURCE or DATA_SOURCE
     'question_source': 'JOIN_SOURCE',
    
     #Used to differentiate between whether this is a single return value or if there is a nested set of values in the form.  
     'single_repeating': 'SINGLE',

     #The datasource table that the question is being pulled from.  For example, if the question is a number entry, then the data source table
     #will be sources from 'application_data_numberanswer'
     'data_source': 'application_data_textboxanswer',

     #This is the question id that is what the question is stored as in the postgresql database. A reference to this can be found when using the tb_find_fields package. 
     'question_id': 1015,

     #Fields to Pull from Table.  First part needs to be the name of the field in the joined table,
     #This can be found in the PostgreSQL application under the data source table.
     #Format of this item is a list that contains a dictionary. The keys in the dictionary are the names of the 
     #field that appears in the data source table, and the values are the name of the field you want to appear in the
     #final table.
     'fields' : [{'value':'hotel_name'}],

     #Cleaning for the field, a list of fucntions can be found in rds_clean_utils.py. Format will be a list that contains
     #a dictionary, the keys are the name of the field that will appear in the final table, and a code name for the cleaning step ex. DATE_CONVERT
     'clean' : []
    },


    {'name': 'hotel_address',
     'question_source': 'DATA_SOURCE',
     'single_or_repeat': 'SINGLE',
     'question_id': 1016,
     'data_source': 'application_data_addressanswer',
     'fields': [{'line1':'hotel_address_line_1',
                 'line2': 'hotel_address_line_2',
                 'city' : 'hotel_city',
                 'state': 'hotel_state',
                 'zip' : 'hotel_zip'}],
     'clean' : []
    },

    {'name': 'hotel_status',
     'question_source': 'DATA_SOURCE',
     'source_id': 'repeating_answer_section_id',
     'join_id': 'repeating_answer_section_id',
     'data_source': 'application_data_singleselectanswer',
     'question_id': 1013,
     'fields': [{'value':'hotel_status'}],
     'clean' : []
    },

    {'name': 'license_in',
     'question_source': 'DATA_SOURCE',
     'source_id': 'repeating_answer_section_id',
     'join_id': 'repeating_answer_section_id',
     'data_source': 'application_data_dateanswer',
     'question_id': 1021,
     'fields': [{'value':'license_in'}],
     'clean' : [{'license_in': ['DATE_CONVERT']}]
    },

    {'name': 'license_out',
     'question_source': 'DATA_SOURCE',
     'source_id': 'repeating_answer_section_id',
     'join_id': 'repeating_answer_section_id',
     'data_source': 'application_data_dateanswer',
     'question_id': 1022,
     'fields': [{'value':'license_out'}],
     'clean' : [{'license_out': ['DATE_CONVERT']}]
    },

    {'name': 'total_in_household',
     'question_source': 'JOIN_SOURCE',
     'source_id': 'id',
     'join_id': 'application_id',
     'data_source': 'application_data_numberanswer',
     'question_id': 596,
     'fields': [{'value':'total_in_household'}],
     'clean' : []
    },

    {'name': 'active_bookings',
     'question_source': 'JOIN_SOURCE',
     'source_id': 'id',
     'join_id': 'application_id',
     'data_source': 'application_data_numberanswer',
     'question_id': 1010,
     'fields': [{'value':'active_bookings'}],
     'clean' : []
    },

    {'name': 'pathway_determination',
     'question_source': 'JOIN_SOURCE',
     'source_id': 'id',
     'join_id': 'application_id',
     'data_source': 'application_data_singleselectanswer',
     'question_id': 632,
     'fields': [{'value':'pathway_determination'}],
     'clean' : []
    }
]


# Create Query Package
query_package = {'source':source, 'join_list': join_list}


# Function to Return Package
def get_query_package():
    return query_package