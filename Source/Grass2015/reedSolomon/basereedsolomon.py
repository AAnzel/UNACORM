import galois as gl
from pathos.multiprocessing import ProcessingPool as Pool
from . import helper

class Base_Reed_Solomon():
    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int,multi_processing,irr_poly=None,debug=True,p=1,):
        """base reed solomon class that is to be inherited
        Args:
            field_size (int): field characteristic
            message_length (int): message length
            payload_length (int): length of info symbols
            symbol_size (int): field degree
            multi_processing (boolean): allows multiprocessing of some steps
            irr_poly (list, optional): irreducible polynominal over which the field is to be constructed. Defaults to None.
            debug (bool, optional): determines whether steps should be printed to console. Defaults to True.
            p (int, optional): split up factor. Defaults to 1.
        """
        self.field_size = field_size
        if multi_processing:
            self.pool = Pool(p)
        else:
            self.pool = None
        if irr_poly ==None:
            try:
                self.galois_field = gl.GF(field_size**symbol_size)#TODO remove power asap
            except LookupError:
                print("need to find irreducible polynominal manually")
                irreducible_polynominal = gl.irreducible_poly(field_size,symbol_size)
                self.galois_field = gl.GF(field_size**symbol_size,irreducible_poly=irreducible_polynominal)   
        else:
            self.galois_field = gl.GF(field_size**symbol_size,irreducible_poly=irr_poly)   
        self.message_length = message_length
        self.payload_length = payload_length
        self.two_s = message_length - payload_length
        self.helper = helper.Galois_Helper(self.galois_field,self.pool,debug)
        self.multi = multi_processing
    

    def convert_to_symbol_array(self,array):
        """converts list of galois elements in their coefficent representation to their integer representation
        Args:
            array (list): list of list representing galois elements in their coefficent representation
        Returns:
            list: containing galosi elements
        """
        if self.galois_field.degree > 1:
            output = []
            for i in range(0,len(array)):
                output.append(int(self.galois_field.Vector(array[i])))
            return output
        return array
    
    def symbol_array_to_array(self,array):
        """converts list of galois elements into their coefficent representation
        Args:
            array (list): list of galois elements
        Returns:
            list: list of list each one representing a galois element in its polynominal representation
        """
        if self.galois_field.degree > 1:
            output = []
            for i in range(0,len(array)):
                output.append(self.galois_field(array[i]).vector().tolist())
            return output
        return array