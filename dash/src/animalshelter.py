from pymongo import MongoClient

class AnimalShelter(object):
    """ CRUD operations for Animal collection in the AAC MongoDB.
    
    Attributes:
        user (string): Username for the the mongo database connection
        password (string): Password for the the mongo database connection
        
    Example:
        
        connection = AnimalShelter('myUser', 'myPassword')
        connection.create({"testKey":"testValue"})
        
    """

    
    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            port: int,
            db: str,
            collection: str
            ):
        
        # Check that init parameters were given
        if user is None:
            raise ValueError("user cannot be None")
        if password is None:
            raise ValueError("password cannot be None")
        if host is None:
            raise ValueError("host cannot be None")
        if port is None:
            raise ValueError("port cannot be None")
        if db is None:
            raise ValueError("db cannot be None")
        if collection is None:
            raise ValueError("password cannot be None")
        
        # Connection Variables
        #
        self.user = user
        self.password = password
        HOST = host
        PORT = port
        DB = db
        COL = collection
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (self.user,self.password,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

        
# Complete this create method to implement the C in CRUD.
    def create(self, data: dict) -> bool:
        """
        The create method creates a new document in the 
        animals collection.


        Parameters
        ----------
        data : dict
            Required. Input data for the new document.

        Returns
        -------
        bool
            MongoDB acknowledgement for data creation.
            True is a successful database write.
        
        Example
        -------
        
        connection.create({"testKey":"testValue"})

        """
        
        if data is None:
            raise Exception("Nothing to save, because data parameter is empty")
        if not isinstance(data, dict):
            raise Exception("Error, data parameter is not a dictionary")
        
        try:
            result = self.database.animals.insert_one(data)  # data should be dictionary
        except Exception as e:
            raise Exception(f"Error creating document: {e}")
        if result.acknowledged:
            return True
        else:
            return False
            
            
# Create method to implement the R in CRUD.
    def read(self, data_filter: dict = None) -> list:
        """
        The read method fetches documents that meet the provided filter.

        Parameters
        ----------
        data_filter : dict
            Key:value pairs used for querying the collection.
            If nothing provided, all records are returned.

        Returns
        -------
        list
            If matching documents are found, they are returned as a list.
        
        Example
        -------
        
        connection.read({"testKey":"testValue"})

        """
        
        if data_filter is not None and not isinstance(data_filter, dict):
            raise Exception("Error, data_filter parameter is not a dictionary")
        
        try:
            result = self.database.animals.find(data_filter)
        except Exception as e:
            raise Exception(f"Error finding document(s): {e}")
        
        document_list = []
        
        # Iterate through returned result and add documents to list
        for document in result:
            document_list.append(document)
        return document_list
        
        
# Create method to implement the U in CRUD.
    def update(self, data_filter: dict, update: dict, update_all: bool = True) -> int:
        """
        Method to update one or multiple documents that meet the provided data_filter.

        Parameters
        ----------
        data_filter : dict
            Required. Key:value pairs used for querying the collection for updates.
        update : dict
            Required. Key:value pairs used for updating the document(s).
        update_all : bool, optional
            Boolean option. True updates all matching documents. False update the
            first match found. The default is True.

        Returns
        -------
        int
            The number of documents updated.
            
        Example
        -------
        connection.update({"test":"test"}, {"$set": {"test":"test1"}})

        """
        
        if data_filter is None:
            raise Exception("Data filter is required and cannot be None")
        if not isinstance(data_filter, dict):
            raise Exception("Error, data_filter parameter is not a dictionary")
        if update is None:
            raise Exception("No update to be made because update parameter is empty")
            
        try:
            if update_all == True:
                result = self.database.animals.update_many(data_filter, update)
            else:
                result = self.database.animals.update_one(data_filter, update)
        except Exception as e:
            raise Exception(f"Error updating record(s): {e}")
        
        modified_count = result.modified_count
        return modified_count


# Create method to implement the D in CRUD.
    def delete(self, data_filter: dict) -> int:
        """
        Delete documents from the collection matching the provided data_filter.

        Parameters
        ----------
        data_filter : dict
            Required. Key:value pairs used for querying the collection for deletions.

        Returns
        -------
        int
            The number of documents updated.
        
        Example
        -------
        connection.delete({"test":"test"})

        """
        
        if data_filter is None:
            raise Exception("No deletion(s) to be made because update parameter is empty")
        if not isinstance(data_filter, dict):
            raise Exception("Error, data_filter parameter is not a dictionary")
            
        try:
            result = self.database.animals.delete_many(data_filter)
            deleted_count = result.deleted_count
            return deleted_count
        except Exception as e:
            raise Exception(f"Error deleting records: {e}")
            