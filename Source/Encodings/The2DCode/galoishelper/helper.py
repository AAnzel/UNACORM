import galois as gl


class Galois_Helper():

    def __init__(self,_field) -> None:
        self.field = _field

    
    def get_power_of_field_element(self,el):
        divider = self.field.primitive_element
        i = 1
        while int(el/divider) != 1:
            i+= 1
            divider *= self.field.primitive_element
        
        return i

    def get_nth_unity_root_of_field(self,n):
        power_of_one = self.get_power_of_field_element(self.field(1))
        if power_of_one % n != 0:
            assert("failure in getting nth root") 
        return self.field.primitive_element**(power_of_one//n)

field = gl.Field(2**4,display="power")
helper = Galois_Helper(field)
print(helper.get_power_of_field_element(field(6)))
print(helper.get_nth_unity_root_of_field(3))